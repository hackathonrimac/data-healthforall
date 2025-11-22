# CMP Doctor Data Crawler

A Python crawler to extract doctor data from the CMP (Colegio Médico del Perú) website structure.

## Features

- Extracts all specialties from the landing page
- Crawls doctor listings for each specialty
- Extracts detailed information for each doctor
- Handles multiple specialties per doctor
- Supports both local HTML files and live website crawling
- Exports data to CSV and JSON formats

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Using Local HTML Files (Recommended for Testing)

If you have local HTML files (`cmp.html`, `speciality-cmp.html`, `dr-cmp.html`):

```bash
python crawler.py --local
```

### Crawling Live Website

```bash
python crawler.py --base-url https://www.cmp.org.pe
```

### Advanced Options

```bash
# Process only first 5 specialties
python crawler.py --local --max 5

# Resume from specialty index 10
python crawler.py --local --start 10

# Custom delay between requests (for live crawling)
python crawler.py --delay 2.0

# Custom output filenames
python crawler.py --local --output-csv my_data.csv --output-json my_data.json
```

## Output Format

### CSV Output (`doctors_data.csv`)

Each row represents a doctor-specialty relationship. If a doctor has multiple specialties, there will be multiple rows.

Columns:
- `cmp`: Doctor's CMP ID
- `apellidos`: Last names
- `nombres`: First names
- `apellido_paterno`: Paternal last name
- `apellido_materno`: Maternal last name
- `status`: Status (e.g., "HÁBIL")
- `email`: Email address
- `consejo_regional`: Regional council
- `foto_url`: Photo URL
- `specialty`: Specialty name
- `specialty_id`: Specialty ID
- `registro`: Registration type
- `tipo`: Type
- `codigo`: Code
- `fecha`: Date

### JSON Output (`doctors_data.json`)

Structured JSON with all doctor information, including multiple registrations per doctor.

## Example Python Usage

```python
from crawler import CMPCrawler

# Create crawler instance
crawler = CMPCrawler(use_local_files=True)

# Parse specialties from landing page
specialties = crawler.parse_specialties('cmp.html')

# Process a specific specialty
specialty = specialties[0]
doctors = crawler.parse_doctors_from_specialty(specialty, 'speciality-cmp.html')

# Get details for a specific doctor
doctor = doctors[0]
detailed = crawler.parse_doctor_detail(doctor, 'dr-cmp.html')

# Or crawl everything
crawler.crawl_all(use_local_files=True, max_specialties=5)
crawler.save_to_csv('output.csv')
crawler.save_to_json('output.json')
```

## Data Structure

The final database structure will be:

```
Doctor 1 - Specialty 1
Doctor 1 - Specialty 2 (if doctor has multiple specialties)
Doctor 2 - Specialty 1
Doctor 3 - Specialty 1
...
```

Each doctor-specialty combination is stored as a separate row in the CSV, making it easy to query and analyze.

## Notes

- When using local files, the crawler will look for files in the current directory
- For live crawling, be respectful with delays to avoid overwhelming the server
- The crawler handles encoding issues and missing data gracefully
- Progress is logged to the console

## Troubleshooting

1. **File not found errors**: Make sure HTML files are in the same directory as the script
2. **Encoding errors**: The script handles UTF-8 encoding, but some special characters may need manual fixing
3. **Empty results**: Check that the HTML structure matches the expected format

