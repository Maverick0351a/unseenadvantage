from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np

def l2norm(x: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    return x / (np.linalg.norm(x) + eps)

@dataclass
class LinearFlow:
    W: Dict[Tuple[int,int], np.ndarray]
    lam: float = 1e-3
    lr: float = 0.05

    @staticmethod
    def init(dims: List[int]) -> "LinearFlow":
        rng = np.random.default_rng(7)
        W = {}
        for m in range(len(dims)-1):
            W[(m,m+1)] = rng.normal(0, 0.05, size=(dims[m+1], dims[m])).astype(np.float32)
        return LinearFlow(W=W)

    def propagate(self, n_m: np.ndarray, m: int) -> np.ndarray:
        W = self.W[(m,m+1)]
        z = W @ n_m
        return np.tanh(z)

    def cascade(self, seed: np.ndarray, m0: int = 0) -> Dict[int, np.ndarray]:
        states = {m0: l2norm(seed)}
        max_m = max(k[1] for k in self.W.keys())
        for m in range(m0, max_m):
            states[m+1] = l2norm(self.propagate(states[m], m))
        return states

    def fit_online(self, x_src: np.ndarray, y_tgt: np.ndarray, m: int) -> None:
        W = self.W[(m,m+1)]
        x = x_src.reshape(-1,1)
        y = y_tgt.reshape(-1,1)
        Wx = W @ x
        grad = (Wx - y) @ x.T - self.lam * W
        self.W[(m,m+1)] = W - self.lr * grad.astype(W.dtype)
