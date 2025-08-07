import httpx

BYPASS_HEADERS = [
    {"X-Original-URL": "/"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forwarded-Host": "localhost"},
    {"X-Host": "localhost"}
]

def check_403_bypass(urls):
    findings = []
    client = httpx.Client(follow_redirects=True, timeout=8)
    for url in urls:
        try:
            r = client.get(url)
            if r.status_code == 403:
                for headers in BYPASS_HEADERS:
                    rb = client.get(url, headers=headers)
                    if rb.status_code in [200, 401]:
                        findings.append({
                            "type": "403 Bypass",
                            "url": url,
                            "header": headers,
                            "status": rb.status_code
                        })
        except:
            pass
    client.close()
    return findings

