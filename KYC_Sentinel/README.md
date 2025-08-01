# KYC Sentinel

A GUI-based desktop application for KYC/AML compliance screening using the OpenSanctions API.

## Features

- **GUI-based Interface**: Clean, user-friendly Tkinter interface
- **Dual Processing Modes**:
  - Manual Mode: Individual name checking with instant results
  - Batch Mode: CSV bulk processing for multiple records
- **OpenSanctions Integration**: Real-time screening against global sanctions databases
- **Excel Export**: Automated results export with visual highlighting
- **Error Handling**: Robust error management for network issues and malformed data
- **Progress Tracking**: Real-time progress indicators for batch operations

## Requirements

- Python 3.8+
- Internet connection (for API access)
- Windows/Linux/macOS compatible

## Installation & Setup

### 🔧 Classic Setup (pip)

```bash
# Clone or download the project
cd KYC_Sentinel

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### 🧪 Modern Setup (uv - Recommended)

```bash
# Install uv if not already installed
pip install uv

# Clone or download the project
cd KYC_Sentinel

# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Run the application
python main.py
```

**Alternative uv method using pyproject.toml:**
```bash
uv venv
uv pip install .
python main.py
```

> **Note**: `uv` is faster than pip and supports virtualenv out of the box, making it ideal for modern Python development.

## Usage

### Manual Mode
1. Launch the application: `python main.py`
2. Select "Manual Mode"
3. Enter the person's details:
   - **Name**: Full name to check (required)
   - **DOB**: Date of birth in YYYY-MM-DD format (optional)
   - **CNIC**: National ID number (optional)
4. Click "Run KYC Check"
5. View results in the results panel
6. Excel file automatically saved to `/output/KYC_Results.xlsx`

### Batch Mode
1. Launch the application: `python main.py`
2. Select "Batch Mode (CSV)"
3. Click "Browse" and select your CSV file
4. Ensure your CSV has these columns: `Name`, `DOB`, `CNIC`
5. Click "Upload CSV & Run Bulk Check"
6. Monitor progress in real-time
7. View summary and check the output Excel file

### Sample CSV Format
```csv
Name,DOB,CNIC
John Smith,1985-03-15,12345-6789012-3
Jane Doe,1990-07-22,11111-2222233-4
```

## Output

Results are saved to `/output/KYC_Results.xlsx` with the following columns:
- **Name**: Person's name
- **DOB**: Date of birth
- **CNIC**: National ID
- **Status**: 
  - `Clear` - No sanctions matches found
  - `Match Found` - Potential sanctions match (highlighted in red)
  - `Error: [reason]` - Processing error

## API Information

This application uses the [OpenSanctions API](https://api.opensanctions.org/) for sanctions screening:
- **Endpoint**: `https://api.opensanctions.org/match`
- **Rate Limits**: Please be respectful of API usage
- **Data Sources**: Global sanctions, PEPs, and watchlists

## Building Executable

To create a standalone `.exe` file for Windows distribution:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable (see build_guide.txt for details)
pyinstaller --onefile --noconsole main.py

# Find executable in /dist/ folder
```

## Error Handling

The application handles various error scenarios:
- **Network Issues**: Shows popup when API is unreachable
- **Malformed CSV**: Validates required columns and data format
- **API Failures**: Graceful handling of API errors and timeouts
- **File Access**: Handles Excel export and file permission issues

## Project Structure

```
KYC_Sentinel/
│
├── main.py                 # Main application file
├── requirements.txt        # pip dependencies
├── pyproject.toml         # uv/modern Python project config
├── README.md              # This file
├── build_guide.txt        # PyInstaller build instructions
│
├── /input/
│   └── sample_input.csv   # Sample CSV for testing
│
├── /output/
│   └── (KYC_Results.xlsx) # Generated results
│
└── /assets/
    └── (optional icons)
```

## Troubleshooting

**Common Issues:**

1. **"No module named 'tkinter'"**: Install tkinter
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL
   sudo yum install tkinter
   ```

2. **API Connection Errors**: Check internet connection and firewall settings

3. **Excel Export Fails**: Ensure `/output/` directory exists and is writable

4. **CSV Import Issues**: Verify CSV has required columns: `Name`, `DOB`, `CNIC`

## License

This project is provided as-is for compliance and educational purposes. Please ensure compliance with OpenSanctions API terms of use.

## Support

For issues or questions:
1. Check the error messages in the application
2. Verify your CSV format matches the requirements
3. Ensure stable internet connection for API access

---

**Note**: This tool is designed for compliance screening purposes. Always verify results through official channels for critical decisions.