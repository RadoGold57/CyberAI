import httpx

ADMIN_PATHS = [
    "/admin", "/administrator", "/internal", "/dashboard", "/manage", "/controlpanel"
]

def find_admin_panels(base_url):
    findings = []
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    client = httpx.Client(follow_redirects=True, timeout=8)
    for path in ADMIN_PATHS:
        try:
            r = client.get(base_url.rstrip("/") + path)
            if r.status_code in [200, 401, 403]:
                findings.append({
                    "type": "Admin Page",
                    "url": base_url.rstrip("/") + path,
                    "status": r.status_code
                })
        except:
            pass
    client.close()
    return findings
