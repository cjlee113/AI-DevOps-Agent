# AI DevOps Agent

Webhook-driven bot that analyzes PRs, generates tests, runs pytest, and comments results.

## How it works
1) Webhook verifies signature
2) Fetch PR changed files at head SHA
3) Run pylint/flake8/bandit
4) Generate tests (placeholder)
5) Run pytest
6) Post Markdown summary to PR

## Quick start
1. Copy `.env.example` to `.env`
2. `docker compose up --build`
3. Expose `http://localhost:8080/webhook` (ngrok or deploy)

## Permissions
Use a fine-grained token with: pull requests:read, contents:read, issues:write.