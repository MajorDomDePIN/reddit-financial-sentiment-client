# Reddit Data Handling

This document defines the data-handling boundary for this application.

## Purpose and collection

The application is a personal, non-commercial, read-only financial discussion client. A request is initiated manually by its single operator and is restricted to `r/stocks`, `r/investing`, or `r/wallstreetbets`.

The normalized record contains only:

- Reddit post/thing identifier;
- subreddit;
- title and self-text;
- creation timestamp;
- score and comment count when supplied by Reddit;
- canonical Reddit permalink.

Author username, Reddit user ID, profile URL, avatar, user flair and other profile fields are deliberately excluded.

## Purpose limitation

Reddit data is used only for the approved financial-discussion use case. It is not used for advertising, lead generation, marketing outreach, user targeting, user profiling, identity resolution, resale, licensing, redistribution, or a commercial product/service.

The application does not infer potentially sensitive characteristics about Reddit users, including health, political affiliation or sexual orientation, and does not attempt to identify, re-identify, deanonymize, or match Redditors to off-platform identities.

## AI / machine learning

Reddit content is not used to train, fine-tune, benchmark, evaluate, or otherwise modify an AI or machine-learning model.

If included in the use case Reddit approves, existing local models may process transient retrieved text at inference time for aggregate/topic-level sentiment classification or summarization. Outputs are about discussion of the requested financial asset, not individual Redditors.

## Retention

The reference CLI processes records in memory and writes JSON to standard output. It does not create a persistent Reddit-content database.

If short-lived caching is later required for the approved functionality, the integration must:

1. cache only the minimum fields required for that functionality;
2. expire cached Reddit content automatically within 48 hours at the latest;
3. refresh/delete cached records when the corresponding Reddit content is deleted or removed;
4. delete author-identifying information associated with a deleted Reddit account if any such information was ever received outside the normalized record;
5. immediately delete data that is no longer necessary for the approved use case, that Reddit requests be deleted, or when API access/application operation ends;
6. never retain deleted content merely because it has been anonymized or transformed.

The preferred design is no persistent storage at all.

## OAuth credentials and security

OAuth tokens are supplied locally through environment variables, excluded from version control, and must not appear in logs, datasets, examples, or repository files. Tokens must only be credentials issued/authorized for this application and approved use case.

## Rate limiting and access controls

The client observes Reddit's `X-Ratelimit-Used`, `X-Ratelimit-Remaining`, and `X-Ratelimit-Reset` response headers and honors HTTP 429 / `Retry-After`.

It does not rotate accounts, OAuth clients, tokens, proxies, IP addresses, User-Agents, browser sessions, or other identities to circumvent Reddit access controls or limits. It does not scrape Reddit HTML as a substitute for denied API access.

## No write or automated interaction

There is no functionality for posting, commenting, voting, messaging, moderation, account creation, automated outreach, or engagement manipulation.

## Scope changes

The approved use case is the boundary. Commercial use, research, AI training, broader data collection, additional communities, or other material changes are not authorized merely because this client has credentials. The operator must obtain any additional Reddit permission required before making such a change.
