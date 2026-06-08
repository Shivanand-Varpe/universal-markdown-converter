import streamlit as st
from markitdown import MarkItDown
import os

# 1. Page Configuration
st.set_page_config(
    page_title="MarkDownify Pro", 
    page_icon="⚡", 
    layout="centered"
)

# 2. Premium CSS Injection (Aesthetics & Animations)
st.markdown("""
    <style>
    /* Main background and font cleanup */
    .main {
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(45deg, #ff4b4b, #ff7676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle Description */
    .sub-title {
        color: #808495;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }
    
    /* File Uploader Container Box Customization */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #30363d;
        background-color: #161b22;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #ff4b4b;
        background-color: #1f242c;
    }
    
    /* Custom Design for Download Button */
    .stDownloadButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff4b4b 0%, #cc1111 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2);
        transition: all 0.3s ease !important;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
    }
    
    /* Tab Design Cleanup */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Clean Header Interface
st.markdown('<h1 class="main-title">⚡ MarkDownify Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">High-performance engine turning complex enterprise documents into production-ready Markdown layers.</p>', unsafe_allow_html=True)

# 4. Engine Initialization
@st.cache_resource
def get_converter():
    return MarkItDown()

try:
    md = get_converter()
except Exception as e:
    st.error(f"Failed to initialize converter engine: {e}")

# 5. Dropzone File Interface
uploaded_file = st.file_uploader(
    "", # Hidden label text because CSS handles the context box
    type=["docx", "pptx", "xlsx", "xls", "pdf", "html", "csv", "json", "xml", "txt"]
)

# 6. Core Conversion Pipeline
if uploaded_file is not None:
    temp_file_path = f"temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    try:
        with st.spinner("Decoding layout layers..."):
            conversion_result = md.convert(temp_file_path)
            markdown_output = conversion_result.text_content
            
        st.balloons() # Fun completion asset trigger
        
        # Display Result Tabs
        preview_tab, raw_code_tab = st.tabs(["Layout Preview", "Clean Source Markdown"])
        
        with preview_tab:
            st.markdown(markdown_output)
            
        with raw_code_tab:
            st.code(markdown_output, language="markdown")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Download Asset
        st.download_button(
            label="Download Markdown File (.md)",
            data=markdown_output,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}.md",
            mime="text/markdown"
        )
            
    except Exception as error:
        st.error(f"An error occurred during parsing: {error}")
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)