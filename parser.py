import pdfplumber
import re
import io
import json
import os
import requests
from typing import Dict, Any, List
from regex_patterns import REGEX_TEMPLATES

GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"
API_URL_TEMPLATE = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key="

def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    """Extracts text from all pages of the PDF file."""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    cleaned_text = re.sub(r'[\r\n]+', '\n', text)
                    full_text += cleaned_text + "\n"
            return full_text
    except Exception as e:
        print(f"Error during PDF text extraction: {e}")
        return ""

def identify_bank(text: str) -> str:
    """Identifies the bank based on keywords found in the text."""
    clean_text = text.upper().replace('\n', ' ')
    for bank_key, template in REGEX_TEMPLATES.items():
        identifiers_to_check = [i.upper() for i in template.get("identifier", [])]
        for identifier in identifiers_to_check:
            if identifier in clean_text:
                return bank_key
    return "unknown"

def clean_amount(value: str) -> str:
    """
    Clean and normalize amount values.
    Handles formats like: 22,935.00, 22935.00, 22.935,00, etc.
    """
    if not value:
        return value
    
    
    value = value.replace('$', '').replace('£', '').replace('₹', '').replace('Rs', '').replace('`', '').strip()
    value = value.replace('DR', '').replace('Cr', '').replace('CR', '').replace('dr', '').replace('cr', '').strip()
    
    
    value = value.replace(' ', '')
    
    
    if ',' in value and '.' in value:
        value = value.replace(',', '')
    elif ',' in value:
        value = value.replace(',', '')
    
    
    value = re.sub(r'[^\d.]', '', value)
    
    
    if value.count('.') > 1:
        parts = value.split('.')
        value = ''.join(parts[:-1]) + '.' + parts[-1]
    
    return value.strip()

def extract_hdfc_total_dues(text: str) -> str:
    """
    Special extraction logic for HDFC Total Dues from Account Summary table.
    """
    pattern = r"Total\s+Dues[\s\S]{0,100}?([\d,]+\.[\d]{2})"
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    valid_amounts = []
    for match in matches:
        cleaned = clean_amount(match)
        try:
            amount_float = float(cleaned)
            if amount_float > 0:
                valid_amounts.append((amount_float, match))
        except:
            continue
    
    if valid_amounts:
        valid_amounts.sort(reverse=True)
        return valid_amounts[0][1]
    
    account_summary_pattern = r"Account\s+Summary[\s\S]{1,500}?Total\s+Dues[\s\S]{0,100}?([\d,]+\.[\d]{2})"
    match = re.search(account_summary_pattern, text, re.IGNORECASE)
    if match:
        amount = match.group(1)
        if float(clean_amount(amount)) > 0:
            return amount
    
    return None

def extract_idfc_amounts(text: str) -> Dict[str, str]:
    """
    Special extraction logic for IDFC First Bank amounts.
    IDFC statements have specific format with Statement Summary section.
    """
    result = {"total_due": None, "min_payment": None}
    
    
    summary_pattern = r"Statement\s+Summary[\s\S]{1,500}?Total\s+Amount\s+Due[\s\S]{0,100}?`?\s*([\d,]+\.[\d]{2})"
    match = re.search(summary_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if match:
        result["total_due"] = match.group(1)
    
    
    if result["total_due"]:
        min_pattern = r"Minimum\s+Amount\s+Due[\s\S]{0,100}?`?\s*([\d,]+\.[\d]{2})"
        min_match = re.search(min_pattern, text, re.IGNORECASE)
        if min_match:
            result["min_payment"] = min_match.group(1)
    
    
    if not result["total_due"] or not result["min_payment"]:
        payment_section_pattern = r"Payment\s+Due\s+Date[\s\S]{0,200}?Total\s+Amount\s+Due[\s\S]{0,50}?`?\s*([\d,]+\.[\d]{2})[\s\S]{0,100}?Minimum\s+Amount\s+Due[\s\S]{0,50}?`?\s*([\d,]+\.[\d]{2})"
        payment_match = re.search(payment_section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if payment_match:
            if not result["total_due"]:
                result["total_due"] = payment_match.group(1)
            if not result["min_payment"]:
                result["min_payment"] = payment_match.group(2)
    
    
    if not result["total_due"]:
        total_standalone = re.search(r"Total\s+Amount\s+Due\s*\n?\s*`?\s*([\d,]+\.[\d]{2})\s*(?:CR|Dr)?", text, re.IGNORECASE)
        if total_standalone:
            amount = total_standalone.group(1)
            try:
                if float(clean_amount(amount)) > 0:
                    result["total_due"] = amount
            except:
                pass
    
    if not result["min_payment"]:
        min_standalone = re.search(r"Minimum\s+Amount\s+Due\s*\n?\s*`?\s*([\d,]+\.[\d]{2})", text, re.IGNORECASE)
        if min_standalone:
            result["min_payment"] = min_standalone.group(1)
    
    return result

def extract_with_llm(full_text: str, api_key: str) -> Dict[str, Any]:
    """Uses Gemini LLM to extract structured data as a fallback."""
    if not api_key or api_key == "GEMINI_API_KEY":
        return {"llm_status": "SKIPPED", "reason": "Gemini API Key is missing or placeholder."}

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "statement_date": {"type": "STRING"},
            "payment_due_date": {"type": "STRING"},
            "total_due": {"type": "STRING"},
            "min_payment": {"type": "STRING"},
            "card_last_4_digits": {"type": "STRING"},
        },
    }

    system_prompt = (
        "You are an expert financial data extractor. Extract five specific fields "
        "into strict JSON. Use only data from the text; if missing, return 'NOT_FOUND'. "
        "For total_due, find the 'Total Amount Due' or 'Total Dues' value, NOT zero values. "
        "Remove DR, Cr, or CR suffixes from amounts."
    )
    user_query = f"Extract data from the statement text:\n---\n{full_text}\n---"

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema,
            "temperature": 0.0
        },
    }

    try:
        api_url = API_URL_TEMPLATE + api_key
        response = requests.post(api_url, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status()
        result = response.json()

        if result.get('candidates'):
            json_text = result['candidates'][0]['content']['parts'][0]['text']
            llm_extracted_data = json.loads(json_text)
            llm_extracted_data["llm_status"] = "SUCCESS"
            return llm_extracted_data

        return {"llm_status": "FAILED", "reason": "Empty or malformed LLM response."}

    except requests.exceptions.HTTPError as err:
        return {"llm_status": "FAILED", "reason": f"HTTP Error: {err}"}
    except Exception as e:
        return {"llm_status": "FAILED", "reason": f"Error processing LLM response: {e}"}

def parse_statement(pdf_file: io.BytesIO, api_key: str = None) -> Dict[str, Any]:
    """Main function: parses PDF with RegEx, falls back to LLM if needed."""
    full_text = extract_text_from_pdf(pdf_file)
    if not full_text:
        return {"status": "FAILED", "reason": "Could not extract text from PDF."}

    bank_key = identify_bank(full_text)
    if bank_key == "unknown":
        supported = ', '.join(k.replace('_', ' ').title() for k in REGEX_TEMPLATES.keys())
        return {"status": "FAILED", "reason": f"Unknown issuer. Supported banks: {supported}"}

    template = REGEX_TEMPLATES.get(bank_key)
    patterns = template["patterns"]
    bank_display_name = template["identifier"][0]

    extracted_data = {
        "bank_name": bank_display_name,
        "status": "SUCCESS",
        "extraction_method": "RegEx",
        "raw_text": full_text
    }

    keys_to_search = ["statement_date", "payment_due_date", "total_due", "min_payment", "card_last_4_digits"]

    
    for key in keys_to_search:
        extracted_data[key] = "NOT_FOUND"
        
        
        if bank_key == "hdfc" and key == "total_due":
            hdfc_amount = extract_hdfc_total_dues(full_text)
            if hdfc_amount:
                extracted_data[key] = clean_amount(hdfc_amount)
                continue
        
        
        if bank_key == "idfc" and key in ["total_due", "min_payment"]:
            idfc_amounts = extract_idfc_amounts(full_text)
            if idfc_amounts[key]:
                extracted_data[key] = clean_amount(idfc_amounts[key])
                continue
        
        for pattern_str in patterns.get(key, []):
            try:
                pattern = re.compile(pattern_str, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                match = pattern.search(full_text)
                if match:
                    value = match.group(1).strip()
                    
                    if key in ["total_due", "min_payment"]:
                        value = clean_amount(value)
                        if not value or not re.match(r'^\d+\.?\d*$', value):
                            continue
                        if key == "total_due" and float(value) == 0:
                            continue
                    
                    value = re.sub(r'[\s\n]+', ' ', value).strip()
                    
                    if value:
                        extracted_data[key] = value
                        break
            except re.error as e:
                print(f"Regex error for key '{key}': {e}")
                continue

    
    needs_fallback = any(extracted_data[key] == "NOT_FOUND" for key in ["total_due", "payment_due_date", "min_payment"])
    is_key_valid = api_key and api_key != "GEMINI_API_KEY"

    if needs_fallback and is_key_valid:
        llm_results = extract_with_llm(full_text, api_key)
        extracted_data["llm_status"] = llm_results.get("llm_status", "SKIPPED")

        if llm_results.get("llm_status") == "SUCCESS":
            extracted_data["extraction_method"] = "RegEx/LLM Fallback"
            for key in keys_to_search:
                if extracted_data[key] == "NOT_FOUND" and llm_results.get(key) not in ["NOT_FOUND", None]:
                    value = llm_results[key]
                    if key in ["total_due", "min_payment"]:
                        value = clean_amount(value)
                        try:
                            if key == "total_due" and float(value) == 0:
                                continue
                        except:
                            pass
                    extracted_data[key] = value
        elif llm_results.get("llm_status") == "FAILED":
            extracted_data["llm_error"] = llm_results.get("reason", "Unknown LLM error.")
    elif not is_key_valid:
        extracted_data["llm_status"] = "SKIPPED"
        extracted_data["llm_error"] = "Gemini API Key missing or placeholder."

    return extracted_data
