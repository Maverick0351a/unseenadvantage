from __future__ import annotations
import json, os
from pathlib import Path
import pandas as pd

from unseen_advantage.ui.service import compute_lncp_top, compute_tcd_watchlist, compute_civi_score
from unseen_advantage.config import Settings

def main():
    s = Settings()
    events_path = s.dashboard_events_path
    reports = Path("reports"); reports.mkdir(exist_ok=True, parents=True)

    lncp = compute_lncp_top(events_path, top_alerts=8)
    pd.DataFrame(lncp).to_csv(reports / "lncp_alerts.csv", index=False)

    tcd = compute_tcd_watchlist(events_path, s.dashboard_watchlist_assets)
    pd.DataFrame(tcd).to_csv(reports / "tcd_watchlist.csv", index=False)

    civi = compute_civi_score(events_path)
    (reports / "civi.json").write_text(json.dumps(civi, indent=2))

    print("Wrote:")
    print(" - reports/lncp_alerts.csv")
    print(" - reports/tcd_watchlist.csv")
    print(" - reports/civi.json")

if __name__ == "__main__":
    main()
