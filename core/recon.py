import asyncio
import httpx

async def run_async_recon(target):
    findings = []
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            r = await client.get(target)
            findings.append({"type": "Recon", "url": target, "payload": "", "evidence": r.status_code})
        except Exception as e:
            findings.append({"type": "Recon Error", "url": target, "payload": "", "evidence": str(e)})

    return {"status": "ok", "target": target, "findings": findings}
