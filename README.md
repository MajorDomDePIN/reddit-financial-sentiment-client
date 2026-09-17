# Reddit Financial Sentiment Client

A small, read-only Python reference client for retrieving recent public Reddit discussions for **aggregate financial sentiment and topic analysis**.

The project is intentionally standalone. It does not contain or expose any private downstream analysis system. It demonstrates the Reddit-facing data-access layer that can be integrated into a separate application after Reddit Data API access has been approved.

## Scope

The client is designed to:

- authenticate through Reddit's approved OAuth flow;
- retrieve public posts from explicitly configured public subreddits;
- search for recent discussions about a user-supplied company, ticker, asset, or topic;
- normalize only the fields needed for aggregate topic/sentiment analysis;
- observe Reddit rate-limit response headers and back off rather than bypass limits;
- use a truthful, descriptive User-Agent;
- avoid automated posting, commenting, voting, messaging, moderation, or account creation;
- avoid user profiling and inference of sensitive characteristics;
- avoid use of Reddit content for model training or fine-tuning;
- minimize local retention of Reddit content.

This repository does **not** include API credentials. Credentials must be supplied locally through environment variables only after Reddit has approved the application's Data API access.

## Intended use

The intended use is low-volume, read-only analysis of public discussions as one signal in an external information-analysis workflow. For example, a query for a public company or ticker can retrieve recent matching submissions from configured investing communities and return normalized records that a separate local application may classify or summarize at an aggregate level.

The application is not intended to target, contact, score, or build profiles of individual Redditors.

## Data minimization

The normalized output intentionally omits author identity. By default, retrieved records are processed in memory and are not persistently stored by this reference client. Applications integrating this client should retain Reddit content only when necessary for their approved functionality, routinely refresh/delete cached content, and honor Reddit deletion requirements.

See [DATA_HANDLING.md](DATA_HANDLING.md) for details.

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure the approved OAuth client values in `.env`. Do not commit `.env`.

## Example

```bash
python -m reddit_sentiment search --query "NVDA" --subreddit stocks --limit 10
```

The command emits normalized JSON to stdout. It does not perform sentiment inference itself and does not persist the retrieved Reddit content.

## API-access status

This repository is prepared for an application for Reddit Data API access. It must not be interpreted as authorization to access Reddit's Data API before Reddit grants approval.

## Policy

Use of this software must comply with Reddit's Responsible Builder Policy, Developer Terms, Data API Terms, the approved use case, and applicable law. Do not use it to circumvent access controls or rate limits.

## License

MIT. See [LICENSE](LICENSE).
