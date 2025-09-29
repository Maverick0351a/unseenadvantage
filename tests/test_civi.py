from unseen_advantage.ui.service import compute_civi_score
from unseen_advantage.config import Settings

def test_civi_runs():
    s = Settings()
    d = compute_civi_score(s.dashboard_events_path)
    assert "civi" in d and "samples" in d
