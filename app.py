import streamlit as st
import pandas as pd
import pdfplumber
import tempfile
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Invoice Comparison App",
    page_icon="📄",
    layout="wide"
)

st.title("AI-Powered Invoice Comparison Application")
st.write("Upload your PDF invoice and Master Data Excel file for AI-powered comparison")

# Function to extract complete text from PDF
def extract_pdf_text(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

# Function to extract structured data from PDF
def extract_pdf_data(pdf_path):
    data = []
    full_text = extract_pdf_text(pdf_path)
    
    # Store the complete text for display
    st.session_state['pdf_full_text'] = full_text
    
    # Try to extract structured data
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if any(char.isdigit() for char in line):
                        parts = line.split()
                        if len(parts) >= 4:
                            try:
                                item = ' '.join(parts[:-3])
                                quantity = float(parts[-3])
                                unit_price = float(parts[-2])
                                total = float(parts[-1])
                                data.append({
                                    'Item': item,
                                    'Quantity': quantity,
                                    'Unit Price': unit_price,
                                    'Total': total
                                })
                            except:
                                continue
    return pd.DataFrame(data)

# Function to compare data using OpenAI
def compare_data_with_ai(pdf_df, excel_df, pdf_text):
    # Convert dataframes to JSON for better context
    pdf_data = pdf_df.to_dict('records')
    excel_data = excel_df.to_dict('records')
    
    # Prepare the prompt for OpenAI
    prompt = f"""
    Compare the following invoice data with master data and identify any discrepancies:
    
    Complete PDF Text:
    {pdf_text}
    
    Extracted Structured Data from PDF:
    {json.dumps(pdf_data, indent=2)}
    
    Master Data:
    {json.dumps(excel_data, indent=2)}
    
    Please analyze and identify:
    1. Items present in invoice but not in master data
    2. Items present in master data but not in invoice
    3. Any discrepancies in all fields (Quantity, Unit Price, Subtotal, Discount, Tax, Total)
    4. Any potential data entry errors or formatting issues
    5. Any additional information from the PDF text that might be relevant
    
    Format your response as a JSON object with the following structure:
    {{
        "missing_in_master": [list of items missing in master data],
        "missing_in_invoice": [list of items missing in invoice],
        "discrepancies": [
            {{
                "item": "item name",
                "field": "field name",
                "invoice_value": "value in invoice",
                "master_value": "value in master data",
                "difference": "difference amount",
                "severity": "high/medium/low",
                "context": "additional context from PDF text"
            }}
        ],
        "summary": "overall summary of findings",
        "additional_notes": "any additional observations from the PDF text",
        "total_discrepancies": {{
            "high": number_of_high_severity_discrepancies,
            "medium": number_of_medium_severity_discrepancies,
            "low": number_of_low_severity_discrepancies,
            "total": total_number_of_discrepancies
        }}
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert in invoice verification and data comparison. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        
        # Get the content from the response
        content = response.choices[0].message.content
        
        # Validate that content is not empty
        if not content:
            st.error("Received empty response from AI")
            return None
            
        # Try to parse the JSON response
        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError as e:
            st.error(f"Error parsing AI response: {str(e)}")
            st.error(f"Raw response: {content}")
            return None
        
    except Exception as e:
        st.error(f"Error in AI comparison: {str(e)}")
        return None

# File uploaders
col1, col2 = st.columns(2)
with col1:
    uploaded_pdf = st.file_uploader("Upload PDF Invoice", type="pdf")
with col2:
    uploaded_excel = st.file_uploader("Upload Master Data Excel", type="xlsx")

if uploaded_pdf is not None and uploaded_excel is not None:
    # Process PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
        tmp_pdf.write(uploaded_pdf.getvalue())
        tmp_pdf_path = tmp_pdf.name
    
    # Process Excel
    excel_df = pd.read_excel(uploaded_excel)
    
    try:
        # Extract data from PDF
        pdf_df = extract_pdf_data(tmp_pdf_path)
        
        if not pdf_df.empty:
            # Compare data using AI
            with st.spinner("Analyzing data with AI..."):
                comparison_result = compare_data_with_ai(pdf_df, excel_df, st.session_state['pdf_full_text'])
            
            if comparison_result:
                # Display results
                st.subheader("AI Analysis Results")
                
                # Display summary
                st.write("### Summary")
                st.write(comparison_result["summary"])
                
                # Display additional notes
                if "additional_notes" in comparison_result:
                    st.write("### Additional Notes")
                    st.write(comparison_result["additional_notes"])
                
                # Display missing items
                if comparison_result["missing_in_master"]:
                    st.write("### Items Missing in Master Data")
                    st.write(comparison_result["missing_in_master"])
                
                # if comparison_result["missing_in_invoice"]:
                #     st.write("### Items Missing in Invoice")
                #     st.write(comparison_result["missing_in_invoice"])
                
                # Display discrepancies
                if comparison_result["discrepancies"]:
                    st.write("### Detailed Discrepancies")
                    
                    # Display total discrepancies summary
                    if "total_discrepancies" in comparison_result:
                        total = comparison_result["total_discrepancies"]
                        st.write(f"**Total Discrepancies:** {total['total']}")
                        st.write(f"- High Severity: {total['high']}")
                        st.write(f"- Medium Severity: {total['medium']}")
                        st.write(f"- Low Severity: {total['low']}")
                    
                    discrepancies_df = pd.DataFrame(comparison_result["discrepancies"])
                    st.dataframe(discrepancies_df)
                    
                    # Download button for discrepancies
                    csv = discrepancies_df.to_csv(index=False)
                    st.download_button(
                        label="Download Discrepancies as CSV",
                        data=csv,
                        file_name=f"discrepancies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.success("No discrepancies found between the PDF invoice and master data!")
                
                # Display complete PDF text
                st.subheader("Complete PDF Text")
                st.text(st.session_state['pdf_full_text'])
                
                st.subheader("Master Data")
                st.dataframe(excel_df)
                
                
            
        else:
            st.error("Could not extract data from the PDF file. Please check the PDF format.")
            
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
    finally:
        # Clean up temporary files
        os.unlink(tmp_pdf_path) 