"""Minimal read-only Reddit Data API client.

The client intentionally exposes retrieval only. It has no write, moderation,
messaging, voting, outreach, or account-automation functionality.

Data API calls must only be made after Reddit has approved this application's
access and issued/authorized the corresponding OAuth credentials.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import requests

API_BASE = "https://oauth.reddit.com"
ALLOWED_SUBREDDITS = frozenset({"stocks", "investing", "wallstreetbets"})


class RedditAccessError(RuntimeError):
    pass


@dataclass
class RateState:
    used: float | None = None
    remaining: float | None = None
    reset_seconds: float | None = None


class RedditReadOnlyClient:
    """Read-only client using an OAuth bearer token obtained through an approved flow.

    OAuth token acquisition is deliberately kept outside this reference client.
    Reddit may authorize a particular OAuth application type/flow during App Review;
    the caller supplies the resulting token through REDDIT_ACCESS_TOKEN.
    """

    def __init__(self, access_token: str, user_agent: str) -> None:
        if not access_token:
            raise ValueError("An OAuth access token from the approved application is required")
        if not user_agent or "your_reddit_username" in user_agent:
            raise ValueError("Set a truthful, descriptive REDDIT_USER_AGENT")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"bearer {access_token}",
                "User-Agent": user_agent,
            }
        )
        self.rate = RateState()

    @classmethod
    def from_env(cls) -> "RedditReadOnlyClient":
        return cls(
            os.environ.get("REDDIT_ACCESS_TOKEN", ""),
            os.environ.get("REDDIT_USER_AGENT", ""),
        )

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
        # Stop proactively before exhausting the allowance rather than trying
        # alternate accounts, credentials, IPs, or other circumvention.
        if self.rate.remaining is not None and self.rate.remaining <= 2:
            wait = self.rate.reset_seconds or 60.0
            time.sleep(max(1.0, min(wait, 600.0)))

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        self._respect_rate_state()
        response = self.session.get(f"{API_BASE}{path}", params=params, timeout=20)
        self._update_rate_state(response)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            try:
                wait = float(retry_after) if retry_after else (self.rate.reset_seconds or 60.0)
            except ValueError:
                wait = 60.0
            # One conservative retry only. Never rotate credentials or loop
            # around an enforced Reddit limit.
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
        """Search one approved public finance subreddit.

        The allowlist intentionally prevents Reddit-wide or arbitrary-community
        collection. Returned records omit author identity/profile metadata.
        """
        if not query.strip():
            raise ValueError("query must not be empty")
        subreddit = subreddit.strip().removeprefix("r/").strip("/").lower()
        if subreddit not in ALLOWED_SUBREDDITS:
            raise ValueError(
                f"subreddit must be one of the configured scope: {', '.join(sorted(ALLOWED_SUBREDDITS))}"
            )

        # Low-volume reference client: deliberately cap a manual query at 25.
        limit = max(1, min(int(limit), 25))
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
