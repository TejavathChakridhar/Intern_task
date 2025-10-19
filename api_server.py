#!/usr/bin/env python3
"""
Simple Flask API for eCourts cause list checking.

Endpoints:
  GET  /api/search?cnr=...&url=...&date=today
  GET  /api/search?type=...&number=...&year=...&url=...&date=tomorrow
  GET  /api/causelist?url=...&date=today
  GET  /health

Install: pip install flask flask-cors
Run:     python api_server.py
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import date, timedelta

from fetch_ecourts import (
    fetch_url, read_local_file, parse_cause_list_html,
    guess_case_pattern, make_date_strings
)

app = Flask(__name__)
CORS(app)  # Enable CORS for web frontend


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "ecourts-api", "version": "1.0"})


@app.route('/api/search', methods=['GET'])
def search_case():
    """
    Search for a case in cause list.
    Query params:
      - cnr: CNR number (OR)
      - type, number, year: Case details
      - url: Cause list URL (required)
      - date: 'today' or 'tomorrow' (default: today)
    """
    cnr = request.args.get('cnr')
    case_type = request.args.get('type')
    case_number = request.args.get('number')
    case_year = request.args.get('year')
    url = request.args.get('url')
    date_param = request.args.get('date', 'today').lower()

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    if not cnr and not (case_type and case_number and case_year):
        return jsonify({"error": "Provide either 'cnr' or 'type'+'number'+'year'"}), 400

    dates = make_date_strings()
    if date_param not in ['today', 'tomorrow']:
        return jsonify({"error": "date must be 'today' or 'tomorrow'"}), 400

    target_date_str = dates[date_param]

    # Fetch HTML
    if url.startswith("file://") or url.startswith("/"):
        html = read_local_file(url.replace("file://", ""))
    else:
        html = fetch_url(url)

    if not html:
        return jsonify({"error": "Failed to fetch cause list"}), 500

    # Parse
    search_cnr = cnr.strip() if cnr else None
    case_re = None
    if not search_cnr:
        pattern = guess_case_pattern(case_type, case_number, case_year)
        case_re = re.compile(pattern, re.I)

    matches = parse_cause_list_html(html, search_cnr=search_cnr, case_re=case_re, base_url=url)

    return jsonify({
        "date": date_param,
        "date_str": target_date_str,
        "query": {
            "cnr": search_cnr,
            "case": f"{case_type} {case_number}/{case_year}" if case_type else None
        },
        "matches": matches,
        "count": len(matches)
    })


@app.route('/api/causelist', methods=['GET'])
def download_causelist():
    """
    Get entire cause list text.
    Query params:
      - url: Cause list URL (required)
      - date: 'today' or 'tomorrow' (default: today)
    """
    url = request.args.get('url')
    date_param = request.args.get('date', 'today').lower()

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    dates = make_date_strings()
    if date_param not in ['today', 'tomorrow']:
        return jsonify({"error": "date must be 'today' or 'tomorrow'"}), 400

    target_date_str = dates[date_param]

    # Fetch HTML
    if url.startswith("file://") or url.startswith("/"):
        html = read_local_file(url.replace("file://", ""))
    else:
        html = fetch_url(url)

    if not html:
        return jsonify({"error": "Failed to fetch cause list"}), 500

    from bs4 import BeautifulSoup
    text = BeautifulSoup(html, "html.parser").get_text(separator="\n")

    return jsonify({
        "date": date_param,
        "date_str": target_date_str,
        "url": url,
        "text": text,
        "html_length": len(html)
    })


if __name__ == '__main__':
    print("🚀 Starting eCourts API server...")
    print("   Health check: http://127.0.0.1:5000/health")
    print("   Search API:   http://127.0.0.1:5000/api/search?cnr=XXX&url=...")
    print("   Cause list:   http://127.0.0.1:5000/api/causelist?url=...")
    app.run(debug=True, host='0.0.0.0', port=5000)
