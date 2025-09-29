from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    embedding_dim: int = 256

    # Dashboard / demo defaults
    dashboard_events_path: str = "examples/finance_demo/events.csv"
    dashboard_prices_path: Optional[str] = "examples/finance_demo/prices.csv"
    dashboard_watchlist_assets: List[str] = ["AAPL", "TSLA", "NVDA", "MSFT"]
    dash_api_key: str = ""  # set to require X-API-Key

    class Config:
        env_prefix = "UA_"
