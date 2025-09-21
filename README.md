# AI DevOps Agent

Webhook-driven bot that analyzes PRs, generates tests, runs pytest, and comments results.

## How it works
1) Webhook verifies signature
2) Fetch PR changed files at head SHA
3) Run pylint/flake8/bandit
4) Generate tests (placeholder)
5) Run pytest
6) Post Markdown summary to PR
