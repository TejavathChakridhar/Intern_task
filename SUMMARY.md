# ✅ Project Summary: eCourts Case Checker

## 🎯 What This Tool Does

A complete Python solution for checking court case listings from the eCourts India website.

### Key Features Implemented ✨

✅ **Search by CNR or Case Details** (Type/Number/Year)  
✅ **Check Today's or Tomorrow's Listings** with `--today` / `--tomorrow` flags  
✅ **Extract Serial Number, Court Name, PDF Links**  
✅ **Download Case PDFs** automatically  
✅ **Download Entire Cause Lists** (HTML + Text + JSON)  
✅ **REST API Server** for web/mobile integration  
✅ **Web Frontend** with beautiful UI  
✅ **Comprehensive Tests** (5 test cases, all passing)  

---

## 📁 Files Created

### Core Files
- **`fetch_ecourts.py`** - Main CLI script (300+ lines)
- **`api_server.py`** - Flask REST API server
- **`web_frontend.html`** - Web interface with beautiful UI

### Documentation
- **`README.md`** - Complete documentation (200+ lines)
- **`QUICKSTART.md`** - Step-by-step quick start guide
- **`requirements.txt`** - Python dependencies

### Tests
- **`tests/test_parse.py`** - 5 test cases (all passing ✅)
- **`tests/fixtures/cause_list_sample.html`** - Sample HTML for testing

### Demos
- **`demo.py`** - Interactive demo of all features

---

## 🚀 Quick Start

```powershell
# 1. Setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Test
python fetch_ecourts.py --cnr "MHDS1234567890" --cause-list-url "tests/fixtures/cause_list_sample.html" --today

# 3. Run tests
python -m pytest -v
```

---

## 💻 CLI Usage Examples

### Search by CNR (Today)
```powershell
python fetch_ecourts.py --cnr "DLCA01234567890" --cause-list-url "URL" --today
```

### Search by Case Details (Tomorrow)
```powershell
python fetch_ecourts.py --case CIV 123 2024 --cause-list-url "URL" --tomorrow --download-pdf
```

### Download Full Cause List
```powershell
python fetch_ecourts.py --causelist --cause-list-url "URL" --today
```

---

## 🌐 Web API Usage

### Start Server
```powershell
python api_server.py
```

### API Endpoints

**Health Check:**
```
GET http://127.0.0.1:5000/health
```

**Search Case:**
```
GET http://127.0.0.1:5000/api/search?cnr=XXX&url=...&date=today
GET http://127.0.0.1:5000/api/search?type=CIV&number=123&year=2024&url=...&date=tomorrow
```

**Get Cause List:**
```
GET http://127.0.0.1:5000/api/causelist?url=...&date=today
```

### Web Interface
1. Start API: `python api_server.py`
2. Open `web_frontend.html` in browser
3. Fill form and search!

---

## 📊 Test Results

```
====================================== test session starts ======================================
collected 5 items

tests/test_parse.py::test_parse_sample_by_cnr PASSED                                       [ 20%]
tests/test_parse.py::test_parse_sample_by_case PASSED                                      [ 40%]
tests/test_parse.py::test_date_strings PASSED                                              [ 60%]
tests/test_parse.py::test_cli_cnr_today PASSED                                             [ 80%]
tests/test_parse.py::test_cli_causelist_download PASSED                                    [100%]

======================================= 5 passed in 0.30s =======================================
```

---

## 📦 Output Files

All results saved to `outputs/` directory:

```
outputs/
├── search_result_today_2025-10-19.json      # Search results
├── search_result_tomorrow_2025-10-19.json   # Tomorrow's results
├── cause_list_today_2025-10-19.html         # Full HTML
├── cause_list_today_2025-10-19.txt          # Plain text
├── cause_list_today_2025-10-19.json         # Metadata
└── case_pdf_today_1.pdf                     # Downloaded PDFs
```

---

## 🎨 Features Breakdown

### CLI Features
- ✅ `--cnr` - Search by CNR number
- ✅ `--case TYPE NUM YEAR` - Search by case details
- ✅ `--causelist` - Download entire list (no search)
- ✅ `--today` - Check today's listings (default)
- ✅ `--tomorrow` - Check tomorrow's listings
- ✅ `--download-pdf` - Auto-download case PDFs
- ✅ `--outdir` - Custom output directory
- ✅ `--verbose` - Detailed logging

### API Features
- ✅ RESTful endpoints
- ✅ CORS enabled
- ✅ JSON responses
- ✅ Error handling
- ✅ Health check endpoint

### Web UI Features
- ✅ Beautiful gradient design
- ✅ CNR or Case detail search
- ✅ Today/Tomorrow selection
- ✅ Loading spinner
- ✅ Responsive layout
- ✅ Match cards with all details

---

## 🔧 Technical Details

### Technologies Used
- **Python 3.11+**
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **Flask** - Web framework
- **Pytest** - Testing framework

### Architecture
```
User Input (CLI/API/Web)
         ↓
   fetch_ecourts.py (Core Logic)
         ↓
   HTML Parsing (BeautifulSoup)
         ↓
   Data Extraction (Regex + Selectors)
         ↓
   Output (JSON/Console/Files)
```

---

## ⚠️ Important Notes

### Limitations
- Requires cause-list URL (doesn't auto-navigate eCourts site)
- HTML structure varies by court (may need customization)
- PDF download works only with absolute URLs or proper base URL
- Date filtering based on system date (not parsed from HTML)

### Customization Needed For
- Specific court HTML structures
- Different table/list formats
- Session/cookie-based authentication
- CAPTCHA handling

---

## 🎯 How to Get Real eCourts URLs

1. Visit: https://services.ecourts.gov.in/ecourtindia_v6/
2. Navigate: State → District → Court
3. Click: "Daily Cause List"
4. Select: Date and Court Number
5. Copy: URL from browser after list loads
6. Use: That URL with `--cause-list-url` parameter

---

## 📚 Documentation Structure

```
.
├── README.md           # Full documentation (all features)
├── QUICKSTART.md       # Quick start guide (3 minutes)
├── SUMMARY.md          # This file (project overview)
├── fetch_ecourts.py    # Main CLI script
├── api_server.py       # REST API server
├── web_frontend.html   # Web interface
├── demo.py             # Interactive demo
├── requirements.txt    # Dependencies
└── tests/
    ├── test_parse.py           # Test cases
    └── fixtures/
        └── cause_list_sample.html  # Sample data
```

---

## 🚦 Next Steps

### For Basic Usage:
1. Read `QUICKSTART.md`
2. Test with sample data
3. Get real eCourts URL
4. Run your first search

### For Advanced Usage:
1. Read full `README.md`
2. Customize parsing logic
3. Set up API server
4. Build automation scripts

### For Development:
1. Study `fetch_ecourts.py`
2. Adjust `parse_cause_list_html()` for your court
3. Add more test cases
4. Contribute improvements

---

## ✅ All Requirements Met

| Requirement | Status | Implementation |
|------------|--------|----------------|
| Input CNR/Case details | ✅ Done | `--cnr` or `--case` flags |
| Check today/tomorrow | ✅ Done | `--today` / `--tomorrow` flags |
| Show serial & court | ✅ Done | Extracted in `parse_cause_list_html()` |
| Download case PDF | ✅ Done | `--download-pdf` flag |
| Download cause list | ✅ Done | `--causelist` flag |
| Console output | ✅ Done | Pretty formatted with emojis |
| Save JSON/text files | ✅ Done | Multiple formats in `outputs/` |
| CLI options | ✅ Done | 8+ flags implemented |
| Web/API interface | ✅ Done | Flask API + HTML frontend |

---

## 🎉 Success Metrics

✅ **All 5 tests passing**  
✅ **Zero import errors**  
✅ **Clean console output**  
✅ **Multiple output formats**  
✅ **Comprehensive documentation**  
✅ **Web interface included**  
✅ **API server included**  
✅ **Demo script included**  

---

## 📞 Support

- Check `README.md` for detailed docs
- Check `QUICKSTART.md` for quick help
- Run `python demo.py` to see examples
- Run tests: `python -m pytest -v`

---

**Built with ❤️ for Indian Legal System**  
**Version 1.0 - October 2025**
