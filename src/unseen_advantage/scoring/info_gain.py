from __future__ import annotations
import numpy as np
from unseen_advantage.config import Settings
from unseen_advantage.utils.embedding import stable_embed_text

class InfoGainScorer:
    def __init__(self, settings: Settings):
        self.dim = settings.embedding_dim
        # simple global narrative seed (could be learned)
        self.narr = np.zeros(self.dim, dtype=np.float32)

    def score_event(self, asset: str, text: str, risk01: float = 0.25):
        v = stable_embed_text(text, dim=self.dim)
        # proxy: score by alignment to current pseudo-narrative + keyword bump
        s_dense = float(max(0.0, np.dot(v, self.narr)))
        # asset keyword bump
        if asset.lower() in text.lower():
            s_dense += 0.05
        # update narrative (EMA-like) lightly
        self.narr = 0.98 * self.narr + 0.02 * v
        # return (score, debug...)
        return s_dense, {"dense": s_dense}
