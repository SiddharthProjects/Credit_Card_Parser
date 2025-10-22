
DATE_PATTERNS = [
    r"\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}",  
    r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}",  
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}",
]



AMOUNT_PATTERNS = [
    r"(?:Rs\.?\s*|INR\s*|₹\s*)?([\d,]+\.?\d{0,2})",
    r"([\d,]+\.\d{2})",
    r"([\d,]+)",
]



REGEX_TEMPLATES = {
    
    "hdfc": {
        "identifier": ["HDFC BANK", "HDFC"],
        "patterns": {
            "statement_date": [
                r"Statement\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Dt\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Date\s+of\s+Statement\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Period.*?to\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Stmt\.?\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Billing\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "payment_due_date": [
                r"Payment\s+Due\s+Date[\s\S]{0,50}?(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Payment\s+Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Pay\s+by\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "total_due": [
                
                r"Account\s+Summary[\s\S]{1,500}?Total\s+Dues[\s\S]{0,50}?([\d,]+\.[\d]{2})",
                r"Finance\s+Charges[\s\S]{0,150}?Total\s+Dues[\s\S]{0,50}?([\d,]+\.[\d]{2})",
                
                r"(?<!Minimum\s+Amount\s+Due)(?<!Past\s+Dues)(?<!Current\s+Dues)Total\s+Dues\s*\n?\s*([\d,]+\.[\d]{2})",
                
                r"=\s*Total\s+Dues\s+([\d,]+\.[\d]{2})",
                
                r"Total\s+Dues\s+((?!0\.00)[\d,]+\.[\d]{2})",
                
                r"Total\s+Dues\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Total\s+Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Total\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Total\s+Outstanding\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Total\s+Payable\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
            ],
            "min_payment": [
                
                r"Minimum\s+Amount\s+Due\s*[:\s]+([\d,]+\.[\d]{2})",
                r"Minimum\s+Amount\s+Due[\s\S]{0,100}?([\d,]+\.[\d]{2})",
                r"Minimum\s+Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                
                r"Minimum\s+Payment\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Minimum\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Min\.?\s+Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"MAD\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
            ],
            "card_last_4_digits": [
                r"Card\s+No\s*:?\s*\d{4}\s+\d{2}[Xx]{2}\s+[Xx]{4}\s+(\d{4})",
                r"Card\s+(?:No|Number|Account)\s*:?\s*.*?[\*Xx]{4,}(\d{4})",
                r"Credit\s+Card\s+(?:No|Number)\s*:?\s*.*?[\*Xx]{4,}(\d{4})",
                r"[\*Xx]{4,}\s*(\d{4})",
                r"XXXX[\s\-]*(\d{4})",
            ],
        },
    },


    
    "axis": {
        "identifier": ["AXIS BANK", "FLIPKART AXIS"],
        "patterns": {
            "statement_date": [
                r"Statement\s+(?:Generation\s+)?Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Dt\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Billing\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Period.*?to\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Date\s+of\s+Statement\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "payment_due_date": [
                r"Payment\s+Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Pay\s+by\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Payment\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Last\s+Payment\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "total_due": [
                r"Total\s+(?:Amount\s+)?(?:Payment\s+)?Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Total\s+Outstanding\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Closing\s+Balance\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Total\s+Payable\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Current\s+Dues\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
            ],
            "min_payment": [
                r"Minimum\s+(?:Amount\s+)?Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"MAD\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Min\.?\s+Payment\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
                r"Minimum\s+Payment\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Minimum\s+Amt\.?\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
            ],
            "card_last_4_digits": [
                r"Credit\s+Card\s+Number\s*:?\s*.*?[\*Xx]{4,}(\d{4})",
                r"Card\s+Number\s*:?\s*.*?[\*Xx]{4,}(\d{4})",
                r"[\*Xx]{4,}[\s\-]*(\d{4})",
                r"Card\s+No\.?\s*:?\s*.*?(\d{4})",
                r"XXXX[\s\-]*(\d{4})",
            ],
        },
    },



    "icici": {
        "identifier": ["ICICI BANK", "ICICI"],
        "patterns": {
            "statement_date": [
                r"Statement\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Date\s+of\s+Statement\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Period.*?to\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Billing\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+as\s+on\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "payment_due_date": [
                r"(?:Payment\s+)?Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Pay\s+by\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Payment\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Due\s+on\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "total_due": [
                r"(?:Your\s+)?Total\s+Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Total\s+Outstanding\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Total\s+Payment\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Current\s+(?:Amount\s+)?Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Total\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
            ],
            "min_payment": [
                r"Minimum\s+(?:Amount\s+)?Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"MAD\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Minimum\s+Payment\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Min\.?\s+(?:Amt|Amount)\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?[\d]{0,2})",
            ],
            "card_last_4_digits": [
                r"Card\s+Account\s+No\.?\s*:?\s*.*?(\d{4})",
                r"Card\s+Number\s*:?\s*.*?[\*Xx]+(\d{4})",
                r"[\*Xx]{4,}[\s\-]*(\d{4})",
                r"Credit\s+Card\s+No\.?\s*:?\s*.*?(\d{4})",
                r"XXXX[\s\-]*(\d{4})",
            ],
        },
    },



    "idfc": {
        "identifier": ["IDFC FIRST BANK", "IDFC FIRST", "IDFC BANK", "IDFC"],
        "patterns": {
            "statement_date": [
                
                r"Credit\s+Card\s+Statement[\s\S]{0,100}?(\d{1,2}\/\d{1,2}\/\d{4})\s*-\s*\d{1,2}\/\d{1,2}\/\d{4}",
                r"Statement[\s\S]{0,50}?(\d{1,2}\/\d{1,2}\/\d{4})\s*-\s*(\d{1,2}\/\d{1,2}\/\d{4})",
                
                r"\d{1,2}\/\d{1,2}\/\d{4}\s*-\s*(\d{1,2}\/\d{1,2}\/\d{4})",
                
                r"Statement\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Period.*?to\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Billing\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Date\s+of\s+Statement\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Dt\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "payment_due_date": [
                r"Payment\s+Due\s+Date[\s\S]{0,100}?(\d{1,2}\/\d{1,2}\/\d{4})",
                r"Payment\s+Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Pay\s+by\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Payment\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Last\s+(?:Date\s+(?:of|for)\s+)?Payment\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "total_due": [
                
                r"Total\s+Amount\s+Due\s*\n?\s*[₹`]?\s*([\d,]+\.?[\d]{0,2})\s*(?:CR|Dr)?",
                r"Total\s+Amount\s+Due[\s\S]{0,100}?[₹`]?\s*([\d,]+\.[\d]{2})",
                
                r"STATEMENT\s+SUMMARY[\s\S]{1,300}?Total\s+Amount\s+Due[\s\S]{0,50}?[₹`]?\s*([\d,]+\.[\d]{2})",
                
                r"Total\s+(?:Amount\s+)?Due\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})\s*(?:CR|Dr)?",
                r"Total\s+Outstanding\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
                r"Amount\s+(?:Payable|Due)\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
                r"Total\s+Payment\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
                r"Closing\s+Balance\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
            ],
            "min_payment": [
                
                r"Minimum\s+Amount\s+Due\s*\n?\s*[₹`]?\s*([\d,]+\.?[\d]{0,2})",
                r"Minimum\s+Amount\s+Due[\s\S]{0,100}?[₹`]?\s*([\d,]+\.[\d]{2})",
                r"Minimum\s+(?:Amount\s+)?Due\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
                r"MAD\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
                r"Minimum\s+Payment\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
                r"Min\.?\s+(?:Amt|Amount)\s*:?\s*(?:Rs\.?\s*|₹\s*|`\s*)?([\d,]+\.?[\d]{0,2})",
            ],
            "card_last_4_digits": [
                
                r"(?:Account\s+Number|Card\s+Number)\s*:?\s*[Xx]{4}\s+[Xx]{4}\s+[Xx]{4}\s+(\d{4})",
                r"Card\s+(?:No|Number)\s*:?\s*.*?[Xx]{4,}[\s\-]*(\d{4})",
                r"Account\s+Number\s*:?\s*.*?[Xx]{4,}[\s\-]*(\d{4})",
                r"[\*Xx]{4}[\s\*Xx]{4}[\s\*Xx]{4}[\s]*(\d{4})",
                r"XXXX[\s\-]*XXXX[\s\-]*XXXX[\s\-]*(\d{4})",
                r"Credit\s+Card\s+No\.?\s*:?\s*.*?(\d{4})",
            ],
        },
    },



    "yes": {
        "identifier": ["YES BANK", "YES FIRST", "YES CREDIT"],
        "patterns": {
            "statement_date": [
                r"Statement\s+(?:Date|Period).*?to\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Statement\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Billing\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Date\s+of\s+Statement\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "payment_due_date": [
                r"Payment\s+Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Due\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Pay\s+by\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
                r"Payment\s+Date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            ],
            "total_due": [
                r"Total\s+Dues?\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Closing\s+Balance\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Total\s+Outstanding\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Total\s+Payment\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
            ],
            "min_payment": [
                r"Minimum\s+Amount\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"MAD\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Minimum\s+Payment\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
                r"Min\.?\s+(?:Amt|Amount)\s+Due\s*:?\s*(?:Rs\.?\s*|₹\s*)?([\d,]+\.?\d{0,2})",
            ],
            "card_last_4_digits": [
                r"Card\s+Number\s*:?\s*.*?[\*Xx]+(\d{4})",
                r"[\*Xx]{4,}[\s\-]*(\d{4})",
                r"Credit\s+Card\s+No\.?\s*:?\s*.*?(\d{4})",
                r"XXXX[\s\-]*(\d{4})",
            ],
        },
    },
}
