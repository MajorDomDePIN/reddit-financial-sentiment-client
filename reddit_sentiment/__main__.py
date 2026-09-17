from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from .client import RedditReadOnlyClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only Reddit topic retrieval")
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="Search recent public submissions")
    search.add_argument("--query", required=True)
    search.add_argument("--subreddit", required=True)
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--time", dest="time_filter", default="week", choices=["hour", "day", "week", "month", "year", "all"])

    args = parser.parse_args()
    load_dotenv()
    client = RedditReadOnlyClient.from_env()

    if args.command == "search":
        records = client.search_submissions(
            args.query,
            args.subreddit,
            limit=args.limit,
            time_filter=args.time_filter,
        )
        print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
