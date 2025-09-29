from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import numpy as np

@dataclass
class LNCPAlert:
    npe: float
    scale_states: Dict[int, np.ndarray]
    cluster_ids: List[str]
    score_components: dict

def path_length(predicted: Dict[int, np.ndarray]) -> float:
    L = 0.0
    for m in sorted(predicted.keys())[:-1]:
        v = predicted[m+1]
        g = float(np.linalg.norm(v))
        L += 1.0 / (g + 1e-6)
    return float(L)

def stability(freq: float, var_dt: float, af: float = 2.0, av: float = 1.5) -> float:
    import math
    sf = 1.0 / (1.0 + math.exp(-af * (freq - 0.5)))
    sv = 1.0 / (1.0 + math.exp(-av * (max(0.0, 0.5 - var_dt))))
    return float(sf * sv)

def compute_npe(delta_E: float, L: float, S: float, alpha: float = 0.6) -> float:
    return float(delta_E * np.exp(-alpha * L) * S)
