from unseen_advantage.ui.service import compute_lncp_top
from unseen_advantage.config import Settings

def test_lncp_runs():
    s = Settings()
    rows = compute_lncp_top(s.dashboard_events_path, top_alerts=5)
    assert isinstance(rows, list)
    # should produce at least one row with this synthetic dataset
    assert len(rows) >= 1
    for r in rows:
        assert "npe" in r and "dE" in r and "path" in r and "stab" in r
