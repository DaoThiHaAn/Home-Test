** OptiBot Mini Clone**
Daily scraper and Gemini File Search loader for OptiSigns support articles.

# Setup

1. Create a Google AI Studio API key.
2. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

# Run Locally

Run once from Python:

```bash
python main.py
```

Or run once with Docker:

```bash
docker build -t optibot .
docker run -e API_KEY="YOUR_KEY_HERE" optibot-scraper
```


# Google AI Studio Agent

In AI Studio, create a Playground chat/agent with this system prompt:

```text
You are OptiBot, the customer-support bot for OptiSigns.com.
* Tone: helpful, factual, concise.
* Only answer using the uploaded docs.
* Max 5 bullet points; else link to the doc.
* Cite up to 3 "Article URL:" lines per reply.
```

# Daily Job

`.github/workflows/daily_jobs.yml` runs the Docker job daily at 02:00 UTC and uploads
`last_run.txt` as the daily run artifact. Configure repository secrets:

```text
GEMINI_API_KEY
```

Each run re-scrapes articles, writes Markdown to `articles_markdown`, compares each
`slug_updatedTimestamp.md` against Gemini File Search documents, uploads only new or
updated files, and logs `added`, `updated`, `skipped`.

Chunking strategy: Gemini File Search automatically splits Markdown into chunks for embedding.

Daily job logs: add the GitHub Actions run URL here after the first scheduled/manual run.

Screenshot: add the AI Studio answer screenshot here before submission.
