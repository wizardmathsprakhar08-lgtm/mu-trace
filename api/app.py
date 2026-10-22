import os
import threading
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.config import settings
from core.schema import FullReport
from orchestrator import ResearchReportOrchestrator
from data.seed_data import COMPANIES_SEED

app = FastAPI(
    title="mu-trace - Institutional Research API",
    description="Automated Institutional Investment Research Report Generator with Claim-Level Provenance",
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

job_tracker: Dict[str, Dict[str, Any]] = {}
report_cache: Dict[str, FullReport] = {}
orchestrator = ResearchReportOrchestrator()

class GenerateRequest(BaseModel):
    ticker: str
    focus: str = "comprehensive"

@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME, "version": settings.VERSION}

@app.get("/api/v1/entities")
def list_entities():
    return [
        {
            "ticker": c["ticker"],
            "name": c["name"],
            "sector": c["sector"],
            "industry": c["industry"],
            "is_bank": c.get("is_bank", False),
            "currency": c["currency"]
        }
        for c in COMPANIES_SEED
    ]

def _run_report_task(job_id: str, ticker: str, focus: str):
    job_tracker[job_id]["status"] = "RUNNING"
    try:
        def on_progress(stage: str, pct: int, meta: Dict[str, Any]):
            job_tracker[job_id]["current_stage"] = stage
            job_tracker[job_id]["progress"] = pct

        report = orchestrator.run_pipeline(ticker=ticker, focus=focus, progress_callback=on_progress)
        report_cache[report.report_id] = report
        
        job_tracker[job_id]["status"] = "COMPLETED"
        job_tracker[job_id]["progress"] = 100
        job_tracker[job_id]["report_id"] = report.report_id
    except Exception as e:
        job_tracker[job_id]["status"] = "FAILED"
        job_tracker[job_id]["error"] = str(e)

@app.post("/api/v1/generate-report")
def generate_report(req: GenerateRequest, background_tasks: BackgroundTasks):
    import uuid
    job_id = f"JOB-{uuid.uuid4().hex[:8].upper()}"
    job_tracker[job_id] = {
        "job_id": job_id,
        "ticker": req.ticker.upper(),
        "status": "QUEUED",
        "progress": 0,
        "current_stage": "Queued in runner",
        "report_id": None,
        "error": None
    }
    background_tasks.add_task(_run_report_task, job_id, req.ticker, req.focus)
    return {"job_id": job_id, "status": "QUEUED"}

@app.get("/api/v1/report-status/{job_id}")
def check_status(job_id: str):
    if job_id not in job_tracker:
        raise HTTPException(status_code=404, detail="Job ID not found")
    return job_tracker[job_id]

@app.get("/api/v1/report/{report_id}")
def get_report(report_id: str):
    if report_id not in report_cache:
        matching_json = list(settings.REPORTS_DIR.glob(f"*_{report_id}_claims.json"))
        if matching_json:
            import json
            with open(matching_json[0], "r", encoding="utf-8") as f:
                return json.load(f)
        raise HTTPException(status_code=404, detail="Report ID not found")
    return report_cache[report_id].model_dump()

@app.get("/api/v1/download-pdf/{report_id}")
def download_pdf(report_id: str):
    matching_pdf = list(settings.REPORTS_DIR.glob(f"*_{report_id}.pdf"))
    if not matching_pdf:
        raise HTTPException(status_code=404, detail="PDF report not found")
    return FileResponse(
        str(matching_pdf[0]),
        media_type="application/pdf",
        filename=matching_pdf[0].name
    )
