from fastapi import FastAPI
from api.routers import health, platform, storage, cluster
from fastapi import Request
from api.metrics import REQUEST_COUNT, REQUEST_LATENCY, router as metrics_router
import threading
from aurora_operator.controller import run_controller

app = FastAPI(
    title="AURORA Control Plane",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(platform.router)
app.include_router(storage.router)
app.include_router(cluster.router)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    with REQUEST_LATENCY.time():
        response = await call_next(request)
    REQUEST_COUNT.labels(
        method=request.method,
        path=request.url.path
    ).inc()
    return response

app.include_router(metrics_router)


@app.on_event("startup")
def start_controller():
    import threading
    from aurora_operator.controller import run_controller
    t = threading.Thread(target=run_controller, daemon=True)
    t.start()
