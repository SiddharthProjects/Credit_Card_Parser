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
    """CreditCard Intel - Enhanced Visuals & Upload Box Clarity"""

    gemini_api_key = os.environ.get('GEMINI_API_KEY')

    st.set_page_config(
        page_title="CreditCard Intel",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        /* ===== Global App Background ===== */
        .stApp {
            background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* ===== Sidebar Styling ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #5f27cd 0%, #341f97 100%);
        }
        [data-testid="stSidebar"] * { color: #f8f9fa !important; }

        /* ===== Header Card ===== */
        .main-header {
            background: linear-gradient(130deg, #ffffff 0%, #eef1ff 50%, #f4eaff 100%);
            padding: 2.5rem 2rem;
            border-radius: 25px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.3);
            animation: floatCard 6s ease-in-out infinite alternate;
        }
        @keyframes floatCard {
            from { transform: translateY(0px); }
            to { transform: translateY(-6px); }
        }

        .main-header h1 {
            color: #1b2a68 !important;
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 0.3rem;
            letter-spacing: 1px;
        }
        .main-header p {
            color: #353b50 !important;
            font-size: 1.2rem;
            font-weight: 600;
        }

        /* ===== Info Card ===== */
        .info-card {
            background: rgba(255,255,255,0.95);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }

        /* ===== Upload Section ===== */
        .upload-section {
            background: linear-gradient(120deg, #eaf0ff 0%, #ffffff 50%, #e0eaff 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(41,65,171,0.12);
            border: 1.5px solid #d1d9ff;
            margin-bottom: 2rem;
            backdrop-filter: blur(8px);
        }

        .upload-instruction {
            background: linear-gradient(120deg, #f8fafc 60%, #e4e7fa 100%);
            padding: 1.7rem;
            border-radius: 14px;
            border: 2.5px dashed #636363;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 16px rgba(41,65,171,0.07);
        }
        .upload-instruction h4 {
            color: #1b2a68 !important;
            font-size: 1.25rem;
            font-weight: 800;
            margin: 0;
        }

        /* ===== File Uploader (Drag & Drop Box) ===== */
        [data-testid="stFileUploader"] {
            padding: 1.5rem;
            border-radius: 16px;
            border: 2.5px dashed #7088ff;
            background: linear-gradient(120deg, #edf2ff 0%, #ffffff 60%, #e5e8ff 100%) !important;
            box-shadow: 0 8px 32px rgba(41,65,171,0.12);
            transition: all 0.3s ease;
        }
        [data-testid="stFileUploader"]:hover {
            box-shadow: 0 10px 35px rgba(41,65,171,0.25);
            transform: scale(1.01);
        }
        [data-testid="stFileUploader"] label {
            color: #1b2a68 !important;
            font-weight: 800 !important;
            font-size: 1.15rem !important;
        }
        [data-testid="stFileUploader"] div, 
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] strong,
        [data-testid="stFileUploader"] p {
            color: #1b1b1b !important;
            font-weight: 800 !important;
        }
        [data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #1b2a68 0%, #2941ab 100%);
            color: #fff !important;
            border-radius: 18px;
            font-weight: bold;
            font-size: 1.08rem;
            padding: 0.7rem 1.5rem;
            border: none;
            box-shadow: 0 3px 12px rgba(41,65,171,0.15);
            transition: all 0.2s;
        }
        [data-testid="stFileUploader"] button:hover {
            background: linear-gradient(135deg, #2941ab 0%, #1b2a68 100%);
        }

        /* ===== Expander (White Slip for Raw Text) ===== */
        [data-testid="stExpander"] {
            background: linear-gradient(120deg, #f9f9ff 0%, #eef1ff 70%, #f3edff 100%)!important;
            border-radius: 15px;
            border: 1px solid #d2d8ff;
            box-shadow: 0 4px 18px rgba(41,65,171,0.12);
        }
        [data-testid="stExpander"] div, 
        [data-testid="stExpander"] span, 
        [data-testid="stExpander"] p, 
        [data-testid="stExpander"] textarea {
            color: #1b1b1b !important;
            font-weight: 700;
        }

        /* ===== Results Card ===== */
        .results-card {
            background: linear-gradient(120deg, #ffffff 0%, #eef1ff 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-left: 6px solid #00b894;
        }

        /* ===== Animations ===== */
        .main-header, .info-card, .upload-section, .results-card {
            animation: fadeInUp 0.6s ease-out;
        }
        @keyframes fadeInUp {
            from {opacity: 0; transform: translateY(30px);}
            to {opacity: 1; transform: translateY(0);}
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
        st.markdown("## 🧠 CreditCard Intel")
        st.markdown("---")
        st.subheader("📋 Supported Banks")
        for bank_key in REGEX_TEMPLATES.keys():
            bank_name = REGEX_TEMPLATES[bank_key]["identifier"][0]
            st.markdown(f"✓ {bank_name}")
        st.markdown("---")

    # Main layout
    col1, col2, col3 = st.columns([1,6,1])
    with col2:
        st.markdown("""
            <div class="main-header">
                <h1>🧠 CreditCard Intel</h1>
                <p>Smart Statement Parser Powered by AI</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 How It Works")
        st.markdown("""
        1️⃣ **Upload:** Upload your statement PDF  
        2️⃣ **Extract:** AI analyzes and extracts details  
        3️⃣ **Review:** Instantly view and download data
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Upload Section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload Your Statement")
        st.markdown("""
            <div class="upload-instruction">
                <h4>📄 Drag & Drop Your PDF Here</h4>
                <p>or click "Browse files" • Max 200MB • PDF only</p>
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
                st.success("✅ Extraction Successful!")
                df_complete = pd.DataFrame({
                    "Field": ["Statement Date", "Payment Due Date", "Total Due"],
                    "Value": [
                        results.get("statement_date","NOT_FOUND"),
                        results.get("payment_due_date","NOT_FOUND"),
                        results.get("total_due","NOT_FOUND")
                    ]
                })
                st.dataframe(df_complete, hide_index=True, use_container_width=True)

                if 'raw_text' in results:
                    with st.expander("🔍 View Raw Extracted Text (Debug)"):
                        st.text_area("Raw Text", results['raw_text'], height=300)
            else:
                st.error("❌ Extraction Failed")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
