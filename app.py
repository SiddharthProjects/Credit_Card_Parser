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
        /* Main background - Elegant Gradient */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Main content container */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Sidebar styling - Deep Purple */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #5f27cd 0%, #341f97 100%);
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.3);
        }
        
        /* Header styling - Elegant and Compact */
        .main-header {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2.5rem 2rem;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .main-header h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 0.3rem;
            letter-spacing: 1px;
        }
        
        .main-header p {
            color: #6c757d !important;
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        
        /* Card styling - Clean White */
        .info-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
        }
        
        .info-card h3 {
            color: #667eea !important;
            font-weight: 700;
            font-size: 1.6rem;
            margin-bottom: 1.5rem;
        }
        
        .info-card h4 {
            color: #764ba2 !important;
            font-weight: 700;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        
        .info-card p {
            color: #495057 !important;
            font-weight: 600;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        /* Upload section - Elegant */
        .upload-section {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
        }
        
        .upload-section h3 {
            color: #667eea !important;
            font-weight: 700;
            font-size: 1.6rem;
        }
        
        /* Custom upload instruction box */
        .upload-instruction {
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 3px dashed #e17055;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(225,112,85,0.2);
        }
        
        .upload-instruction h4 {
            color: #d63031 !important;
            font-size: 1.5rem;
            font-weight: 800;
            margin: 0;
        }
        
        .upload-instruction p {
            color: #2d3436 !important;
            font-size: 1rem;
            font-weight: 600;
            margin: 0.5rem 0 0 0;
        }
        
        /* Results card - Success Green */
        .results-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-top: 2rem;
            border-left: 5px solid #00b894;
            backdrop-filter: blur(10px);
        }
        
        .results-card h3 {
            color: #00b894 !important;
            font-weight: 700;
            font-size: 1.6rem;
        }
        
        .results-card h4 {
            color: #667eea !important;
            font-weight: 700;
            font-size: 1.3rem;
        }
        
        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Metric cards - Elegant */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            color: #667eea !important;
            font-weight: 800;
        }
        
        [data-testid="stMetricLabel"] {
            color: #6c757d !important;
            font-weight: 700;
            font-size: 1rem;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
            font-size: 0.95rem;
        }
        
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            background: rgba(255, 255, 255, 0.9) !important;
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid #dfe6e9;
        }
        
        [data-testid="stFileUploader"] label {
            color: #2d3436 !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }
        
        [data-testid="stFileUploader"] small {
            color: #636e72 !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
        }
        
        /* All text in main content */
        .main .block-container p,
        .main .block-container li,
        .main .block-container span,
        .main .block-container label {
            color: #495057 !important;
        }
        
        /* Markdown headers */
        .main .block-container h1,
        .main .block-container h2 {
            color: #667eea !important;
            font-weight: 700;
        }
        
        .main .block-container h3,
        .main .block-container h4 {
            color: #495057 !important;
            font-weight: 600;
        }
        
        /* Expander */
        [data-testid="stExpander"] {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            border: 1px solid #dfe6e9;
        }
        
        /* Button styling - Gradient */
        .stDownloadButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            font-weight: 700;
            font-size: 1.1rem;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
        }
        
        .stDownloadButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Spinner */
        .stSpinner > div {
            color: #667eea !important;
            font-weight: 600;
        }
        
        /* Success/Error messages */
        .stSuccess {
            background-color: #d4edda !important;
            color: #155724 !important;
            font-weight: 600;
            border-radius: 10px;
        }
        
        .stError {
            background-color: #f8d7da !important;
            color: #721c24 !important;
            font-weight: 600;
            border-radius: 10px;
        }
        
        /* Column text */
        [data-testid="column"] p {
            color: #495057 !important;
            font-weight: 600;
        }
        
        /* Smooth animations */
        .info-card, .upload-section, .results-card, .main-header {
            animation: fadeInUp 0.6s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
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
                <p>Smart Statement Parser Powered by AI</p>
            </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 How It Works")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("#### 1️⃣ Upload")
            st.markdown('<p style="color: #495057 !important; font-weight: 600; font-size: 1rem; line-height: 1.5;">Upload your credit card statement PDF file</p>', unsafe_allow_html=True)
        with col_b:
            st.markdown("#### 2️⃣ Extract")
            st.markdown('<p style="color: #495057 !important; font-weight: 600; font-size: 1rem; line-height: 1.5;">AI analyzes and extracts key information</p>', unsafe_allow_html=True)
        with col_c:
            st.markdown("#### 3️⃣ Review")
            st.markdown('<p style="color: #495057 !important; font-weight: 600; font-size: 1rem; line-height: 1.5;">View and download extracted data instantly</p>', unsafe_allow_html=True)
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
                        return ['background-color: #fee; color: #c00; font-weight: 600'] * len(row)
                    else:
                        return ['background-color: #efe; color: #060; font-weight: 600'] * len(row)
                
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
