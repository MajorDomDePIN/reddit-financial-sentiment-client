"""Minimal read-only Reddit Data API client.

This module intentionally exposes only retrieval methods. It contains no write,
moderation, messaging, voting, or account-automation functionality.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import requests

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API_BASE = "https://oauth.reddit.com"


class RedditAccessError(RuntimeError):
    pass


@dataclass
class RateState:
    used: float | None = None
    remaining: float | None = None
    reset_seconds: float | None = None


class RedditReadOnlyClient:
    def __init__(self, client_id: str, client_secret: str, user_agent: str) -> None:
        if not client_id or not client_secret:
            raise ValueError("OAuth client credentials are required")
        if not user_agent or "your_reddit_username" in user_agent:
            raise ValueError("Set a truthful, descriptive REDDIT_USER_AGENT")

        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self._access_token: str | None = None
        self._expires_at = 0.0
        self.rate = RateState()

    @classmethod
    def from_env(cls) -> "RedditReadOnlyClient":
        return cls(
            os.environ.get("REDDIT_CLIENT_ID", ""),
            os.environ.get("REDDIT_CLIENT_SECRET", ""),
            os.environ.get("REDDIT_USER_AGENT", ""),
        )

    def _authenticate(self) -> None:
        # OAuth client-credentials grant is suitable only if Reddit has approved
        # that grant/application type for this app. The implementation can be
        # adjusted to the exact OAuth flow specified in the approval response.
        response = self.session.post(
            TOKEN_URL,
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=20,
        )
        if response.status_code >= 400:
            raise RedditAccessError(
                f"OAuth failed with HTTP {response.status_code}; verify that "
                "this application's API access and OAuth flow are approved."
            )
        payload = response.json()
        token = payload.get("access_token")
        if not token:
            raise RedditAccessError("OAuth response did not contain access_token")
        self._access_token = token
        self._expires_at = time.time() + max(60, int(payload.get("expires_in", 3600)) - 60)

    def _ensure_token(self) -> None:
        if not self._access_token or time.time() >= self._expires_at:
            self._authenticate()
        self.session.headers["Authorization"] = f"bearer {self._access_token}"

    def _update_rate_state(self, response: requests.Response) -> None:
        def number(name: str) -> float | None:
            try:
                value = response.headers.get(name)
                return float(value) if value is not None else None
            except ValueError:
                return None

        self.rate = RateState(
            used=number("X-Ratelimit-Used"),
            remaining=number("X-Ratelimit-Remaining"),
            reset_seconds=number("X-Ratelimit-Reset"),
        )

    def _respect_rate_state(self) -> None:
        if self.rate.remaining is not None and self.rate.remaining <= 1:
            wait = self.rate.reset_seconds or 60.0
            time.sleep(max(1.0, min(wait, 600.0)))

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        self._ensure_token()
        self._respect_rate_state()
        response = self.session.get(f"{API_BASE}{path}", params=params, timeout=20)
        self._update_rate_state(response)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            try:
                wait = float(retry_after) if retry_after else (self.rate.reset_seconds or 60.0)
            except ValueError:
                wait = 60.0
            # One conservative retry only; never loop around an enforced limit.
            time.sleep(max(1.0, min(wait, 600.0)))
            response = self.session.get(f"{API_BASE}{path}", params=params, timeout=20)
            self._update_rate_state(response)

        if response.status_code >= 400:
            raise RedditAccessError(f"Reddit API returned HTTP {response.status_code}")
        return response.json()

    def search_submissions(
        self,
        query: str,
        subreddit: str,
        limit: int = 25,
        sort: str = "new",
        time_filter: str = "week",
    ) -> list[dict[str, Any]]:
        """Search public submissions and return a data-minimized representation."""
        if not query.strip():
            raise ValueError("query must not be empty")
        subreddit = subreddit.strip().removeprefix("r/").strip("/")
        if not subreddit:
            raise ValueError("subreddit must not be empty")

        limit = max(1, min(int(limit), 100))
        payload = self._get(
            f"/r/{subreddit}/search",
            {
                "q": query,
                "restrict_sr": "on",
                "sort": sort,
                "t": time_filter,
                "limit": limit,
                "raw_json": 1,
            },
        )

        records: list[dict[str, Any]] = []
        for child in payload.get("data", {}).get("children", []):
            data = child.get("data", {})
            # Deliberately omit author identity and profile metadata.
            records.append(
                {
                    "id": data.get("name") or data.get("id"),
                    "subreddit": data.get("subreddit"),
                    "title": data.get("title", ""),
                    "text": data.get("selftext", ""),
                    "created_utc": data.get("created_utc"),
                    "score": data.get("score"),
                    "num_comments": data.get("num_comments"),
                    "permalink": (
                        f"https://www.reddit.com{data.get('permalink')}"
                        if data.get("permalink")
                        else None
                    ),
                }
            )
        return records
