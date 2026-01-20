from fastapi import FastAPI
from api.routers import health, platform, storage, cluster

app = FastAPI(
    title="AURORA Control Plane",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(platform.router)
app.include_router(storage.router)
app.include_router(cluster.router)
