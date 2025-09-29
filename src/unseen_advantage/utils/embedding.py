from __future__ import annotations
import hashlib
from typing import Iterable, List
import numpy as np

def _unit(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    n = float(np.linalg.norm(x) + eps)
    return x / n

def stable_embed_text(text: str, dim: int = 256) -> np.ndarray:
    vals = np.empty(dim, dtype=np.float32)
    for i in range(dim):
        h = hashlib.sha256(f"{text}::{i}".encode("utf-8")).digest()
        u = int.from_bytes(h[:8], "big", signed=False)
        vals[i] = (u / 2**63) - 1.0
    # light token weighting for keywords
    tokens = [t.lower() for t in text.split()]
    for t in tokens[:8]:
        j = (hash(t) % dim)
        vals[j] += 0.05
    return _unit(vals)

def stable_embed_texts(texts: Iterable[str], dim: int = 256) -> np.ndarray:
    return np.vstack([stable_embed_text(t, dim=dim) for t in texts])
