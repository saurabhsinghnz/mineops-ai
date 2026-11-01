from fastapi import FastAPI

app = FastAPI(
    title="MineOps AI",
    description="Industrial Maintenance Intelligence Platform",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "application": "MineOps AI",
        "version": "0.1.0"
    }
