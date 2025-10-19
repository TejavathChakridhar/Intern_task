# 🚀 Quick Start Guide

## eCourts Case Checker - Get Started in 3 Minutes

### Step 1: Setup (First time only)

```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

### Step 2: Test with Sample Data

```powershell
# Search for a case by CNR (today's listings)
python fetch_ecourts.py --cnr "MHDS1234567890" --cause-list-url "tests/fixtures/cause_list_sample.html" --today

# Download entire cause list for tomorrow
python fetch_ecourts.py --causelist --cause-list-url "tests/fixtures/cause_list_sample.html" --tomorrow
```

**Expected Output:**
```
✅ Found 1 listing(s) for today (19-10-2025)
============================================================

--- Match 1 ---
Serial No.: 1
Court:      Court No. 1
PDF Link:   /docs/case_123.pdf
Details:    CIV 123 of 2024 - John vs Jane...
```

---

### Step 3: Use with Real eCourts Data

#### Get the Cause List URL:
1. Go to https://services.ecourts.gov.in/ecourtindia_v6/
2. Select your State → District → Court
3. Click **"Daily Cause List"**
4. Select date and court number
5. **Copy the URL** from your browser after the list loads

#### Search Your Case:

```powershell
# By CNR
python fetch_ecourts.py --cnr "YOUR_CNR_NUMBER" --cause-list-url "COPIED_URL" --today

# By Case Type/Number/Year
python fetch_ecourts.py --case CIV 123 2024 --cause-list-url "COPIED_URL" --tomorrow --download-pdf
```

---

### Step 4 (Optional): Start Web Interface

```powershell
# Install Flask (if not already)
pip install flask flask-cors

# Start API server
python api_server.py

# Open web interface
# Open web_frontend.html in your browser
```

Then visit: http://127.0.0.1:5000/health to verify API is running.

---

## Common Use Cases

### 📋 Case 1: Check if my case is listed today
```powershell
python fetch_ecourts.py --cnr "DLCA01234567890" --cause-list-url "https://services.ecourts.gov.in/.../causelist" --today
```

### 📋 Case 2: Download tomorrow's full cause list
```powershell
python fetch_ecourts.py --causelist --cause-list-url "https://services.ecourts.gov.in/.../causelist" --tomorrow
```

### 📋 Case 3: Search by case number and download PDF
```powershell
python fetch_ecourts.py --case CRLP 456 2023 --cause-list-url "URL" --today --download-pdf
```

### 📋 Case 4: Check using web interface
1. Start server: `python api_server.py`
2. Open `web_frontend.html` in browser
3. Fill form and click Search

---

## Output Files Location

All files saved to `outputs/` folder:
- `search_result_today_2025-10-19.json` - Search results
- `cause_list_tomorrow_2025-10-19.html` - Full HTML
- `cause_list_tomorrow_2025-10-19.txt` - Plain text
- `case_pdf_today_1.pdf` - Downloaded PDFs

---

## Troubleshooting

**❌ "No module named flask"**
```powershell
pip install flask flask-cors
```

**❌ "No listings found"**
- Check if the URL is correct
- Verify the date (cause lists are date-specific)
- Try `--verbose` flag for debugging

**❌ "Failed to fetch cause list"**
- Check internet connection
- URL might require login/session cookies
- Try downloading HTML manually and use local file

---

## Next Steps

✅ Read full documentation: `README.md`  
✅ Run tests: `python -m pytest -v`  
✅ Customize parsing: Edit `parse_cause_list_html()` in `fetch_ecourts.py`  
✅ Automate: Set up scheduled tasks (Windows Task Scheduler / cron)  

---

## Need Help?

1. Check `README.md` for detailed documentation
2. Run tests to verify setup: `.\.venv\Scripts\python.exe -m pytest -v`
3. Use `--verbose` flag for debugging
4. Check output files in `outputs/` folder

**Happy Court Listing! ⚖️**
