import httpx

payload = "<script>alert('CyberAI')</script>"

def test_xss(urls):
    findings = []
    print(f"[+] Testing {len(urls)} URLs for reflected XSS")

    for url in urls:
        if '=' not in url:
            continue
        test_url = url.replace('=', '=' + payload)
        try:
            r = httpx.get(test_url, timeout=10, follow_redirects=True)
            if payload in r.text:
                print(f"[!] Potential XSS found: {test_url}")
                findings.append({
                    "url": test_url,
                    "type": "Reflected XSS",
                    "payload": payload,
                    "evidence": "Payload reflected in response"
                })
        except Exception:
            pass
    return findings
