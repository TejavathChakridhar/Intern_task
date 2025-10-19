# eCourts Case Checker - Command Reference

## Quick Commands (Copy & Paste)

### Setup (First Time)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run Tests
```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

### CLI Examples

#### Search by CNR (Today)
```powershell
python fetch_ecourts.py --cnr "MHDS1234567890" --cause-list-url "tests/fixtures/cause_list_sample.html" --today
```

#### Search by CNR (Tomorrow)
```powershell
python fetch_ecourts.py --cnr "MHDS1234567890" --cause-list-url "tests/fixtures/cause_list_sample.html" --tomorrow
```

#### Search by Case Details
```powershell
python fetch_ecourts.py --case CIV 123 2024 --cause-list-url "tests/fixtures/cause_list_sample.html" --today
```

#### Download Entire Cause List
```powershell
python fetch_ecourts.py --causelist --cause-list-url "tests/fixtures/cause_list_sample.html" --today
```

#### Search with PDF Download
```powershell
python fetch_ecourts.py --cnr "MHDS1234567890" --cause-list-url "tests/fixtures/cause_list_sample.html" --download-pdf
```

### API Server

#### Start Server
```powershell
python api_server.py
```

#### Test Endpoints
```powershell
# Health check
curl http://127.0.0.1:5000/health

# Search by CNR
curl "http://127.0.0.1:5000/api/search?cnr=MHDS1234567890&url=tests/fixtures/cause_list_sample.html&date=today"

# Get cause list
curl "http://127.0.0.1:5000/api/causelist?url=tests/fixtures/cause_list_sample.html&date=today"
```

### Demo
```powershell
python demo.py
```

### View Output Files
```powershell
dir outputs
```

### Clean Output Files
```powershell
Remove-Item outputs\* -Force
```

---

## File Structure
```
.
├── fetch_ecourts.py         # Main CLI script
├── api_server.py            # REST API server
├── web_frontend.html        # Web UI
├── demo.py                  # Interactive demo
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
├── QUICKSTART.md           # Quick start guide
├── SUMMARY.md              # Project overview
├── COMMANDS.md             # This file
├── tests/
│   ├── test_parse.py
│   └── fixtures/
│       └── cause_list_sample.html
└── outputs/                # Generated files
```

---

## Help
```powershell
python fetch_ecourts.py --help
```
