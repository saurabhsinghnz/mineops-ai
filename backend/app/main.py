from app.api.routes.equipment import router as equipment_router
from fastapi import FastAPI

app = FastAPI(title="MineOps AI", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(equipment_router)
