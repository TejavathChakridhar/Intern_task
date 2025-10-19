# 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    eCourts Case Checker                          │
│                       Architecture                               │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │     CLI      │  │   Web API    │  │  Web Browser │         │
│  │   Terminal   │  │   REST API   │  │  (Frontend)  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                      CORE LOGIC LAYER                           │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│   fetch_ecourts.py (Main Module)                               │
│   ┌──────────────────────────────────────────────────┐         │
│   │  ┌─────────────────┐  ┌─────────────────┐       │         │
│   │  │  Input Parser   │  │  Date Handler   │       │         │
│   │  │  (CNR/Case)     │  │  (Today/Tom.)   │       │         │
│   │  └────────┬────────┘  └────────┬────────┘       │         │
│   │           │                     │                │         │
│   │           └──────────┬──────────┘                │         │
│   │                      ▼                           │         │
│   │           ┌──────────────────────┐               │         │
│   │           │   HTML Fetcher       │               │         │
│   │           │   (requests lib)     │               │         │
│   │           └──────────┬───────────┘               │         │
│   │                      ▼                           │         │
│   │           ┌──────────────────────┐               │         │
│   │           │   HTML Parser        │               │         │
│   │           │   (BeautifulSoup)    │               │         │
│   │           └──────────┬───────────┘               │         │
│   │                      ▼                           │         │
│   │           ┌──────────────────────┐               │         │
│   │           │  Data Extractor      │               │         │
│   │           │  (Regex + Selectors) │               │         │
│   │           └──────────┬───────────┘               │         │
│   │                      ▼                           │         │
│   │           ┌──────────────────────┐               │         │
│   │           │   PDF Downloader     │               │         │
│   │           │   (Optional)         │               │         │
│   │           └──────────────────────┘               │         │
│   └──────────────────────────────────────────────────┘         │
│                                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│   │   Console    │  │  JSON Files  │  │  HTML/Text   │        │
│   │   Pretty     │  │  Structured  │  │  Cause Lists │        │
│   │   Output     │  │  Data        │  │              │        │
│   └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│   ┌──────────────┐                                             │
│   │  PDF Files   │                                             │
│   │  (Optional)  │                                             │
│   └──────────────┘                                             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                      DATA FLOW                                   │
└─────────────────────────────────────────────────────────────────┘

User Input (CNR/Case + URL + Date)
         ↓
  Validate & Parse
         ↓
  Fetch HTML from URL
         ↓
  Parse HTML (BeautifulSoup)
         ↓
  Extract Data (Regex + CSS Selectors)
    • Serial Number (first <td> or leading number)
    • Court Name (look for "Court" keyword)
    • PDF Link (find <a> tags with .pdf)
    • Row Text (full context)
         ↓
  Filter Matches (CNR or Case pattern)
         ↓
  Download PDFs (if --download-pdf)
         ↓
  Save Results
    • JSON: search_result_today_*.json
    • HTML: cause_list_today_*.html
    • Text: cause_list_today_*.txt
         ↓
  Display on Console
    • Pretty formatted
    • Serial, Court, PDF, Details


┌─────────────────────────────────────────────────────────────────┐
│                    API ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────┘

Web Browser (web_frontend.html)
         │
         │ HTTP Request
         ↓
   Flask Server (api_server.py)
         │
         ├─→ /health              → Health Check
         │
         ├─→ /api/search          → Search Case
         │      │
         │      ├─ Parse query params (cnr/type/number/year/url/date)
         │      ├─ Call fetch_ecourts functions
         │      └─ Return JSON response
         │
         └─→ /api/causelist       → Get Full List
                │
                ├─ Parse query params (url/date)
                ├─ Fetch & parse HTML
                └─ Return text + metadata


┌─────────────────────────────────────────────────────────────────┐
│                    FILE STRUCTURE                                │
└─────────────────────────────────────────────────────────────────┘

.
├── Core Scripts
│   ├── fetch_ecourts.py       (CLI + Core Logic - 300+ lines)
│   ├── api_server.py          (REST API - Flask)
│   └── demo.py                (Interactive Demo)
│
├── Frontend
│   └── web_frontend.html      (Web UI - Modern Design)
│
├── Documentation
│   ├── README.md              (Full Docs - 200+ lines)
│   ├── QUICKSTART.md          (Quick Start - Step by Step)
│   ├── SUMMARY.md             (Project Overview)
│   ├── COMMANDS.md            (Command Reference)
│   └── ARCHITECTURE.md        (This File)
│
├── Tests
│   ├── tests/test_parse.py    (5 Test Cases)
│   └── tests/fixtures/        (Sample HTML)
│
├── Config
│   └── requirements.txt       (Dependencies)
│
└── Output (Generated)
    └── outputs/               (JSON/HTML/Text/PDF)


┌─────────────────────────────────────────────────────────────────┐
│                   PARSING STRATEGY                               │
└─────────────────────────────────────────────────────────────────┘

HTML Structure Detection:
┌──────────────────────────┐
│  Try <tr> in <table>     │ ← Primary method
└────────┬─────────────────┘
         │ If no rows found
         ↓
┌──────────────────────────┐
│  Try <li> in <ul>/<ol>   │ ← Fallback method
└────────┬─────────────────┘
         │
         ↓
For each row:
┌──────────────────────────────────────────────┐
│  1. Get full text                            │
│  2. Check if matches CNR or Case pattern     │
│  3. Extract:                                 │
│     • Serial: First <td> or leading number   │
│     • Court: Look for "Court" keyword        │
│     • PDF: Find <a href="*.pdf">             │
│  4. Add to matches if found                  │
└──────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                  DEPLOYMENT OPTIONS                              │
└─────────────────────────────────────────────────────────────────┘

Option 1: Local CLI
  • Run on your PC
  • Manual execution
  • Best for: Personal use

Option 2: Scheduled Task
  • Windows Task Scheduler
  • Auto-check daily
  • Best for: Regular monitoring

Option 3: Web Server
  • Deploy Flask API
  • Access from anywhere
  • Best for: Team use

Option 4: Cloud Function
  • AWS Lambda / Azure Functions
  • Serverless
  • Best for: Scalability


┌─────────────────────────────────────────────────────────────────┐
│                    CUSTOMIZATION POINTS                          │
└─────────────────────────────────────────────────────────────────┘

1. HTML Parsing (parse_cause_list_html)
   • Adjust CSS selectors
   • Change regex patterns
   • Add new extraction fields

2. Case Pattern Matching (guess_case_pattern)
   • Add more pattern variations
   • Support regional formats

3. PDF Download Logic (download_file)
   • Add authentication
   • Handle redirects
   • Support different file types

4. Date Handling (make_date_strings)
   • Parse dates from HTML
   • Support different date formats
   • Add date range queries

5. API Endpoints (api_server.py)
   • Add authentication
   • Rate limiting
   • Caching


┌─────────────────────────────────────────────────────────────────┐
│                   TECHNOLOGY STACK                               │
└─────────────────────────────────────────────────────────────────┘

Backend:
  • Python 3.11+
  • BeautifulSoup4 (HTML parsing)
  • Requests (HTTP client)
  • Pathlib (File handling)
  • Re (Regular expressions)

API:
  • Flask (Web framework)
  • Flask-CORS (Cross-origin)

Testing:
  • Pytest (Test framework)

Frontend:
  • HTML5
  • CSS3 (Gradients, Flexbox)
  • Vanilla JavaScript (Fetch API)
