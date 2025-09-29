docker compose logs -f api
docker compose run --rm demo
docker compose down
# Unseen Advantage — Market Intelligence SaaS (Private Core)

**What it does**  
Unseen Advantage turns raw financial streams (news, filings, social, macro) into three actionable signals:

- **LNCP (Emergence):** surfaces *new, non-obvious* narratives early.
- **TCD (Exit Timing):** shows when a thesis is *losing grip* (decay).
- **CIVI (Fragility):** measures *systemic vulnerability* to small shocks.

**Who it’s for**  
Quant teams, macro desks, risk managers, and data platforms that need ranked, explainable signals—not another firehose.

---

## Product highlights

- **Multi-tenant API & dashboard** with per-tenant API keys, roles, and usage analytics.  
- **Plans & quotas** (Starter/Pro/Enterprise) with Stripe billing, trials, and webhooks.  
- **Fast endpoints** with Redis caching, rate-limiting, and background jobs for batch scans.  
- **Observability built-in**: Prometheus metrics, OpenTelemetry traces, structured logs.  
- **Deterministic demo mode**: SHA-based embeddings for fully reproducible examples.

---

## Quickstart (local, dev)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e ".[dev]"
cp .env.example .env        # fill STRIPE_* if testing billing

# run services

alembic upgrade head
uvicorn unseen_advantage.api.server:app --port 8088

# open dashboard
# http://127.0.0.1:8088/
```

API keys: create in the dashboard, use x-api-key header with /v1/* endpoints.

Key endpoints

GET /healthz

POST /v1/score

POST /v1/lncp/scan

POST /v1/tcd

POST /v1/civi

GET /metrics (internal)

All endpoints are tenant-scoped, rate-limited, and metered.

Plans & entitlements (example)
Plan	Seats	QPS	Events/mo	Features
Starter	1	2	25k	score
Pro	5	5	250k	score, lncp, tcd
Enterprise	custom	custom	custom	score, lncp, tcd, civi, SSO

Billing via Stripe. Webhooks update entitlements in real time.

Operations & observability

Metrics: request latency, error rate, 2xx/4xx/5xx, RPS by feature.

Tracing: OTel FastAPI integration.

Logs: structured (JSON), request IDs, no PII in logs.

Audit: user actions written to audit_log.

Contributing (profit-share program)

This repo is private. If you’re invited to contribute:

Sign the CLA.

Our Contributor Profit-Share (see CONTRIBUTORS.md) allocates a portion of net SaaS revenue monthly, weighted by impact.

All contributions must include tests and pass CI.

License

Proprietary (see LICENSE_EULA.md). No redistribution or reverse engineering.


---

## 12) Minimal test plan (must pass CI)

- **Unit**: auth, entitlements, rate limiting, LNCP/TCD/CIVI smoke.
- **API**: 200 on happy paths; 401/403 on bad keys/quotas; webhook signature verify.
- **Integration**: enqueue LNCP job, confirm output rows appear for tenant.
- **Performance**: p95 latency guard (e.g., < 200ms for `/v1/score` in dev).

### Copilot prompt
> Add tests under **tests/** for auth (API key & JWT), entitlements (plan gating), rate-limit (redis), and webhook verification (Stripe mock). Add one perf test for `/v1/score` with small batch.

---

## 13) Profit-share ledger (MVP calculation)

- **Pool** = `pool_pct * net_revenue(month)`
- **Weights**: `impact_score` (merged code, issues resolved, feature impact) + optional *referral* weight.
- **Output**: `ProfitShareRun` rows + `ProfitShareGrant` rows per contributor.  
- **Export**: CSV for accounting + dashboard view for transparency.

### Copilot prompt
> Implement `compute_profit_share(period_start, period_end, pool_pct)` in `jobs/tasks.py`.  
> Create `GET /admin/profit-share/:run_id` dashboard view and CSV export.

---

## 14) Deployment notes (pick one now, switch later)

- **Heroku/Render/Fly.io**: simplest to start.  
- **AWS ECS Fargate**: private subnets, RDS Postgres, ElastiCache, ALB; use Terraform stubs under `infra/terraform/`.  
- **Cloudflare**: DNS, WAF, bot mitigation, rate-limit at edge (bonus).

---

# TL;DR execution map

1) **Phase A**: EULA/CLA + repo hygiene → CI green  
2) **Phase B**: Multi-tenant models + Auth + RBAC + Audit  
3) **Phase C**: Stripe billing + entitlements + webhooks  
4) **Phase D**: Quotas/rate-limit/metering (Redis)  
5) **Phase E**: v1 endpoints, Dashboard, Admin  
6) **Phase F**: Jobs (LNCP nightly, metering, profit-share)  
7) **Phase G**: Observability & security hardening  
8) **Phase H**: Docker, compose, CI/CD, deploy staging → prod

If you want, I can also produce a **ready-to-paste EULA + CLA template** and a **set of exact file diffs** for the Phase B+C models/routes so Copilot can apply patches in one go.
Environment variables (optional):
