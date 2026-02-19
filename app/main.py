from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()
from prometheus_client import Counter
from fastapi import Request
REQUESTS = Counter(
    "requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)

    REQUESTS.labels(
        method=request.method,
        path=request.url.path,
        status=response.status_code
    ).inc()

    return response

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/hello")
def hello():
    return {"msg": "hello from devops-platform-demo"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

