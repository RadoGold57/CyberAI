from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import httpx

def mutate_idor(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    mutated_urls = []
    for param, vals in qs.items():
        for v in vals:
            if v.isdigit():
                qs[param] = [str(int(v) + 1)]
                mutated_urls.append(urlunparse(parsed._replace(query=urlencode(qs, doseq=True))))
                qs[param] = [str(int(v) - 1)]
                mutated_urls.append(urlunparse(parsed._replace(query=urlencode(qs, doseq=True))))
                qs[param] = [v]
    return mutated_urls

def scan_idor(urls):
    findings = []
    client = httpx.Client(follow_redirects=True, timeout=8)
    for url in urls:
        if "?" not in url:
            continue
        for mutant in mutate_idor(url):
            try:
                r = client.get(mutant)
                if r.status_code == 200 and len(r.content) > 50:
                    findings.append({
                        "type": "IDOR",
                        "url": mutant,
                        "status": r.status_code,
                        "length": len(r.content)
                    })
            except:
                pass
    client.close()
    return findings
