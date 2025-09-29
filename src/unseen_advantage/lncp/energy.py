from __future__ import annotations
from typing import Dict
import numpy as np

def energy_m(n: np.ndarray, C: np.ndarray, lam: float = 0.1) -> float:
    return float(- n.T @ C @ n + 0.5 * lam * (n @ n))

def build_kernel(anchors: np.ndarray) -> np.ndarray:
    if anchors.size == 0:
        return np.eye(256, dtype=np.float32)
    A = anchors / (np.linalg.norm(anchors, axis=1, keepdims=True) + 1e-12)
    K = A.T @ A
    return (K + 1e-3 * np.eye(K.shape[0], dtype=K.dtype)).astype(np.float32)

def delta_E_pred(baseline: Dict[int, np.ndarray],
                 predicted: Dict[int, np.ndarray],
                 kernels: Dict[int, np.ndarray],
                 lam: float = 0.1) -> float:
    dE = 0.0
    for m, n_old in baseline.items():
        C = kernels.get(m)
        if C is None:
            continue
        n_new = predicted.get(m, n_old)
        dE += energy_m(n_old, C, lam=lam) - energy_m(n_new, C, lam=lam)
    return float(max(0.0, dE))
