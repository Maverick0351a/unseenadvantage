from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PORT = int(os.environ.get("PORT", "8088"))
BASE = f"http://127.0.0.1:{PORT}"


def wait_for(url: str, timeout: float = 20.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def main() -> int:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "unseen_advantage.api.server:app",
        "--host",
        "127.0.0.1",
        "--port",
        str(PORT),
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        text=True,
    )

    try:
        if not wait_for(f"{BASE}/healthz", timeout=25.0):
            print("ERROR: API did not become healthy in time", file=sys.stderr)
            return 1

        with urllib.request.urlopen(f"{BASE}/healthz", timeout=3) as resp:
            body = resp.read().decode("utf-8")
            print("healthz:", body)

        try:
            data = {
                "events": [
                    {
                        "event_id": "demo-1",
                        "ts": "2024-01-01T00:00:00Z",
                        "asset": "AAPL",
                        "text": "Apple announces new AI chip",
                    }
                ],
                "top_k": 2,
            }
            req = urllib.request.Request(
                f"{BASE}/score_events",
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                scored = resp.read().decode("utf-8")
                print("score_events:", scored[:256], "...")
        except Exception as exc:
            print("WARN: /score_events not executed:", exc)

        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
