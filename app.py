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
        /* Main background - Light Blue Gradient */
        .stApp {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
        }
        
        /* Main content container */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Sidebar styling - Deep Blue */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1565c0 0%, #0d47a1 100%);
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.3);
        }
        
        /* Header styling - Rich Blue with White Text */
        .main-header {
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 2rem;
            text-align: center;
            border: 5px solid #0d47a1;
        }
        
        .main-header h1 {
            color: #ffffff !important;
            font-size: 4rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-shadow: 3px 3px 8px rgba(0,0,0,0.4);
            letter-spacing: 3px;
        }
        
        .main-header p {
            color: #ffffff !important;
            font-size: 1.6rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Card styling - White Background with Blue Border */
        .info-card {
            background: #ffffff;
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            margin-bottom: 2rem;
            border: 4px solid #1976d2;
        }
        
        .info-card h3 {
            color: #1565c0 !important;
            font-weight: 800;
            font-size: 2rem;
            margin-bottom: 1.5rem;
        }
        
        .info-card h4 {
            color: #0d47a1 !important;
            font-weight: 700;
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
        }
        
        .info-card p {
            color: #212121 !important;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        /* Upload section - White Background */
        .upload-section {
            background: #ffffff;
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            margin-bottom: 2rem;
            border: 4px solid #42a5f5;
        }
        
        .upload-section h3 {
            color: #1565c0 !important;
            font-weight: 800;
            font-size: 2rem;
        }
        
        /* Custom upload instruction box - Bright Attention Color */
        .upload-instruction {
            background: #fff9c4;
            padding: 2.5rem;
            border-radius: 12px;
            border: 5px dashed #f57c00;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .upload-instruction h4 {
            color: #d84315 !important;
            font-size: 2rem;
            font-weight: 900;
            margin: 0;
            text-transform: uppercase;
        }
        
        .upload-instruction p {
            color: #212121 !important;
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0.5rem 0 0 0;
        }
        
        /* Results card - White with Green Accent */
        .results-card {
            background: #ffffff;
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            margin-top: 2rem;
            border: 4px solid #66bb6a;
        }
        
        .results-card h3 {
            color: #388e3c !important;
            font-weight: 800;
            font-size: 2rem;
        }
        
        .results-card h4 {
            color: #0d47a1 !important;
            font-weight: 700;
            font-size: 1.4rem;
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
            background: #c8e6c9;
            color: #2e7d32;
        }
        
        .badge-warning {
            background: #fff9c4;
            color: #f57f17;
        }
        
        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Metric cards - Bold Blue */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #1565c0 !important;
            font-weight: 900;
        }
        
        [data-testid="stMetricLabel"] {
            color: #0d47a1 !important;
            font-weight: 800;
            font-size: 1.2rem;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
            font-size: 1.05rem;
        }
        
        /* File uploader styling - White Background */
        [data-testid="stFileUploader"] {
            background: #ffffff !important;
            padding: 2rem;
            border-radius: 12px;
            border: 3px solid #1976d2;
        }
        
        [data-testid="stFileUploader"] label {
            color: #0d47a1 !important;
            font-weight: 800 !important;
            font-size: 1.3rem !important;
        }
        
        [data-testid="stFileUploader"] small {
            color: #212121 !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stFileUploader"] section {
            background-color: #ffffff !important;
        }
        
        /* All text in main content area - Dark for Visibility */
        .main .block-container p,
        .main .block-container li,
        .main .block-container span,
        .main .block-container label {
            color: #212121 !important;
        }
        
        /* Markdown headers in main content */
        .main .block-container h1,
        .main .block-container h2 {
            color: #1565c0 !important;
            font-weight: 800;
        }
        
        .main .block-container h3,
        .main .block-container h4 {
            color: #0d47a1 !important;
            font-weight: 700;
        }
        
        /* Expander text */
        [data-testid="stExpander"] {
            background-color: #ffffff;
            border-radius: 8px;
            border: 2px solid #1976d2;
        }
        
        /* Button styling - Blue Gradient */
        .stDownloadButton button {
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
            color: white !important;
            font-weight: 800;
            font-size: 1.2rem;
            border: none;
            padding: 1rem 2.5rem;
            border-radius: 10px;
        }
        
        .stDownloadButton button:hover {
            background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(25, 118, 210, 0.4);
        }
        
        /* Spinner text */
        .stSpinner > div {
            color: #1565c0 !important;
            font-weight: 700;
            font-size: 1.2rem;
        }
        
        /* Success/Error messages */
        .stSuccess {
            background-color: #c8e6c9 !important;
            color: #2e7d32 !important;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        .stError {
            background-color: #ffcdd2 !important;
            color: #c62828 !important;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        /* Column text styling */
        [data-testid="column"] p {
            color: #212121 !important;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)
    
    
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
        st.markdown('<h1 style="font-size: 2rem; margin-top: 0.5rem; font-weight: 800;">🧠 CreditCard Intel</h1>', unsafe_allow_html=True)
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
                <h1>🧠 CREDITCARD INTEL</h1>
                <p>Smart CreditCard Statement Parser</p>
            </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 How It Works")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("#### 1️⃣ Upload")
            st.markdown('<p style="color: #212121 !important; font-weight: 700; font-size: 1.15rem;">Upload your credit card statement PDF</p>', unsafe_allow_html=True)
        with col_b:
            st.markdown("#### 2️⃣ Extract")
            st.markdown('<p style="color: #212121 !important; font-weight: 700; font-size: 1.15rem;">AI analyzes and extracts key data</p>', unsafe_allow_html=True)
        with col_c:
            st.markdown("#### 3️⃣ Review")
            st.markdown('<p style="color: #212121 !important; font-weight: 700; font-size: 1.15rem;">View extracted information instantly</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload Your Statement")
        
        st.markdown("""
            <div class="upload-instruction">
                <h4>📄 DRAG & DROP YOUR PDF HERE</h4>
                <p>or click "Browse files" button below | Max Size: 200MB | PDF Only</p>
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
                        return ['background-color: #ffcdd2; color: #c62828; font-weight: 700'] * len(row)
                    else:
                        return ['background-color: #c8e6c9; color: #2e7d32; font-weight: 700'] * len(row)
                
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
