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


def save_json_report(findings, target):
    output_path = Path("results") / f"{target.replace('.', '_')}_report.json"
    formatted = []

    for f in findings:
        formatted.append({
            "host": target,
            "url": f.get("url", ""),
            "issue": f.get("type", ""),
            "payload": f.get("payload", ""),
            "evidence": f.get("evidence", ""),
        })

    output_path.write_text(json.dumps(formatted, indent=2))
    print(f"[+] JSON report saved: {output_path}")