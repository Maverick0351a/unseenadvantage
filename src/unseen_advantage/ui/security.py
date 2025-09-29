from fastapi import Header, HTTPException, status
from unseen_advantage.config import Settings

async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expect = Settings().dash_api_key.strip()
    if expect == "":
        return
    if x_api_key is None or x_api_key != expect:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
