from fastapi import FastAPI, HTTPException
from web_dashboard.services.pipeline import run_pipeline

app = FastAPI(title="MENA Eval Tools (Dashboard Bridge)", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/run")
def run(payload: dict | None = None):
    try:
        result = run_pipeline(payload or {})
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
