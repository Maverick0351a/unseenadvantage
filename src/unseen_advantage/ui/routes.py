from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from unseen_advantage.config import Settings
from unseen_advantage.ui.templating import templates
from unseen_advantage.ui.security import require_api_key
from unseen_advantage.ui.service import compute_lncp_top, compute_civi_score, compute_tcd_watchlist

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    s = Settings()
    lncp = compute_lncp_top(s.dashboard_events_path, top_alerts=5)
    civi = compute_civi_score(s.dashboard_events_path)
    tcd = compute_tcd_watchlist(s.dashboard_events_path, s.dashboard_watchlist_assets)
    return templates.TemplateResponse("home.html", {"request": request, "lncp": lncp, "civi": civi, "tcd": tcd})

@router.post("/ui/run_lncp", dependencies=[Depends(require_api_key)], response_class=HTMLResponse)
def ui_run_lncp(request: Request):
    s = Settings()
    lncp = compute_lncp_top(s.dashboard_events_path, top_alerts=8)
    return templates.TemplateResponse("partials/lncp_table.html", {"request": request, "lncp": lncp})

@router.post("/ui/run_civi", dependencies=[Depends(require_api_key)], response_class=HTMLResponse)
def ui_run_civi(request: Request):
    s = Settings()
    civi = compute_civi_score(s.dashboard_events_path)
    return templates.TemplateResponse("partials/civi_tile.html", {"request": request, "civi": civi})

@router.post("/ui/run_tcd", dependencies=[Depends(require_api_key)], response_class=HTMLResponse)
def ui_run_tcd(request: Request):
    s = Settings()
    tcd = compute_tcd_watchlist(s.dashboard_events_path, s.dashboard_watchlist_assets)
    return templates.TemplateResponse("partials/tcd_table.html", {"request": request, "tcd": tcd})
