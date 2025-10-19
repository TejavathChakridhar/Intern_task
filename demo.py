#!/usr/bin/env python3
"""
Demo script showing various usage scenarios of the eCourts checker.
Run this to see examples of different features.
"""
import subprocess
import sys
from pathlib import Path

def run_cmd(description, cmd):
    print(f"\n{'='*70}")
    print(f"📌 {description}")
    print(f"{'='*70}")
    print(f"Command: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=False)
    print(f"\nExit code: {result.returncode}")
    return result.returncode

def main():
    python_exe = sys.executable
    fixture = "tests/fixtures/cause_list_sample.html"
    
    print("🎯 eCourts Checker - Feature Demonstration")
    print("=" * 70)
    
    demos = [
        {
            "desc": "Example 1: Search by CNR (today's listings)",
            "cmd": [python_exe, "fetch_ecourts.py", 
                    "--cnr", "MHDS1234567890",
                    "--cause-list-url", fixture,
                    "--today"]
        },
        {
            "desc": "Example 2: Search by Case Type/Number/Year (tomorrow)",
            "cmd": [python_exe, "fetch_ecourts.py",
                    "--case", "CIV", "123", "2024",
                    "--cause-list-url", fixture,
                    "--tomorrow"]
        },
        {
            "desc": "Example 3: Download entire cause list for today",
            "cmd": [python_exe, "fetch_ecourts.py",
                    "--causelist",
                    "--cause-list-url", fixture,
                    "--today"]
        },
        {
            "desc": "Example 4: Search with PDF download (will fail on relative URLs)",
            "cmd": [python_exe, "fetch_ecourts.py",
                    "--cnr", "MHDS1234567890",
                    "--cause-list-url", fixture,
                    "--download-pdf"]
        },
    ]
    
    for demo in demos:
        run_cmd(demo["desc"], demo["cmd"])
        input("\n⏸️  Press Enter to continue to next example...")
    
    print("\n" + "=" * 70)
    print("✅ Demo completed!")
    print("=" * 70)
    print("\nCheck the 'outputs/' folder for generated files:")
    
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        for f in sorted(outputs_dir.iterdir()):
            print(f"  📄 {f.name}")
    
    print("\n💡 Next steps:")
    print("  1. Get a real cause-list URL from eCourts website")
    print("  2. Replace fixture URL with real URL")
    print("  3. Run: python fetch_ecourts.py --cnr YOUR_CNR --cause-list-url YOUR_URL")
    print("\n📖 Read QUICKSTART.md for step-by-step guide")
    print("📖 Read README.md for full documentation")

if __name__ == "__main__":
    main()
