from datetime import datetime
import os

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
