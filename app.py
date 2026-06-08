import streamlit as st
from markitdown import MarkItDown
import os

# Configure the web layout
st.set_page_config(page_title="Universal Markdown Converter", page_icon="📄", layout="centered")

st.title("📄 Universal Markdown Converter")
st.write("Convert your Word documents, Excel sheets, PDFs, and presentations into clean Markdown format instantly.")

# Safely initialize MarkItDown once and cache it for speed
@st.cache_resource
def get_converter():
    return MarkItDown()

try:
    md = get_converter()
except Exception as e:
    st.error(f"Failed to initialize converter engine: {e}")

# Create the file dropzone interface
uploaded_file = st.file_uploader(
    "Drag and drop your document here", 
    type=["docx", "pptx", "xlsx", "xls", "pdf", "html", "csv", "json", "xml", "txt"]
)

if uploaded_file is not None:
    # Save the uploaded file data stream temporarily
    temp_file_path = f"temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    try:
        with st.spinner("Analyzing document structure and parsing layers..."):
            # Run MarkItDown execution
            conversion_result = md.convert(temp_file_path)
            markdown_output = conversion_result.text_content
            
        st.success("Conversion successful!")
        
        # Display the result to the user using UI tabs
        preview_tab, raw_code_tab = st.tabs(["👀 Layout Preview", "📋 Raw Markdown Code"])
        
        with preview_tab:
            st.markdown(markdown_output)
            
        with raw_code_tab:
            st.code(markdown_output, language="markdown")
            
        # Add a one-click download button for the user
        st.download_button(
            label="⬇️ Download Markdown File",
            data=markdown_output,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}.md",
            mime="text/markdown"
        )
            
    except Exception as error:
        st.error(f"An error occurred during parsing: {error}")
        
    finally:
        # Securely sweep away the temporary file from the cloud environment
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)