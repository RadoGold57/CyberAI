import httpx
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def test_idor(urls):
    print("[+] Scanning for IDOR...")
    findings = []
    keywords = ["id", "user", "uid", "account", "profile"]
    fuzz_range = range(1, 10)

    for url in urls:
        if not any(k in url.lower() for k in keywords):
            continue

        try:
            parsed = urlparse(url)
            qs = parse_qs(parsed.query)

            for param in qs:
                if any(k in param.lower() for k in keywords):
                    for i in fuzz_range:
                        qs[param] = str(i)
                        new_query = urlencode(qs, doseq=True)
                        new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

                        r = httpx.get(new_url, timeout=10)
                        if r.status_code == 200 and "error" not in r.text.lower():
                            findings.append({
                                "url": new_url,
                                "type": "Potential IDOR",
                                "payload": f"{param}={i}",
                                "evidence": f"Access succeeded with modified ID {i}"
                            })
        except Exception:
            pass

    return findings
