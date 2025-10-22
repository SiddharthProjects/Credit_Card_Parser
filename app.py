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
    """CreditCard Intel - Smart Statement Parser with modern redesigned UI"""
    
    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    
    
    st.set_page_config(
        page_title="CreditCard Intel",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    
    st.markdown("""
        <style>
        /* Main background - Light blue/gray gradient */
        .stApp {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        }
        
        /* Main content container */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #1e88e5;
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.3);
        }
        
        /* Header styling */
        .main-header {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
            text-align: center;
            border: 3px solid #1e88e5;
        }
        
        .main-header h1 {
            color: #000000 !important;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        .main-header p {
            color: #555 !important;
            font-size: 1.1rem;
        }
        
        /* Card styling */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            border-left: 4px solid #1e88e5;
        }
        
        .info-card h3, .info-card h4, .info-card p {
            color: #333 !important;
        }
        
        /* Upload section */
        .upload-section {
            background: white;
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            border: 3px dashed #ff0000;
        }
        
        .upload-section h3 {
            color: #000000 !important;
            font-weight: 700;
        }
        
        /* Results card */
        .results-card {
            background: #f1f8e9;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            margin-top: 2rem;
            border-left: 5px solid #4caf50;
        }
        
        .results-card h3, .results-card h4 {
            color: #1b5e20 !important;
        }
        
        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            margin: 0.5rem;
        }
        
        .badge-success {
            background: #d4edda;
            color: #155724;
        }
        
        .badge-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem;
            color: #1565c0 !important;
            font-weight: 700;
        }
        
        [data-testid="stMetricLabel"] {
            color: #424242 !important;
            font-weight: 600;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* All text in main content area */
        .main .block-container p,
        .main .block-container li,
        .main .block-container span,
        .main .block-container label {
            color: #212121 !important;
        }
        
        /* Markdown headers in main content */
        .main .block-container h1,
        .main .block-container h2,
        .main .block-container h3,
        .main .block-container h4 {
            color: #1565c0 !important;
        }
        
        /* Expander text */
        [data-testid="stExpander"] {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        
        /* Button styling */
        .stDownloadButton button {
            background-color: #1e88e5;
            color: white !important;
            font-weight: 600;
            border: none;
        }
        
        .stDownloadButton button:hover {
            background-color: #1565c0;
        }
        
        /* File uploader text */
        [data-testid="stFileUploader"] label {
            color: #ff0000 !important;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        [data-testid="stFileUploader"] small {
            color: #ff0000 !important;
            font-size: 0.95rem;
            font-weight: 600;
        }
        
        [data-testid="stFileUploader"] {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
        }
        
        [data-testid="stFileUploader"] > div {
            background: white !important;
        }
        
        [data-testid="stFileUploader"] span {
            color: #ff0000 !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }
        
        /* File uploader drag area */
        [data-testid="stFileUploader"] button {
            background: white !important;
            color: #ff0000 !important;
            border: 2px solid #ff0000 !important;
        }
        
        /* Spinner text */
        .stSpinner > div {
            color: #1e88e5 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
        st.markdown('<h1 style="color: white !important; font-size: 1.8rem; margin-top: 0.5rem;">🧠 CreditCard Intel</h1>', unsafe_allow_html=True)
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
                <p>Smart CreditCard Statement Parser </p>
            </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 How It Works")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("#### 1️⃣ Upload")
            st.caption("Upload your credit card statement PDF")
        with col_b:
            st.markdown("#### 2️⃣ Extract")
            st.caption("AI analyzes and extracts key data")
        with col_c:
            st.markdown("#### 3️⃣ Review")
            st.caption("View extracted information instantly")
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload Your Statement")
        st.markdown("""
            <div style="background: white; padding: 2rem; border: 3px dashed #ff0000; border-radius: 10px; text-align: center; margin-bottom: 1rem;">
                <p style="color: #ff0000; font-weight: 700; font-size: 1.3rem; margin: 0;">
                    📄 Drag and drop your PDF here or click Browse below
                </p>
                <p style="color: #ff0000; font-weight: 600; font-size: 1rem; margin-top: 0.5rem;">
                    Maximum file size: 200MB • Format: PDF only
                </p>
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
                        return ['background-color: #fee; color: #c00'] * len(row)
                    else:
                        return ['background-color: #efe; color: #060'] * len(row)
                
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
