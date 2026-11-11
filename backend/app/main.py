from fastapi import FastAPI

from backend.app.api.routes.equipment import router as equipment_router

app = FastAPI(title="MineOps AI", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(equipment_router)
