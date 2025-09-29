from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from unseen_advantage.config import Settings

app = FastAPI(title="Unseen Advantage", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"ok": True, "version": "0.1.0"}

# Mount UI
from unseen_advantage.ui.routes import router as ui_router
app.include_router(ui_router)
