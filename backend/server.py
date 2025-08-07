from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from rq import Queue
from redis import Redis
import uuid
import json
import os

from backend.tasks import run_scan_task
from backend.pipeline import run_scan

app = FastAPI(title="CyberAI Scanner")

redis_conn = Redis(host=os.getenv("REDIS_HOST", "localhost"),
                   port=int(os.getenv("REDIS_PORT", 6379)))
queue = Queue(connection=redis_conn)

class ScanRequest(BaseModel):
    target: str
    ai_payloads: bool = False
    concurrency: int = 30

@app.post("/scan")
async def scan(request: ScanRequest):
    findings = await run_scan(request.target, request.ai_payloads, request.concurrency)
    return {"target": request.target, "findings": findings}

@app.post("/queue/submit")
def submit_job(request: ScanRequest):
    job_id = str(uuid.uuid4())
    job = queue.enqueue(run_scan_task, request.target, request.ai_payloads, request.concurrency, job_id)
    return {"job_id": job_id, "status": "queued"}

@app.get("/queue/status/{job_id}")
def get_status(job_id: str):
    job = queue.fetch_job(job_id)
    if not job:
        return {"error": "Job not found"}
    return {"job_id": job_id, "status": job.get_status()}

@app.get("/queue/result/{job_id}")
def get_result(job_id: str):
    result_path = f"results/{job_id}.json"
    if not os.path.exists(result_path):
        return {"error": "No result found"}
    with open(result_path) as f:
        return json.load(f)
