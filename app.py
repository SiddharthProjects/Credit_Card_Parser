import streamlit as st
import pandas as pd
import io
import os
from parser import parse_statement
from regex_patterns import REGEX_TEMPLATES

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def main():
    """CreditCard Intel - Enhanced Visibility & Modern Design"""

    gemini_api_key = os.environ.get('GEMINI_API_KEY')

    st.set_page_config(
        page_title="CreditCard Intel",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #5f27cd 0%, #341f97 100%);
        }
        [data-testid="stSidebar"] * {
            color: #f8f9fa !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.3);
        }

        /* MAIN HEADER - Enhanced with border and shadow */
        .main-header {
            background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
            padding: 2.5rem 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,255,255,0.5);
            margin-bottom: 2rem;
            text-align: center;
            border: 2px solid rgba(102, 126, 234, 0.3);
        }

        .main-header h1 {
            background: linear-gradient(135deg, #1b2a68 0%, #667eea 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 0.3rem;
            letter-spacing: 1px;
        }

        .main-header p {
            color: #2d3748 !important;
            font-size: 1.3rem;
            font-weight: 700;
            margin-top: 0.5rem;
        }

        /* INFO CARD - Enhanced with gradient border */
        .info-card {
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            margin-bottom: 2rem;
            border: 2px solid #e2e8f0;
            position: relative;
        }
        
        .info-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px 20px 0 0;
        }
        
        .info-card h3 {
            color: #1a202c !important;
            font-weight: 800;
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
        }
        
        .info-card h4 {
            color: #2d3748 !important;
            font-weight: 700;
            font-size: 1.3rem;
            margin-bottom: 0.8rem;
        }
        
        .info-card p {
            color: #2d3748 !important;
            font-weight: 600;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        /* UPLOAD SECTION - Enhanced with vibrant gradient and strong borders */
        .upload-section {
            background: linear-gradient(135deg, #e0f2fe 0%, #ddd6fe 100%);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 15px 50px rgba(102, 126, 234, 0.2);
            border: 3px solid #667eea;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .upload-section::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 0.8; }
        }
        
        .upload-section h3 {
            color: #1a202c !important;
            font-weight: 800;
            font-size: 1.9rem;
            position: relative;
            z-index: 1;
            margin-bottom: 1.5rem;
        }

        /* UPLOAD INSTRUCTION BOX - High contrast with bold styling */
        .upload-instruction {
            background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%);
            padding: 2rem;
            border-radius: 16px;
            border: 3px dashed #667eea;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
            position: relative;
            z-index: 1;
        }
        
        .upload-instruction h4 {
            color: #1a202c !important;
            font-size: 1.4rem;
            font-weight: 900;
            margin: 0 0 0.5rem 0;
        }
        
        .upload-instruction p {
            color: #2d3748 !important;
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0;
        }

        /* FILE UPLOADER - Maximum visibility with gradient background */
        [data-testid="stFileUploader"] {
            padding: 2rem;
            border-radius: 16px;
            border: 3px solid #667eea !important;
            background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 50%, #ddd6fe 100%) !important;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2) !important;
            position: relative;
            z-index: 1;
        }
        
        [data-testid="stFileUploader"] label {
            color: #1a202c !important;
            font-weight: 900 !important;
            font-size: 1.3rem !important;
        }
        
        /* ALL TEXT IN FILE UPLOADER - Maximum contrast */
        [data-testid="stFileUploader"] div, 
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] strong,
        [data-testid="stFileUploader"] p,
        [data-testid="stFileUploader"] section {
            color: #1a202c !important;
            font-weight: 900 !important;
            font-size: 1.1rem !important;
        }
        
        /* Browse files button - Vibrant and prominent */
        [data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
            border-radius: 12px !important;
            font-weight: 900 !important;
            font-size: 1.15rem !important;
            padding: 1rem 2rem !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
            border: none !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        [data-testid="stFileUploader"] button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5) !important;
        }
        
        [data-testid="stFileUploader"] small {
            color: #1a202c !important;
            font-size: 1rem !important;
            font-weight: 800 !important;
        }

        /* RESULTS CARD - Enhanced with success accent */
        .results-card {
            background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            margin-top: 2rem;
            border: 2px solid #68d391;
            border-left: 6px solid #48bb78;
        }
        
        .results-card h3 {
            color: #1a202c !important;
            font-weight: 800;
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
        }
        
        .results-card h4 {
            color: #2d3748 !important;
            font-weight: 700;
            font-size: 1.3rem;
            margin-bottom: 0.8rem;
        }

        /* METRICS - Enhanced styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #1a202c !important;
            font-weight: 900;
        }
        
        [data-testid="stMetricLabel"] {
            color: #2d3748 !important;
            font-weight: 700;
            font-size: 1.1rem;
        }

        /* DATAFRAME - Enhanced styling */
        .dataframe {
            border-radius: 12px;
            overflow: hidden;
            font-size: 1rem;
            color: #1a202c !important;
            font-weight: 700;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        /* EXPANDER - Enhanced visibility */
        [data-testid="stExpander"] {
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%) !important;
            border-radius: 12px;
            border: 2px solid #cbd5e0 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        [data-testid="stExpander"] summary {
            color: #1a202c !important;
            font-weight: 800 !important;
            font-size: 1.1rem !important;
        }

        /* DOWNLOAD BUTTON - Enhanced styling */
        .stDownloadButton button {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
            color: white !important;
            font-weight: 800 !important;
            font-size: 1.2rem !important;
            border: none !important;
            padding: 1rem 2.5rem !important;
            border-radius: 30px !important;
            box-shadow: 0 6px 25px rgba(72, 187, 120, 0.4) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stDownloadButton button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 35px rgba(72, 187, 120, 0.5) !important;
        }

        /* SPINNER - Enhanced styling */
        .stSpinner > div {
            border-color: #667eea !important;
        }
        
        .stSpinner > div > div {
            border-top-color: #667eea !important;
        }

        /* SUCCESS/ERROR MESSAGES */
        .stSuccess {
            background-color: #c6f6d5 !important;
            color: #22543d !important;
            font-weight: 700;
            border-radius: 12px;
            border-left: 4px solid #48bb78;
        }
        
        .stError {
            background-color: #fed7d7 !important;
            color: #742a2a !important;
            font-weight: 700;
            border-radius: 12px;
            border-left: 4px solid #f56565;
        }

        /* TEXT AREA */
        textarea, .stTextArea textarea {
            color: #1a202c !important;
            font-weight: 600 !important;
            background-color: #f7fafc !important;
            border: 2px solid #cbd5e0 !important;
            border-radius: 8px !important;
        }

        /* GENERAL TEXT STYLING */
        .main .block-container p,
        .main .block-container li,
        .main .block-container span,
        .main .block-container label {
            color: #2d3748 !important;
            font-weight: 700;
        }

        /* HIDE DEFAULT ELEMENTS */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* ANIMATIONS */
        .info-card, .upload-section, .results-card, .main-header {
            animation: fadeInUp 0.6s ease-out;
        }
        
        @keyframes fadeInUp {
            from {opacity: 0; transform: translateY(30px);}
            to {opacity: 1; transform: translateY(0);}
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 1rem 0;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
        st.markdown('<h2 style="font-size: 1.5rem; margin-top: 1rem; font-weight: 800;">🧠 CreditCard Intel</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.subheader("📋 Supported Banks")
        for bank_key in REGEX_TEMPLATES.keys():
            bank_name = REGEX_TEMPLATES[bank_key]["identifier"][0]
            st.markdown(f"✓ {bank_name}")
        
        st.markdown("---")
        st.subheader("⚙️ System Status")
        
        is_key_valid = gemini_api_key and gemini_api_key != "YOUR_GEMINI_API_KEY"
        if is_key_valid:
            st.success("🤖 AI Fallback: Active")
            st.caption("Gemini LLM will assist if needed")
        else:
            st.warning("🤖 AI Fallback: Inactive")
            st.caption("Only RegEx extraction available")
        
        st.markdown("---")
        st.subheader("📊 Features")
        st.markdown("""
        - **Instant Extraction**: Get data in seconds
        - **Multi-Bank Support**: Works with major banks
        - **AI-Powered**: Smart fallback for tricky PDFs
        - **Secure**: All processing happens locally
        """)
        
        st.markdown("---")
        st.caption("v1.0.0 | Built with ❤️ by SIDDHARTH SRIVASTAVA")
    
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        
        st.markdown("""
            <div class="main-header">
                <h1>🧠 CreditCard Intel</h1>
                <p>CreditCard Statement Parser</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 How It Works")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("#### 1️⃣ Upload")
            st.markdown('<p>Upload your credit card statement PDF file</p>', unsafe_allow_html=True)
        with col_b:
            st.markdown("#### 2️⃣ Extract")
            st.markdown('<p>AI analyzes and extracts key information</p>', unsafe_allow_html=True)
        with col_c:
            st.markdown("#### 3️⃣ Review")
            st.markdown('<p>View and download extracted data instantly</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload Your Statement")
        
        st.markdown("""
            <div class="upload-instruction">
                <h4>📄 Drag & Drop Your PDF Here</h4>
                <p>or click "Browse files" button below • Max: 200MB • PDF Only</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a credit card statement from supported banks"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file:
            with st.spinner('🔍 Analyzing your statement...'):
                bytes_data = io.BytesIO(uploaded_file.getvalue())
                results = parse_statement(bytes_data, api_key=gemini_api_key)
            
            st.markdown('<div class="results-card">', unsafe_allow_html=True)
            
            if results.get("status") == "SUCCESS":
                bank_name = results.get('bank_name', 'N/A')
                method = results.get('extraction_method', 'RegEx')
                
                st.markdown("### ✅ Extraction Successful!")
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Bank Detected", bank_name)
                with col_stat2:
                    st.metric("Extraction Method", method)
                with col_stat3:
                    llm_status = results.get("llm_status", "N/A")
                    status_color = "🟢" if llm_status == "SUCCESS" else "🔵" if llm_status == "SKIPPED" else "🟡"
                    st.metric("AI Status", f"{status_color} {llm_status}")
                
                st.markdown("---")
                
                st.markdown("### 💳 Extracted Information")
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("#### 📅 Dates & Deadlines")
                    date_data = {
                        "Field": ["Statement Date", "Payment Due Date"],
                        "Value": [
                            results.get("statement_date", "NOT_FOUND"),
                            results.get("payment_due_date", "NOT_FOUND")
                        ]
                    }
                    df_dates = pd.DataFrame(date_data)
                    st.dataframe(df_dates, hide_index=True, use_container_width=True)
                    
                    st.markdown("#### 🔢 Card Information")
                    card_data = {
                        "Field": ["Card Last 4 Digits"],
                        "Value": [results.get("card_last_4_digits", "NOT_FOUND")]
                    }
                    df_card = pd.DataFrame(card_data)
                    st.dataframe(df_card, hide_index=True, use_container_width=True)
                
                with col_right:
                    st.markdown("#### 💰 Payment Details")
                    
                    total_due = results.get("total_due", "NOT_FOUND")
                    min_payment = results.get("min_payment", "NOT_FOUND")
                    
                    if total_due != "NOT_FOUND":
                        st.metric("Total Amount Due", f"₹ {total_due}", delta=None)
                    else:
                        st.metric("Total Amount Due", "NOT_FOUND", delta=None)
                    
                    if min_payment != "NOT_FOUND":
                        st.metric("Minimum Payment", f"₹ {min_payment}", delta=None)
                    else:
                        st.metric("Minimum Payment", "NOT_FOUND", delta=None)
                
                st.markdown("---")
                
                st.markdown("### 📊 Complete Data Overview")
                
                complete_data = {
                    "Data Point": [
                        "Card Last 4 Digits",
                        "Statement Date",
                        "Payment Due Date",
                        "Total Amount Due",
                        "Minimum Amount Due",
                    ],
                    "Extracted Value": [
                        results.get("card_last_4_digits", "NOT_FOUND"),
                        results.get("statement_date", "NOT_FOUND"),
                        results.get("payment_due_date", "NOT_FOUND"),
                        results.get("total_due", "NOT_FOUND"),
                        results.get("min_payment", "NOT_FOUND"),
                    ],
                    "Status": [
                        "✅ Found" if results.get("card_last_4_digits", "NOT_FOUND") != "NOT_FOUND" else "❌ Missing",
                        "✅ Found" if results.get("statement_date", "NOT_FOUND") != "NOT_FOUND" else "❌ Missing",
                        "✅ Found" if results.get("payment_due_date", "NOT_FOUND") != "NOT_FOUND" else "❌ Missing",
                        "✅ Found" if results.get("total_due", "NOT_FOUND") != "NOT_FOUND" else "❌ Missing",
                        "✅ Found" if results.get("min_payment", "NOT_FOUND") != "NOT_FOUND" else "❌ Missing",
                    ]
                }
                
                df_complete = pd.DataFrame(complete_data)
                
                def highlight_status(row):
                    if row['Status'] == "❌ Missing":
                        return ['background-color: #fed7d7; color: #742a2a; font-weight: 700'] * len(row)
                    else:
                        return ['background-color: #c6f6d5; color: #22543d; font-weight: 700'] * len(row)
                
                st.dataframe(
                    df_complete.style.apply(highlight_status, axis=1),
                    hide_index=True,
                    use_container_width=True
                )
                
                if 'raw_text' in results:
                    with st.expander("🔍 View Raw Extracted Text (Debug)"):
                        st.text_area("Raw Text", results['raw_text'], height=300, label_visibility="collapsed")
                
                st.markdown("---")
                csv_data = df_complete.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_data,
                    file_name=f"statement_data_{uploaded_file.name.replace('.pdf', '')}.csv",
                    mime="text/csv"
                )
                
            else:
                st.markdown("### ❌ Extraction Failed")
                st.error(f"**Reason:** {results.get('reason', 'Unknown error occurred.')}")
                
                st.markdown("#### 💡 Troubleshooting Tips:")
                st.markdown("""
                - Ensure the PDF is not password-protected
                - Check if the bank is in our supported list
                - Verify the PDF contains readable text (not just images)
                - Try uploading a different statement
                """)
                
                if 'raw_text' in results:
                    with st.expander("🔍 View Raw Extracted Text (Debug)"):
                        st.text_area("Raw Text", results['raw_text'], height=300, label_visibility="collapsed")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()



