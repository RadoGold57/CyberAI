import httpx
import re

def scan_for_secrets(urls):
    print("[+] Scanning for sensitive information leakage...")
    findings = []
    secret_regex = {
        "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
        "AWS Access Key": r"AKIA[0-9A-Z]{16}",
        "JWT": r"eyJ[A-Za-z0-9_-]+?\.[A-Za-z0-9._-]+?\.[A-Za-z0-9._-]+"
    }

    for url in urls:
        try:
            r = httpx.get(url, timeout=10)
            for name, regex in secret_regex.items():
                matches = re.findall(regex, r.text)
                for match in matches:
                    findings.append({
                        "url": url,
                        "type": f"Sensitive Info: {name}",
                        "payload": match,
                        "evidence": "Pattern matched in response"
                    })
        except Exception:
            pass

    return findings
