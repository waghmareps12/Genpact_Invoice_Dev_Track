# AI-Powered Invoice Verification System

![Project Logo](images/project_logo.png)

A Streamlit-based application that automates the comparison of PDF invoices with master data in Excel files using AI-powered analysis.

## Features

- 📄 PDF invoice data extraction
- 📊 Excel master data comparison
- 🤖 AI-powered discrepancy detection
- 📈 Detailed discrepancy reporting
- 📥 Export functionality
- 🎯 Severity-based classification
- 📝 Contextual analysis

## Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/invoice-verification-system.git
cd invoice-verification-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Upload your files:
   - Upload a PDF invoice file
   - Upload the master data Excel file

3. View the results:
   - Summary of discrepancies
   - Detailed item-by-item comparison
   - Severity classification
   - Additional context and notes

4. Export results:
   - Download discrepancy report as CSV
   - View complete analysis in the interface

## Project Structure

```
invoice-verification-system/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
└── images/               # Screenshots and assets
    ├── input_interface.png
    ├── results_display.png
    └── detailed_analysis.png
```

## Data Format Requirements

### PDF Invoice
The application expects PDF invoices with the following information:
- Item names
- Quantities
- Unit prices
- Total amounts

### Master Data Excel
The Excel file should contain the following columns:
- Item
- Quantity
- Unit Price
- Subtotal
- Discount (if applicable)
- Tax (if applicable)
- Total

## Troubleshooting

### Common Issues

1. **PDF Parsing Errors**
   - Ensure the PDF is not password protected
   - Check if the PDF contains text (not scanned images)
   - Verify the PDF format matches the expected structure

2. **API Key Issues**
   - Verify the API key in the .env file
   - Check if the key has sufficient credits
   - Ensure the key has access to GPT-4

3. **Excel Format Issues**
   - Verify column names match the expected format
   - Check for data type consistency
   - Ensure no merged cells or special formatting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit for the web application framework
- All contributors and users of this project

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

*Note: This README will be updated as the project evolves. Please check back for the latest information.* 