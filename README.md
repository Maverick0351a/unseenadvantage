# Unseen Advantage — Cognitive Market Intelligence
> **Emergence (LNCP)** · **Exit Timing (TCD)** · **Fragility (CIVI)**

[![CI](https://img.shields.io/github/actions/workflow/status/your-org/your-repo/ci.yml?branch=main&label=CI)](../../actions)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

Unseen Advantage applies **Cognitive Tetrad** principles to financial data:
- **LNCP** – *Latent Narrative Coherence Prediction*: surfaces **emergent narratives** from weak signals.
- **TCD** – *Temporal Coherence Decay*: quantifies **signal decay** to time exits.
- **CIVI** – *Cross-Impact Vulnerability Index*: measures **market fragility** via sensitivity analysis.

The platform ships as a **Python SDK + FastAPI Control Panel**, a **CLI**, and a **reproducible demo**.

---

## Features

- **LNCP (emergence)**: weak-signal clustering → cross-scale flow → predicted energy drop (ΔE) → **Narrative Potential Energy (NPE)** ranking.
- **TCD (exits)**: EMA narrative vector; **drift vs origin × recent dilution** → high TCD means it’s time to trim or re-evaluate.
- **CIVI (fragility)**: standardized small shocks; **Δ Energy** response → higher CIVI signals brittle conditions.
- **Deterministic embeddings** for demos (SHA-256): reproducible by design; swap in real embeddings any time.
- **FastAPI Control Panel** (Jinja2/HTMX-ready) and **CLI** for scripted operation.
- **CI**: unit tests, demo run, and API smoke in GitHub Actions.

---

## Quickstart (local)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e ".[dev,ui]"

# run reproducible demo -> reports/
python scripts/run_demo.py

# launch API
uvicorn unseen_advantage.api.server:app --host 0.0.0.0 --port 8088
# http://127.0.0.1:8088/
```


API endpoints

GET /healthz

POST /score_events – score batch events by InfoGain proxy (demo)

POST /lncp/scan – run emergent narrative scan and return top NPE alerts

CLI

```bash
# LNCP alerts
python -m unseen_advantage.cli lncp-scan --events examples/finance_demo/events.csv --out alerts.csv

# Exit watchlist (TCD)
python -m unseen_advantage.cli tcd-watchlist --events examples/finance_demo/events.csv --assets AAPL,TSLA,NVDA,MSFT --out tcd.csv

# Fragility (CIVI)
python -m unseen_advantage.cli civi --events examples/finance_demo/events.csv --out civi.json
```

Docker

Build & run

```bash
docker build -t unseen-advantage:local .
docker run --rm -it -p 8088:8088 -v $PWD/reports:/app/reports unseen-advantage:local
# open http://127.0.0.1:8088/
```


Compose

```bash
docker compose up -d --build
docker compose logs -f api
docker compose run --rm demo
docker compose down
```


Mounts ./reports for outputs and ./examples for demo inputs.

## Reproducible Demo (what to expect)

Running `python scripts/run_demo.py` generates:

- `reports/lncp_alerts.csv` – ranked emergent narratives with NPE, ΔE, path, and stability
- `reports/tcd_watchlist.csv` – per-asset TCD with coherence-to-origin and recent dilution
- `reports/civi.json` – CIVI (avg ΔEnergy from small shocks; higher → more fragile)

The demo uses deterministic embeddings and a small synthetic event set, so results are the same on every run.

## Configuration

Environment variables (optional):

- `UA_API_KEY` – if set, the API expects header `x-api-key: <value>` (enable gate in your server where appropriate)
- `PORT` – API port (default 8088)

See `src/unseen_advantage/config.py` for additional knobs.

## Architecture (short)

- **Embeddings**: deterministic SHA-256 embeddings (demo); swap with your encoder later.
- **LNCP**: cluster weak signals → linear cross-scale flow (W(m)) → energy deltas via PSD kernel → NPE ranking.
- **TCD**: EMA narrative N_t; TCD = (1 − cos(N_t, N_origin)) × mean(1 − cos(e_new, N_t)).
- **CIVI**: sample standardized perturbations; propagate; compute ΔEnergy; average.

## Roadmap

- Backtest harness: threshold calibration & hit-rates for LNCP/TCD/CIVI
- Multi-tenant Control Panel (API keys + RBAC)
- Optional tensor/bilinear flow in LNCP for richer propagation
- Data connectors (news, transcripts, filings) and real embeddings

## Contributing

PRs welcome! Please:

- add/modify tests under `tests/`
- keep demo deterministic
- include a short note in `CHANGELOG.md` (if present)

License: Apache-2.0 (recommendation; adjust to your preference)


> Replace `your-org/your-repo` in the badge URL after you push.
