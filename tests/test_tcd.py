from unseen_advantage.ui.service import compute_tcd_watchlist
from unseen_advantage.config import Settings

def test_tcd_runs():
    s = Settings()
    rows = compute_tcd_watchlist(s.dashboard_events_path, s.dashboard_watchlist_assets)
    assert isinstance(rows, list)
    assert len(rows) >= 1
    for r in rows:
        assert "asset" in r and "tcd" in r
