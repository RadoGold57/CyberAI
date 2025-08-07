import re
import httpx

EXPOSURE_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "Slack Token": r"xox[baprs]-[0-9A-Za-z]{10,48}",
    "Private Key": r"-----BEGIN PRIVATE KEY-----",
    "JWT": r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"
}

def scan_info_exposure(urls):
    findings = []
    client = httpx.Client(follow_redirects=True, timeout=8)
    for url in urls:
        try:
            r = client.get(url)
            text = r.text
            for name, pattern in EXPOSURE_PATTERNS.items():
                for match in re.findall(pattern, text):
                    findings.append({
                        "type": "Info Exposure",
                        "subtype": name,
                        "url": url,
                        "match": match
                    })
        except:
            pass
    client.close()
    return findings
