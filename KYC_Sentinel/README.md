# KYC Sentinel

A desktop application for KYC/AML compliance screening using the OpenSanctions API.

## Features

- **GUI-based application** with clean, modern interface
- **Dual operation modes:**
  - 🔹 **Manual Mode**: Single name screening with immediate results
  - 🔹 **Batch Mode**: CSV bulk processing for multiple records
- **OpenSanctions API integration** for comprehensive sanctions screening
- **Excel output** with color-coded results (red highlighting for matches)
- **Real-time progress tracking** with status updates
- **Error handling** for network issues, malformed data, and API failures
- **Offline executable** capability for Windows deployment

## Screenshots

The application features a professional interface with:
- Mode selection (Manual/Batch)
- Input fields for Name, DOB, and CNIC
- Progress bar and status updates
- Results display area
- Automatic Excel export

## Usage

### Quick Start

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Choose your mode:**
   - **Manual Mode**: Enter individual details and click "Run Check"
   - **Batch Mode**: Upload a CSV file and click "Upload CSV & Run Bulk Check"

3. **View results:**
   - Results appear in the application window
   - Excel file automatically saved to `/output/KYC_Results.xlsx`
   - Match Found entries are highlighted in red

### Manual Mode

1. Enter the person's name (required)
2. Optionally enter Date of Birth and CNIC
3. Click "Run Check"
4. View results in the results area
5. Excel file saved automatically

### Batch Mode

1. Prepare a CSV file with columns: `Name`, `DOB`, `CNIC`
2. Click "Browse CSV" to select your file
3. Click "Upload CSV & Run Bulk Check"
4. Monitor progress in real-time
5. Results saved to Excel when complete

### CSV Format

Your CSV file must include these exact column headers:
```csv
Name,DOB,CNIC
John Doe,01/01/1990,123456789012
Jane Smith,15/05/1985,234567890123
```

## Installation

### Classic Setup (pip)

1. **Install Python 3.8+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python main.py
   ```

### 🧪 Using UV (Optional Advanced Setup)

UV is a modern, fast Python package manager that's significantly faster than pip:

```bash
# Install uv if not already installed:
pip install uv

# Install dependencies
uv pip install -r requirements.txt

# Or, if using pyproject.toml:
uv venv
uv pip install
```

**Note:** `uv` is faster than pip and supports virtualenv out of the box.

## Building Executable

See `build_guide.txt` for detailed instructions on creating a standalone `.exe` file.

Quick build:
```bash
pyinstaller --onefile --noconsole main.py
```

## Output

Results are saved to `/output/KYC_Results.xlsx` with the following structure:

| Name | DOB | CNIC | Status |
|------|-----|------|--------|
| John Doe | 01/01/1990 | 123456789012 | Clear |
| Vladimir Putin | 07/10/1952 | 123456789012 | **Match Found** |

- **Clear**: No sanctions matches found
- **Match Found**: Potential sanctions match detected (highlighted in red)

## API Information

This application uses the OpenSanctions API:
- **Endpoint:** `https://api.opensanctions.org/match?q=<name>`
- **Rate Limiting:** Built-in delays to prevent API overload
- **Internet Required:** Active internet connection needed for screening

## Error Handling

The application gracefully handles:
- ❌ No internet connection
- ❌ API failures or timeouts
- ❌ Malformed CSV files
- ❌ Missing required columns
- ❌ Excel export failures
- ❌ Empty or invalid input data

Error messages are displayed via popup dialogs with clear explanations.

## System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, Linux
- **Internet:** Required for API access
- **Memory:** Minimum 512MB RAM
- **Storage:** 50MB free space

## Notes

- **Internet connection required** for sanctions screening
- **CSV files must use exact column names:** `Name`, `DOB`, `CNIC`
- **Large batch files** are processed with progress indicators
- **Results are automatically timestamped** in the Excel output
- **Application centers on screen** for optimal user experience

## Troubleshooting

### Common Issues

1. **"No internet connection"**
   - Check your network connection
   - Verify firewall settings allow Python/app internet access

2. **"CSV missing required columns"**
   - Ensure CSV has headers: `Name`, `DOB`, `CNIC`
   - Check for typos in column names

3. **"API request failed"**
   - Temporary API downtime - try again later
   - Check internet connectivity

4. **Excel file errors**
   - Ensure `/output/` directory is writable
   - Close any open Excel files with the same name

### Support

For technical issues:
1. Check error messages in the application
2. Verify all requirements are installed
3. Ensure proper CSV format for batch processing
4. Test with the provided `sample_input.csv`

## License

This project is open source and available under the MIT License.