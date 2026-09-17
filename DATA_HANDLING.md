# Reddit Data Handling

This document describes the intended handling of Reddit data by this reference client.

## Collection

The client requests only public Reddit content needed for an explicit search initiated by the operator. The initial implementation retrieves public submissions and normalizes a minimal set of fields needed for aggregate topic/sentiment analysis:

- Reddit thing/post identifier
- subreddit
- title and self-text
- creation timestamp
- score and comment count when supplied by the API
- canonical Reddit permalink

Author usernames, user IDs, profile information, avatars, flair, and private data are not part of the normalized application record.

## Purpose limitation

Data is retrieved only for the application's approved read-only topic and financial-sentiment analysis use case. It is not used for automated outreach, advertising targeting, individual profiling, or inference of sensitive characteristics.

## AI/ML

Reddit content retrieved by this client must not be used to train or fine-tune machine-learning or AI models unless separately and explicitly authorized by Reddit and applicable rightsholders. The intended downstream use is inference-time classification, clustering, sentiment analysis, or summarization of public discussions at an aggregate/topic level, subject to Reddit's approval of that use case.

## Retention and deletion

The reference CLI processes normalized records in memory and prints them to stdout; it does not create a persistent Reddit-content database.

An integrating application that introduces caching should:

1. store only data required for the approved functionality;
2. use short-lived caching rather than indefinite archives;
3. routinely refresh or delete cached Reddit content, with a target maximum cache age of 48 hours where practical;
4. remove content that Reddit or its author has deleted;
5. remove author-identifying information associated with deleted accounts;
6. immediately remove data that is no longer required for the approved use case or when Reddit requires deletion.

## Security

OAuth credentials are provided through environment variables and must never be committed to source control, logs, example output, or datasets. `.env` is excluded by `.gitignore`.

## Rate limiting

The client observes Reddit's `X-Ratelimit-Used`, `X-Ratelimit-Remaining`, and `X-Ratelimit-Reset` headers when present. It slows or stops requests as the remaining allowance approaches exhaustion and honors HTTP 429 / Retry-After responses. It does not rotate credentials, accounts, proxies, or clients to evade limits.

## No write actions

The reference client has no functionality for posting, commenting, voting, messaging, moderation, or automated account creation.
