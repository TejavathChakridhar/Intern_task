from pathlib import Path
import re
import sys
from io import StringIO

from fetch_ecourts import read_local_file, parse_cause_list_html, make_date_strings, main


def test_parse_sample_by_cnr():
    p = Path(__file__).parent / "fixtures" / "cause_list_sample.html"
    html = read_local_file(str(p))
    assert html is not None
    matches = parse_cause_list_html(html, search_cnr="MHDS1234567890", case_re=None, base_url="https://services.ecourts.gov.in")
    assert len(matches) == 1
    m = matches[0]
    assert m["serial"] == "1"
    assert "Court No. 1" in m["court"] or "Court No" in m["court"]
    assert m["pdf"] is not None


def test_parse_sample_by_case():
    p = Path(__file__).parent / "fixtures" / "cause_list_sample.html"
    html = read_local_file(str(p))
    pattern = re.compile(r"CIV 123 of 2024", re.I)
    matches = parse_cause_list_html(html, search_cnr=None, case_re=pattern, base_url=None)
    assert len(matches) == 1


def test_date_strings():
    """Test that make_date_strings returns today and tomorrow dates."""
    dates = make_date_strings()
    assert "today" in dates
    assert "tomorrow" in dates
    assert len(dates["today"]) == 10  # DD-MM-YYYY format
    assert len(dates["tomorrow"]) == 10


def test_cli_cnr_today():
    """Test CLI with CNR and --today flag."""
    fixture = Path(__file__).parent / "fixtures" / "cause_list_sample.html"
    argv = [
        "--cnr", "MHDS1234567890",
        "--cause-list-url", str(fixture),
        "--today",
        "--outdir", "test_outputs"
    ]
    # Should not raise exception
    try:
        main(argv)
    except SystemExit as e:
        # Exit code 0 is success
        assert e.code == 0 or e.code is None


def test_cli_causelist_download():
    """Test CLI with --causelist flag to download entire list."""
    fixture = Path(__file__).parent / "fixtures" / "cause_list_sample.html"
    argv = [
        "--causelist",
        "--cause-list-url", str(fixture),
        "--tomorrow",
        "--outdir", "test_outputs"
    ]
    try:
        main(argv)
    except SystemExit as e:
        assert e.code == 0 or e.code is None

