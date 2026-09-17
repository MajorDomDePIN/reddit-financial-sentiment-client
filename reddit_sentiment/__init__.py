"""Read-only Reddit financial/topic retrieval client."""

from .client import RedditAccessError, RedditReadOnlyClient

__all__ = ["RedditAccessError", "RedditReadOnlyClient"]
