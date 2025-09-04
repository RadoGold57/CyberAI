from fastapi import FastAPI, Query
from redis import Redis
from rq import Queue
import os

app = FastAPI(title="CyberAI API")

# Redis connection
redis_conn = Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)
queue = Queue("scans", connection=redis_conn)

@app.get("/scan")
def enqueue_scan(target: str = Query(..., description="Target domain or URL")):
    """
    Enqueue a scan for the given target.
    """
    job = queue.enqueue("backend.tasks.run_full_scan", target)
    return {
        "status": "queued",
        "job_id": job.id,
        "target": target
    }
