#!/usr/bin/env python3
"""
Simple eCourts cause-list checker.

Usage:
  - Provide a cause list URL via --cause-list-url (recommended) or point to a local HTML file with file:// path.
  - Search by --cnr OR by --type, --number, --year.
  - Optionally --download-pdf to fetch PDF links found for the case.
  - Optionally --download-cause-list to save the entire cause-list HTML and/or text.

This script is intentionally conservative: the eCourts website structure may change. If you have a specific cause-list URL pattern, pass it with --cause-list-url.

The included test fixture (tests/) demonstrates parsing a small sample HTML.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup


def fetch_url(url: str, timeout: int = 15) -> Optional[str]:
    headers = {
        "User-Agent": "ecourts-checker/1.0 (+https://example.com)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def read_local_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Failed to read local file {path}: {e}")
        return None


def guess_case_pattern(case_type: str, number: str, year: str) -> str:
    # Create a few possible textual patterns to search in cause-list rows
    patterns = [
        f"{case_type} {number} of {year}",
        f"{case_type} {number}/{year}",
        f"{case_type} {number} of {year}",
        f"{case_type}-{number}-{year}",
        f"{case_type} {number} {year}",
    ]
    return "|".join([re.escape(p) for p in patterns])


def find_in_row_text(text: str, cnr: Optional[str], case_re: Optional[re.Pattern]) -> bool:
    t = text.strip().lower()
    if cnr:
        if cnr.strip().lower() in t:
            return True
    if case_re:
        if case_re.search(t):
            return True
    return False


def parse_cause_list_html(html: str, search_cnr: Optional[str] = None, case_re: Optional[re.Pattern] = None, base_url: Optional[str] = None) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # Try to find rows: either <tr> in tables or <li> entries
    rows = soup.find_all("tr")
    if not rows:
        rows = []
        for ul in soup.find_all(["ul", "ol"]):
            rows.extend(ul.find_all("li"))

    for r in rows:
        text = r.get_text(separator=" ", strip=True)
        if not text:
            continue
        if find_in_row_text(text, search_cnr, case_re):
            # Extract serial number heuristically (first number-looking token)
            serial = None
            court = None
            pdf_link = None

            # serial: try first <td> or leading number
            first_td = r.find("td")
            if first_td:
                ft = first_td.get_text(strip=True)
                m = re.search(r"^(\d{1,4})\b", ft)
                if m:
                    serial = m.group(1)

            if not serial:
                m = re.search(r"^(\d{1,4})\b", text)
                if m:
                    serial = m.group(1)

            # court name: look for a cell with 'Court' or 'Court No' or a column after serial
            tds = r.find_all("td")
            if tds and len(tds) >= 2:
                # pick the second or third cell as likely court
                for cand in tds[1:4]:
                    cand_text = cand.get_text(strip=True)
                    if len(cand_text) > 0:
                        court = cand_text
                        break

            # fallback: search for 'Court' word in the row
            if not court:
                m = re.search(r"([A-Za-z .&'-]{4,}\bCourt\b.*?)(?:\b|$)", text, re.I)
                if m:
                    court = m.group(1)

            # pdf link
            a = r.find("a", href=True)
            if a:
                href = a["href"].strip()
                if href.lower().endswith(".pdf") or "pdf" in href.lower():
                    if base_url and href.startswith("/"):
                        pdf_link = base_url.rstrip("/") + href
                    else:
                        pdf_link = href

            results.append({
                "text": text,
                "serial": serial,
                "court": court,
                "pdf": pdf_link,
            })

    return results


def download_file(url: str, dest: str) -> bool:
    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(4096):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False


def save_json(obj, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def make_date_strings() -> Dict[str, str]:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    return {"today": today.strftime("%d-%m-%Y"), "tomorrow": tomorrow.strftime("%d-%m-%Y")}


def main(argv=None):
    p = argparse.ArgumentParser(description="Check eCourts cause list for a case (today/tomorrow)")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--cnr", help="CNR number to search for")
    grp.add_argument("--case", nargs=3, metavar=("TYPE", "NUMBER", "YEAR"), help="Case: TYPE NUMBER YEAR")
    grp.add_argument("--causelist", action="store_true", help="Download entire cause list (no case search)")

    p.add_argument("--cause-list-url", help="Cause-list URL or a local file path (file:///...) to fetch and search")
    p.add_argument("--today", action="store_true", help="Check only today's listings (default if neither --today nor --tomorrow specified)")
    p.add_argument("--tomorrow", action="store_true", help="Check tomorrow's listings")
    p.add_argument("--download-pdf", action="store_true", help="Download PDF if a link is found")
    p.add_argument("--outdir", default="outputs", help="Directory to save JSON and downloaded files")
    p.add_argument("--verbose", action="store_true")

    args = p.parse_args(argv)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    dates = make_date_strings()
    
    # Determine which date to check (default to today)
    check_today = args.today or (not args.tomorrow)
    check_tomorrow = args.tomorrow
    
    target_date = "today" if check_today else "tomorrow"
    target_date_str = dates["today"] if check_today else dates["tomorrow"]
    
    if args.verbose:
        print(f"Checking listings for: {target_date} ({target_date_str})")

    search_cnr = None
    case_re = None
    
    # If --causelist is used, we don't need case details
    if not args.causelist:
        if args.cnr:
            search_cnr = args.cnr.strip()
        else:
            typ, num, yr = args.case
            pattern = guess_case_pattern(typ, num, yr)
            case_re = re.compile(pattern, re.I)

    if not args.cause_list_url:
        print("No cause-list URL provided. This tool requires the cause-list URL from eCourts.\nSee README for how to obtain it.")
        print("You can also point to a local sample HTML (tests/fixtures/cause_list_sample.html) for testing.")
        sys.exit(1)

    # Handle file:// local file
    base_url = None
    is_local = False
    url = args.cause_list_url
    if url.startswith("file://"):
        is_local = True
        path = url[len("file://"):]
        html = read_local_file(path)
    elif url.startswith("/") or os.path.exists(url):
        is_local = True
        html = read_local_file(url)
    else:
        html = fetch_url(url)
        base_url = url

    if html is None:
        print("Failed to fetch cause list.")
        sys.exit(2)

    result = {
        "query": {
            "cnr": search_cnr, 
            "case_re": case_re.pattern if case_re else None, 
            "url": url,
            "date": target_date,
            "date_str": target_date_str
        }, 
        "matches": []
    }

    # If --causelist flag, save entire list and skip search
    if args.causelist:
        html_path = outdir / f"cause_list_{target_date}_{date.today().isoformat()}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        text_path = outdir / f"cause_list_{target_date}_{date.today().isoformat()}.txt"
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(BeautifulSoup(html, "html.parser").get_text(separator="\n"))
        
        out_json = outdir / f"cause_list_{target_date}_{date.today().isoformat()}.json"
        save_json({"date": target_date, "date_str": target_date_str, "url": url, "downloaded": True}, str(out_json))
        
        print(f"✅ Downloaded entire cause list for {target_date} ({target_date_str})")
        print(f"   HTML: {html_path}")
        print(f"   Text: {text_path}")
        print(f"   JSON: {out_json}")
        return

    matches = parse_cause_list_html(html, search_cnr=search_cnr, case_re=case_re, base_url=base_url)
    result["matches"] = matches

    out_json = outdir / f"search_result_{target_date}_{date.today().isoformat()}.json"
    save_json(result, str(out_json))
    print(f"Saved search results to {out_json}")

    if matches and args.download_pdf:
        for i, m in enumerate(matches, start=1):
            pdf = m.get("pdf")
            if pdf:
                fname = outdir / f"case_pdf_{target_date}_{i}.pdf"
                ok = download_file(pdf, str(fname))
                if ok:
                    print(f"Downloaded PDF to {fname}")
                else:
                    print(f"Failed to download PDF from {pdf}")
            else:
                print("No PDF link found for match:", m.get("text")[:120])

    # Print results to console
    if matches:
        print(f"\n{'='*60}")
        print(f"✅ Found {len(matches)} listing(s) for {target_date} ({target_date_str})")
        print(f"{'='*60}")
        for i, m in enumerate(matches, start=1):
            print(f"\n--- Match {i} ---")
            print(f"Serial No.: {m.get('serial') or 'N/A'}")
            print(f"Court:      {m.get('court') or 'N/A'}")
            print(f"PDF Link:   {m.get('pdf') or 'Not available'}")
            print(f"Details:    {m.get('text')[:200]}...")
    else:
        print(f"\n❌ No listings found for the query on {target_date} ({target_date_str}).")


if __name__ == "__main__":
    main()
