import httpx

BYPASS_HEADERS = [
    {"X-Original-URL": "/"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forwarded-Host": "localhost"},
    {"X-Host": "localhost"}
]

async def check_forbidden_bypass(target, paths=None):
    """
    target: base URL (e.g. https://example.com)
    paths: list of paths to test (default: ['/'])
    """
    findings = []
    if paths is None:
        paths = ["/"]

    async with httpx.AsyncClient(follow_redirects=True, timeout=8) as client:
        for path in paths:
            url = target.rstrip("/") + path
            try:
                r = await client.get(url)
                if r.status_code == 403:
                    for headers in BYPASS_HEADERS:
                        rb = await client.get(url, headers=headers)
                        if rb.status_code in (200, 401):
                            findings.append({
                                "type": "403 Bypass",
                                "url": url,
                                "header": headers,
                                "status": rb.status_code
                            })
            except httpx.RequestError as e:
                print(f"[!] Request to {url} failed: {e}")
    return findings
