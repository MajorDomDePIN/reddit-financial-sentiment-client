# Reddit Data API App Review — Scope Summary

This file is provided to make the requested use case easy to review against the implementation.

## Applicant / operator

- GitHub: `MajorDomDePIN`
- Reddit operator account: `/u/Academic-Shape321`
- Users of application: 1
- Use: personal and non-commercial

## Requested functionality

Read-only OAuth Data API access for a local Python application. The operator manually enters a public company, ticker, or financial asset. The application retrieves a small set of recent matching public submissions from one of three configured investing communities and returns data-minimized records for aggregate financial-discussion sentiment/topic analysis.

Example: a manual `NVDA` query in `r/stocks` can retrieve up to 25 recent matching submissions.

## Requested Reddit scope

Communities:

- `r/stocks`
- `r/investing`
- `r/wallstreetbets`

Actions/data:

- search/read recent public submissions;
- post identifier and permalink;
- subreddit and timestamp;
- title/self-text;
- public score and comment count when returned by Reddit.

Not requested:

- posting, commenting or voting;
- messaging or private communications;
- moderation actions;
- account creation;
- private content;
- arbitrary Reddit-wide collection;
- user/profile collection;
- commercial use;
- academic research;
- advertising or lead generation;
- AI/ML training.

## Why an external Data API client instead of a Reddit-native app

The application is a local external Python workflow whose output is combined locally with non-Reddit financial information. Reddit is a limited read-only input rather than the host/user interface of the application. The requested functionality does not need Reddit-native UI, moderation, posting, event triggers, or subreddit-facing interactions.

## Safeguards implemented in this repository

- fixed three-subreddit allowlist in code;
- maximum 25 results per manual query;
- no write methods;
- author/profile fields omitted from normalized records;
- OAuth bearer token required;
- descriptive User-Agent configuration;
- `X-Ratelimit-*` monitoring;
- 429 / `Retry-After` backoff;
- no identity/proxy/credential rotation;
- no persistent Reddit database in reference client;
- 48-hour maximum if temporary caching is introduced;
- documented deletion obligations;
- documented privacy policy;
- explicit prohibition on user profiling, sensitive-trait inference, commercialization, and AI training.

## AI clarification

Reddit data is not training data. No model is trained, fine-tuned, benchmarked, evaluated, or modified with Reddit content. If Reddit approves the described downstream processing, an already-existing local model may transiently classify/summarize retrieved text to produce aggregate discussion sentiment/topic information about the requested financial asset.

## Commercial clarification

This application is not operated for or on behalf of a business, is not monetized, and does not sell, license, redistribute, advertise against, or otherwise commercialize Reddit data or derived data.

Any materially different future use would require whatever additional permission Reddit requires; approval for this scope would not be treated as blanket authorization for another application or use case.
