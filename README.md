# eCourts Cause-List Checker

This Python CLI and API fetches/parses eCourts cause-list HTML and searches for cases by CNR or (Type, Number, Year). It supports checking **today's** or **tomorrow's** listings, downloading PDFs, and saving entire cause lists.

## Features ✨

✅ Search by **CNR** or **Case Type/Number/Year**  
✅ Check listings for **today** or **tomorrow**  
✅ Extract **serial number**, **court name**, and **PDF links**  
✅ Download **case PDFs** automatically  
✅ Download **entire cause list** (HTML + text + JSON)  
✅ **REST API** for web/mobile integration  

---

## Installation

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## CLI Usage

### 1. Search for a case (CNR) - Today's listings

```powershell
python fetch_ecourts.py --cnr "MHDS1234567890" --cause-list-url "tests/fixtures/cause_list_sample.html" --today
```

### 2. Search for a case (Type/Number/Year) - Tomorrow's listings

```powershell
python fetch_ecourts.py --case CIV 123 2024 --cause-list-url "https://services.ecourts.gov.in/.../cause_list.html" --tomorrow --download-pdf
```

### 3. Download entire cause list for today

```powershell
python fetch_ecourts.py --causelist --cause-list-url "tests/fixtures/cause_list_sample.html" --today --outdir outputs
```

### 4. Test with local fixture

```powershell
python fetch_ecourts.py --cnr "MHDS1234567890" --cause-list-url "tests/fixtures/cause_list_sample.html"
```

---

## CLI Options

```
--cnr CNR                  Search by CNR number
--case TYPE NUM YEAR       Search by case details (e.g., --case CIV 123 2024)
--causelist                Download entire cause list (no search)

--cause-list-url URL       URL or local file path to cause list HTML (required)
--today                    Check today's listings (default)
--tomorrow                 Check tomorrow's listings
--download-pdf             Download case PDFs if available
--outdir DIR               Output directory (default: outputs/)
--verbose                  Verbose output
```

---

## Web API Usage

### Start the API server

```powershell
python api_server.py
```

Server runs at: `http://127.0.0.1:5000`

### API Endpoints

#### 1. Health Check
```
GET /health
```
Response: `{"status": "ok", "service": "ecourts-api"}`

#### 2. Search for a case
```
GET /api/search?cnr=MHDS1234567890&url=tests/fixtures/cause_list_sample.html&date=today
GET /api/search?type=CIV&number=123&year=2024&url=https://...&date=tomorrow
```

Response:
```json
{
  "date": "today",
  "date_str": "19-10-2025",
  "query": {"cnr": "MHDS1234567890"},
  "matches": [
    {
      "serial": "1",
      "court": "Court No. 1",
      "pdf": "/docs/case_123.pdf",
      "text": "CIV 123 of 2024 - John vs Jane..."
    }
  ],
  "count": 1
}
```

#### 3. Get entire cause list
```
GET /api/causelist?url=tests/fixtures/cause_list_sample.html&date=today
```

Response:
```json
{
  "date": "today",
  "date_str": "19-10-2025",
  "url": "...",
  "text": "Cause List - 01-01-2025\n...",
  "html_length": 1234
}
```

---

## Output Files

All outputs saved to `outputs/` directory (or custom `--outdir`):

- `search_result_today_2025-10-19.json` - Search results with matches
- `cause_list_today_2025-10-19.html` - Full HTML (when using `--causelist`)
- `cause_list_today_2025-10-19.txt` - Plain text version
- `case_pdf_today_1.pdf` - Downloaded case PDFs (when using `--download-pdf`)

---

## Running Tests

```powershell
# Run all tests
.\.venv\Scripts\python.exe -m pytest -v

# Or activate venv first
.\.venv\Scripts\Activate.ps1
python -m pytest -v
```

---

## Notes & Assumptions

⚠️ **Important:** The eCourts website structure varies by court. This tool uses heuristics to parse HTML tables/lists.

- You **must provide the cause-list URL** (the script doesn't auto-navigate the eCourts site)
- Date filtering (`--today`/`--tomorrow`) is based on your system date
- PDF links are extracted if found in the HTML; adjust selectors in `parse_cause_list_html()` if needed
- For production use, you may need to:
  - Reverse-engineer specific court's POST endpoints
  - Handle CAPTCHA/session cookies
  - Add retry logic and rate limiting

---

## Customization

To adapt parsing for a specific court's HTML format:
1. Download a sample cause list HTML from that court
2. Adjust selectors in `parse_cause_list_html()` function in `fetch_ecourts.py`
3. Add test cases in `tests/test_parse.py`

---

## Examples for Real Usage

### Get cause list URL from eCourts:
1. Go to https://services.ecourts.gov.in/ecourtindia_v6/
2. Navigate to your state/district court
3. Click "Daily Cause List" 
4. Select date and court
5. Copy the URL from the result page
6. Use that URL with `--cause-list-url`

### Quick test workflow:
```powershell
# 1. Search for your case today
python fetch_ecourts.py --cnr "YOUR_CNR_HERE" --cause-list-url "YOUR_URL" --today

# 2. If found, download PDF
python fetch_ecourts.py --cnr "YOUR_CNR_HERE" --cause-list-url "YOUR_URL" --download-pdf

# 3. Download full cause list
python fetch_ecourts.py --causelist --cause-list-url "YOUR_URL" --today
```

---

## Troubleshooting

**Q: Tests fail with "No module named pytest"**  
A: Activate venv first: `.\.venv\Scripts\Activate.ps1` or use `.\.venv\Scripts\python.exe -m pytest`

**Q: API gives import errors**  
A: Install API dependencies: `pip install flask flask-cors`

**Q: No matches found but case exists**  
A: The HTML structure may differ. Try `--verbose` and check the saved HTML/text files to debug parsing logic.

**Q: How to get the cause-list URL?**  
A: Navigate to the eCourts website, select date/court, and copy the URL after the list loads. Each court may have different URL patterns.

---

## License

MIT - Use freely, modify as needed.
