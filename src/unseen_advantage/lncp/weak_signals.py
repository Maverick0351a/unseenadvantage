from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import pandas as pd
from unseen_advantage.utils.embedding import stable_embed_texts

@dataclass
class WeakCluster:
    event_ids: List[str]
    asset: str | None
    seed_vec: np.ndarray
    lps: float

def l2norm(X: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    n = np.linalg.norm(X, axis=1, keepdims=True) + eps if X.ndim == 2 else (np.linalg.norm(X) + eps)
    return X / n

def lps_score(vectors: np.ndarray, anchors: np.ndarray | None = None,
              mu_intra: float = 1.0, mu_proto: float = 0.5) -> float:
    if vectors.shape[0] < 2:
        intra = 0.0
    else:
        V = l2norm(vectors)
        sims = V @ V.T
        intra = float((np.sum(sims) - np.trace(sims)) / (vectors.shape[0] * (vectors.shape[0]-1)))
    proto = 0.0
    if anchors is not None and anchors.size > 0:
        A = l2norm(anchors)
        V = l2norm(vectors)
        proto = float(np.mean(np.max(V @ A.T, axis=1)))
    return mu_intra * intra + mu_proto * proto

def simple_kmeans(X: np.ndarray, k: int, iters: int = 25, seed: int = 13) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    k = min(k, max(1, n))
    idx = rng.choice(n, size=k, replace=False)
    C = X[idx].copy()
    labels = np.zeros(n, dtype=int)
    for _ in range(iters):
        sims = l2norm(X) @ l2norm(C).T
        labels = np.argmax(sims, axis=1)
        for j in range(k):
            mask = labels == j
            if np.any(mask):
                C[j] = np.mean(X[mask], axis=0)
    return l2norm(C), labels

def find_weak_events(events: pd.DataFrame, scores: np.ndarray, smin: float, smax: float) -> pd.DataFrame:
    out = events.copy()
    out["ua_score"] = scores
    return out[(out["ua_score"] >= smin) & (out["ua_score"] <= smax)]

def cluster_weak_signals(weak_df: pd.DataFrame, anchors: np.ndarray | None = None,
                         max_k: int = 6, min_size: int = 3, seed: int = 13,
                         dim: int | None = None) -> List[WeakCluster]:
    if weak_df.empty:
        return []
    if dim is None and anchors is not None and anchors.size:
        dim = anchors.shape[1]
    dim = dim or 256
    X = stable_embed_texts(weak_df["text"].tolist(), dim=dim)
    k = min(max_k, max(1, X.shape[0] // 8))
    C, labels = simple_kmeans(X, k=k, seed=seed)
    clusters: List[WeakCluster] = []
    for j in range(C.shape[0]):
        mask = labels == j
        if np.sum(mask) < min_size:
            continue
        V = X[mask]
        ids = weak_df.loc[mask, "event_id"].tolist()
        assets = weak_df.loc[mask, "asset"].tolist()
        asset = assets[0] if len(set(assets)) == 1 else None
        centroid = l2norm(np.mean(V, axis=0, keepdims=True))[0]
        lps = lps_score(V, anchors=anchors)
        clusters.append(WeakCluster(event_ids=ids, asset=asset, seed_vec=centroid, lps=lps))
    if not clusters and X.shape[0] > 0:
        centroid = l2norm(np.mean(X, axis=0, keepdims=True))[0]
        ids = weak_df["event_id"].tolist()
        assets = weak_df["asset"].tolist()
        asset = assets[0] if len(set(assets)) == 1 else None
        lps = lps_score(X, anchors=anchors)
        clusters.append(WeakCluster(event_ids=ids, asset=asset, seed_vec=centroid, lps=lps))
    clusters.sort(key=lambda c: -c.lps)
    return clusters
