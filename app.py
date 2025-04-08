import streamlit as st
import PyPDF2
import tempfile
import os

st.set_page_config(
    page_title="PDF Upload App",
    page_icon="📄",
    layout="wide"
)

st.title("PDF Upload Application")
st.write("Upload your PDF files here")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # Read the PDF file
        with open(tmp_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            st.success(f"PDF uploaded successfully! Number of pages: {num_pages}")
            
            # Display basic PDF information
            st.subheader("PDF Information")
            st.write(f"File name: {uploaded_file.name}")
            st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")
            
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(tmp_file_path) 