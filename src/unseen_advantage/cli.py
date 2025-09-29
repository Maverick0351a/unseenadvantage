import typer, json
from unseen_advantage.config import Settings
from unseen_advantage.ui.service import compute_lncp_top, compute_tcd_watchlist, compute_civi_score

app = typer.Typer(add_completion=False)

@app.command("lncp-scan")
def lncp_scan(events: str = typer.Option(..., help="Path to events.csv"),
              out: str = typer.Option("alerts.csv", help="Output CSV")):
    rows = compute_lncp_top(events_path=events, top_alerts=10)
    import pandas as pd
    pd.DataFrame(rows).to_csv(out, index=False)
    typer.echo(f"Wrote {out} ({len(rows)} alerts)")

@app.command("tcd-watchlist")
def tcd_watchlist(events: str = typer.Option(..., help="Path to events.csv"),
                  assets: str = typer.Option("AAPL,TSLA,NVDA,MSFT", help="Comma-separated tickers"),
                  out: str = typer.Option("tcd.csv", help="Output CSV")):
    alist = [a.strip() for a in assets.split(",") if a.strip()]
    rows = compute_tcd_watchlist(events_path=events, assets=alist)
    import pandas as pd
    pd.DataFrame(rows).to_csv(out, index=False)
    typer.echo(f"Wrote {out} ({len(rows)} rows)")

@app.command("civi")
def civi(events: str = typer.Option(..., help="Path to events.csv"),
         out: str = typer.Option("civi.json", help="Output JSON")):
    d = compute_civi_score(events_path=events)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)
    typer.echo(f"Wrote {out}")

if __name__ == "__main__":
    app()
