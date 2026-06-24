# An aquatic API

A lightweight, quirky **REST API** that delivers statistics about various fishes. Built with **FastAPI** and integrated with external data sources for fresh content on every request.

## Features

- **Live Data** — Fetches real fish facts from certified sources (no hardcoded tidbits)
- **Rate Limiting** — Protected with SlowAPI (30 requests/min per IP)
- **Smart Caching** — In-memory caching for better performance
- **CORS Enabled** — Ready to be consumed by frontend apps and static websites
- **Clean Architecture** — Environment variables with error handling and structured code
- **Easy Deployment** — Ready for Render, Railway, Fly.io, Docker, etc.

## Purpose

This project serves as an exercise to practice:

- FastAPI development
- Secure API key management
- Rate limiting & caching
- Git branching workflow (`main` → `staging` → `dev` → `feature/`)
- Connecting backend APIs to static frontends

## Endpoints

- `GET /fact` — Get a random fresh fish fact
- `GET /search?q=clownfish` — Search facts by keyword
- `GET /` — API information

## Tech Stack

- **FastAPI**
- **Python 3.11+**
- **SlowAPI** (rate limiting)
- **Requests** + **python-dotenv**
- **Uvicorn**

---

The sole purpose to build this was to study the fetching modern Python API!
