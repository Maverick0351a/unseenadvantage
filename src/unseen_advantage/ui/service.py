from __future__ import annotations
from typing import Dict, List
import numpy as np
from unseen_advantage.config import Settings
from unseen_advantage.finance.parsers import load_events_csv
from unseen_advantage.scoring.info_gain import InfoGainScorer
from unseen_advantage.utils.embedding import stable_embed_texts
from unseen_advantage.lncp.weak_signals import find_weak_events, cluster_weak_signals
from unseen_advantage.lncp.flow import LinearFlow
from unseen_advantage.lncp.energy import build_kernel, delta_E_pred
from unseen_advantage.lncp.npe import path_length, stability, compute_npe

def compute_lncp_top(events_path: str, *, smin=0.05, smax=0.25, max_clusters=6, top_alerts=5):
    settings = Settings()
    ev = load_events_csv(events_path)
    scorer = InfoGainScorer(settings)

    ua_scores = np.array([
        scorer.score_event(str(row["asset"]), str(row["text"]), risk01=0.25)[0]
        for _, row in ev.iterrows()
    ], dtype=float)

    weak_df = find_weak_events(ev, ua_scores, smin=smin, smax=smax)
    if weak_df.empty:
        scored = ev.copy()
        scored["ua_score"] = ua_scores
        if len(scored) > 1:
            lo = float(np.quantile(scored["ua_score"], 0.2))
            hi = float(np.quantile(scored["ua_score"], 0.8))
            if lo == hi:
                hi = float(scored["ua_score"].max())
            weak_df = scored[(scored["ua_score"] >= lo) & (scored["ua_score"] <= hi)]
        if weak_df.empty:
            weak_df = scored.nlargest(min(max_clusters * 3, len(scored)), "ua_score")
    anchors0 = stable_embed_texts(ev["text"].tolist(), dim=settings.embedding_dim)
    clusters = cluster_weak_signals(weak_df, anchors=anchors0, max_k=max_clusters, dim=settings.embedding_dim)
    if not clusters:
        return []

    dims = [settings.embedding_dim, settings.embedding_dim, settings.embedding_dim]
    flow = LinearFlow.init(dims=dims)

    baseline = {}
    baseline[0] = anchors0.mean(axis=0); baseline[0] /= (np.linalg.norm(baseline[0]) + 1e-12)
    baseline[1] = flow.propagate(baseline[0], 0)
    baseline[2] = flow.propagate(baseline[1], 1)

    K0 = build_kernel(anchors0); kernels = {0:K0, 1:K0.copy(), 2:K0.copy()}

    rows = []
    for cl in clusters:
        cascade = flow.cascade(cl.seed_vec, m0=0)
        dE = delta_E_pred(baseline, cascade, kernels, lam=0.1)
        Lp = path_length(cascade)
        freq = min(1.0, len(cl.event_ids) / 10.0)
        S = stability(freq=freq, var_dt=0.25)
        npe = compute_npe(dE, L=Lp, S=S, alpha=0.6)
        rows.append({"npe": float(npe), "dE": float(dE), "path": float(Lp), "stab": float(S),
                     "cluster_size": len(cl.event_ids), "cluster_ids": ";".join(cl.event_ids),
                     "asset": (cl.asset or "")})
    rows = sorted(rows, key=lambda r: -r["npe"])[:top_alerts]
    return rows

def compute_civi_score(events_path: str, *, shocks=20, seed=7) -> Dict:
    settings = Settings()
    rng = np.random.default_rng(seed)
    ev = load_events_csv(events_path)
    A = stable_embed_texts(ev["text"].tolist(), dim=settings.embedding_dim)

    K = build_kernel(A)
    flow = LinearFlow.init([settings.embedding_dim, settings.embedding_dim, settings.embedding_dim])
    n0 = A.mean(axis=0); n0 /= (np.linalg.norm(n0) + 1e-12)
    baseline = {0:n0, 1:flow.propagate(n0,0), 2:flow.propagate(flow.propagate(n0,0),1)}
    kernels = {0:K, 1:K.copy(), 2:K.copy()}

    idx = rng.integers(low=0, high=A.shape[0], size=shocks)
    deltas = A[idx] * 0.05
    impacts = []
    for delta in deltas:
        seed_vec = (n0 + delta); seed_vec /= np.linalg.norm(seed_vec) + 1e-12
        cascade = flow.cascade(seed_vec, m0=0)
        dE = delta_E_pred(baseline, cascade, kernels, lam=0.1)
        impacts.append(float(max(0.0, dE)))
    civi = float(np.mean(impacts)) if impacts else 0.0
    return {"civi": civi, "samples": len(impacts)}

def compute_tcd_watchlist(events_path: str, assets: List[str], *, window=50, recent_k=10):
    from unseen_advantage.utils.embedding import stable_embed_texts
    settings = Settings()
    ev = load_events_csv(events_path)
    rows = []
    for asset in assets:
        sub = ev[ev["asset"] == asset].tail(window)
        if sub.empty:
            rows.append({"asset": asset, "tcd": 0.0, "coh_origin": 0.0, "dilution": 0.0, "n": 0})
            continue
        V = stable_embed_texts(sub["text"].tolist(), dim=settings.embedding_dim)
        origin = V[0] / (np.linalg.norm(V[0]) + 1e-12)
        current = V.mean(axis=0); current /= (np.linalg.norm(current) + 1e-12)
        coh_origin = float(origin @ current)
        R = V[-recent_k:] if len(V) >= recent_k else V
        sims = (R @ current) / (np.linalg.norm(R, axis=1) + 1e-12)
        dilution = float(np.mean(1.0 - sims))
        tcd = (1.0 - max(0.0, min(1.0, coh_origin))) * max(0.0, min(1.0, dilution))
        rows.append({"asset": asset, "tcd": float(tcd), "coh_origin": float(coh_origin), "dilution": float(dilution), "n": int(len(sub))})
    rows.sort(key=lambda r: -r["tcd"])
    return rows
