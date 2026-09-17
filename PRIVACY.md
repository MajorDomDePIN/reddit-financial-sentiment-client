# Privacy Policy

_Last updated: September 17, 2026_

## Application

Reddit Financial Sentiment Client is a personal, non-commercial, read-only developer application operated by the repository owner. It is intended for one operator and is not offered as a public service.

## Reddit data processed

For a manually initiated financial query, the application may process recent public Reddit submissions from the configured communities `r/stocks`, `r/investing`, and `r/wallstreetbets`.

The normalized application record is limited to the post identifier, subreddit, title/self-text, creation timestamp, public score/comment count when supplied, and permalink. The application deliberately excludes author usernames, Reddit user IDs, profiles, avatars and user flair from normalized output.

No private messages or private Reddit content are requested.

## Purpose

The data is processed solely to provide aggregate topic/sentiment information about a user-supplied public company, ticker, or financial asset to the operator.

The application does not use Reddit data for advertising, lead generation, automated outreach, individual profiling, sensitive-trait inference, identity resolution, resale, redistribution, or AI/ML training.

## Storage and deletion

The reference client processes Reddit content in memory and does not maintain a persistent Reddit-content database. If an approved integration later requires temporary caching, cached Reddit content will be limited to what is necessary and configured to expire within 48 hours at the latest.

Content deleted or removed from Reddit will not intentionally be retained. Data no longer needed for the approved functionality, or data Reddit requests be deleted, will be deleted. On termination of API access or operation of the application, stored Reddit content, if any, will be deleted as required by Reddit's terms.

## Sharing and sale

Reddit data is not sold, licensed, shared as a dataset, or provided to advertisers or data brokers. The application is not monetized.

## AI

Reddit content is not used to train, fine-tune, benchmark, evaluate, or otherwise modify AI or machine-learning models. Subject to the scope Reddit approves, existing local models may perform transient inference-time classification or summarization at an aggregate/topic level.

## Security

OAuth credentials are stored locally outside source control. The application uses OAuth credentials only for its approved purpose and follows Reddit rate limits and access controls.

## Requests / contact

Questions or deletion/compliance requests concerning this application can be submitted through the repository's GitHub Issues page. Requests relating to Reddit-hosted content may also need to be handled through Reddit itself.

## Changes

Material changes to the Reddit data use described here will not be treated as automatically covered by an existing Reddit approval. Additional permission will be sought when Reddit's policies require it.
