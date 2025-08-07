from datetime import datetime
import os
import json
from pathlib import Path

def write_markdown_report(findings, target):
    os.makedirs("results", exist_ok=True)
    fname = f"results/{target.replace('.', '_')}_report.md"
    with open(fname, 'w') as f:
        f.write(f"# CyberAI Vulnerability Report\n")
        f.write(f"**Target**: {target}\n")
        f.write(f"**Date**: {datetime.now()}\n\n")
        for vuln in findings:
            f.write(f"## {vuln['type']}\n")
            f.write(f"- URL: `{vuln['url']}`\n")
            f.write(f"- Payload: `{vuln['payload']}`\n")
            f.write(f"- Evidence: {vuln['evidence']}`\n\n")
    print(f"[+] Report written to {fname}")


def save_burp_json(findings, target):
    """
    Save findings in Burp-compatible JSON format.
    """
    # Ensure results directory exists
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Remove protocol and any non-alphanumeric characters from target
    safe_target = target.replace("http://", "").replace("https://", "").replace("/", "_")
    safe_target = safe_target.replace(":", "_").replace(".", "_")

    output_path = results_dir / f"{safe_target}_burp.json"

    # Burp format is usually an array of issues
    burp_issues = []
    for f in findings:
        burp_issues.append({
            "type": f.get("type", ""),
            "host": target,
            "path": f.get("url", ""),
            "confidence": "Firm",
            "severity": "High",
            "request": f.get("payload", ""),
            "response": f.get("evidence", "")
        })

    output_path.write_text(json.dumps(burp_issues, indent=2))
    print(f"[+] Burp JSON report saved: {output_path}")

