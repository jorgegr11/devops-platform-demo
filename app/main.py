from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()
requests_total = Counter("requests_total", "Total requests", ["path"])

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/hello")
def hello():
    requests_total.labels(path="/hello").inc()
    return {"msg": "hello from devops-platform-demo"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

