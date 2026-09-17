# Reddit Financial Sentiment Client

A small, standalone, **read-only and non-commercial** Python client intended for a Reddit Data API App Review.

Its single purpose is to let one operator manually retrieve a small number of recent public submissions about a user-supplied public company, ticker, or financial asset from a fixed set of public investing communities and produce a data-minimized representation for aggregate topic/sentiment analysis.

This repository is independent of any private downstream application. It does not expose or reproduce private source code.

## Access status

**No Reddit Data API access is assumed or bypassed by this project.** Data API functionality is intended to be used only after Reddit explicitly approves the application and the operator obtains an OAuth token through the flow authorized for that application.

The project does not scrape Reddit HTML, use browser/session cookies, rotate identities, proxies or credentials, or attempt to work around API/App Review restrictions.

## Exact scope

The reference implementation is deliberately narrow:

- one operator;
- personal, non-commercial use;
- manual queries rather than continuous bulk collection;
- read-only access;
- public submissions only;
- fixed community allowlist: `r/stocks`, `r/investing`, and `r/wallstreetbets`;
- maximum 25 results per manual query;
- company/ticker/financial-asset discussion only;
- no Reddit-wide arbitrary-community collection;
- no persistent Reddit-content database in this client.

The client has **no capability** to post, comment, vote, message, moderate, create accounts, perform unsolicited outreach, manipulate engagement, or otherwise write to Reddit.

## Data use

Normalized output contains only fields needed for aggregate discussion analysis: post identifier, subreddit, title/text, creation time, public engagement counts when returned by Reddit, and permalink.

Author usernames, Reddit user IDs, profile URLs, avatars, flair and other profile data are intentionally omitted. The application does not profile, score, target, identify, re-identify, or track Redditors and must not infer health, political affiliation, sexual orientation, or other sensitive characteristics.

Reddit content is **not used to train, fine-tune, benchmark, or otherwise modify an AI/ML model**. A separate local application may, if Reddit approves this use case, use existing models at inference time to classify or summarize the retrieved public financial discussion at an aggregate/topic level.

It is not used for advertising, lead generation, sales outreach, user targeting, resale, licensing, redistribution, or any commercial service.

See [DATA_HANDLING.md](DATA_HANDLING.md) and [PRIVACY.md](PRIVACY.md).

## Authentication and identification

All Data API requests use an OAuth bearer token. Token acquisition is intentionally outside this reference implementation so that the exact OAuth application type/flow granted by Reddit App Review can be used without pretending that an unapproved grant is available.

The client sends Reddit's documented descriptive User-Agent format:

```text
<platform>:<app-id>:<version> (by /u/<reddit-username>)
```

The example configuration identifies this app and its operator rather than masquerading as a browser or unrelated application.

## Rate-limit behavior

The client reads `X-Ratelimit-Used`, `X-Ratelimit-Remaining`, and `X-Ratelimit-Reset`, pauses before exhausting the allowance, and honors HTTP 429 / `Retry-After`. A 429 is retried at most once after the instructed wait.

It never rotates accounts, OAuth clients, credentials, proxies, IPs or User-Agents to evade a Reddit limit.

## Setup after approval

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Place only the OAuth token obtained for the approved application in `.env`.

Example manual query:

```bash
python -m reddit_sentiment search --query "NVDA" --subreddit stocks --limit 10
```

The command prints normalized JSON to stdout. The reference client itself does not persist the response.

## Compliance boundary

The repository documents the use case for which access is being requested. A Reddit approval for this application must not be treated as authorization for a different use case. Commercial use, research programs, model training, broader collection, additional communities, or materially different functionality require whatever additional permission Reddit requires at that time.

Use is subject to Reddit's Responsible Builder Policy, Developer Terms, Data API Terms, the approved App Review scope, and applicable law.

## License

MIT. The software license does not grant permission to access or use Reddit data outside Reddit's terms or an approved use case.
