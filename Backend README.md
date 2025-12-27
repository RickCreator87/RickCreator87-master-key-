# RickCreator87‑master‑key — Backend README

A concise, deployment‑ready README for the RickCreator87‑master‑key AI operations backend. This document covers architecture, environment and secrets, quickstart (Docker), deployment options (Kubernetes), health checks, observability, and operational checklists.

## Table of contents
- Overview
- Architecture & routes
- Prerequisites
- Environment & secrets (template)
- Quickstart (Docker Compose)
- Dockerfile / Build
- Kubernetes deployment (recommended)
- Health checks & readiness probes
- Observability (metrics, logs, traces)
- Security & governance notes
- Backup, migrations & rollbacks
- Troubleshooting & smoke tests
- Links & next steps

## Overview
This backend receives GitHub App webhooks, verifies them, enriches context, routes tasks to the correct AI model(s), enforces governance, logs actions for audit, and posts results back to GitHub (checks, comments). It is designed to be small, auditable, and deployable to container platforms or Kubernetes.

Core responsibilities:
- Verify GitHub webhook signatures
- Authenticate as the GitHub App (JWT flow)
- Load installation tokens per installation
- Route tasks to models (DeepSeek, Ollama, OpenAI/Azure) via a policy
- Persist audit trails and telemetry
- Expose health, readiness, and metrics endpoints

## Architecture & routes
Recommended HTTP routes:
- POST /github/webhook — receive & verify webhooks (single entrypoint)
- POST /v1/master/analyze-pr
- POST /v1/master/repo-health
- POST /v1/master/generate-docs
- POST /v1/master/ci-advice
- POST /v1/master/onboard-repo
- GET  /health — basic liveness
- GET  /ready  — readiness checks (DB, model endpoints, key stores)
- GET  /metrics — Prometheus metrics

Event lifecycle (summary):
1. Verify signature using GITHUB_WEBHOOK_SECRET
2. Parse event, load installation context (installation ID)
3. Classify and enqueue or handle synchronously
4. Apply governance (allowlist/blocklist, approval policies)
5. Select model(s) via routing policy & call model(s)
6. Persist audit and post back to GitHub

## Prerequisites
- Container runtime (Docker) or Kubernetes cluster
- Secret manager (Vault, AWS Secrets Manager, Google Secret Manager) or K8s Secrets
- Postgres (or other durable DB) recommended for audit/history
- Redis (or similar) for job queue (optional)
- Observability backend (Prometheus + Grafana recommended), plus Sentry/Datadog option
- Domain + TLS for webhook endpoint (Let's Encrypt, ALB, etc.)

## Environment & secrets
Use the provided `.env.template` (included) as a starting point. All secrets must be stored in a secret manager in production — do not commit them.

Important variables:
- GITHUB_APP_PRIVATE_KEY (PEM)
- GITHUB_APP_ID
- GITHUB_CLIENT_ID
- GITHUB_CLIENT_SECRET
- GITHUB_WEBHOOK_SECRET
- JWT_SIGNING_KEY (optional)
- AI_TOKEN_DEEPSEEK
- AI_TOKEN_OPENAI / AZURE_CREDENTIALS
- OLLAMA_HOST_URL, OLLAMA_AUTH
- DATABASE_URL (postgres://...)
- REDIS_URL (optional)
- SENTRY_DSN (optional)
- PROMETHEUS_SCRAPE (true/false)
- LOG_LEVEL (info/debug)

See `.env.template` for full list.

## Quickstart — Docker Compose (development)
1. Copy `.env.template` to `.env` and fill in values.
2. Build image: docker build -t rick-master-key:latest .
3. Start services: docker-compose up -d

Minimal docker-compose (example snippet):
```yaml
version: "3.8"
services:
  app:
    image: rick-master-key:latest
    env_file: .env
    ports:
      - "8080:8080"
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: masterkey
      POSTGRES_USER: masterkey
      POSTGRES_PASSWORD: example
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

Note: In dev, you can use ngrok/Cloudflare tunnel to expose the webhook endpoint.

## Dockerfile (recommended)
- Use a small base (e.g., python:3.11-slim or node:18-slim)
- Install only required runtime deps
- Build artifacts in a builder stage if compiled
- Set non-root user
- Healthcheck (curl http://localhost:8080/health)

Example:
- COPY requirements, install, expose 8080, CMD to start server

## Kubernetes deployment (production)
Key Kubernetes considerations:
- Use Deployment with liveness/readiness probes (see Health checks)
- Use HorizontalPodAutoscaler (HPA) with CPU/memory or custom metrics
- Store secrets in Kubernetes Secrets or reference external secret manager
- Use PodDisruptionBudgets for high availability
- Use NetworkPolicy to limit egress (to model hosts, secret manager)
- Use RBAC for service account with least privileges

Example resources to include:
- Namespace
- ConfigMap (non-secret config)
- Secret (GITHUB_APP_PRIVATE_KEY, tokens)
- Deployment + Service
- Ingress (TLS)
- HorizontalPodAutoscaler
- PodDisruptionBudget
- ServiceMonitor (Prometheus Operator) or Prometheus scrape config

Minimal Deployment snippet (conceptual):
- container:
  - livenessProbe: GET /health
  - readinessProbe: GET /ready
  - resources: requests/limits

## Health checks & readiness probes
Expose:
- GET /health — returns 200 if process alive (minimal)
- GET /ready — performs deeper checks:
  - DB connectivity
  - Secret manager reachability
  - Model endpoints reachable (Ollama, OpenAI) — or cached last-success timestamp
  - GitHub API reachable & rate limit info fetch (optional)
Return structured JSON:
{
  "status":"ok",
  "checks": {
    "db":"ok",
    "redis":"ok",
    "models":{"ollama":"ok","openai":"ok"},
    "lastWebhookProcessed":"2025-12-01T12:00:00Z"
  }
}

Kubernetes probe configs:
- livenessProbe:
  - httpGet: /health
  - initialDelaySeconds: 10
  - periodSeconds: 30
- readinessProbe:
  - httpGet: /ready
  - initialDelaySeconds: 5
  - periodSeconds: 15
- Consider configuring a separate /startup probe if initialization is lengthy

## Observability (metrics, logs, traces)
Metrics:
- Expose Prometheus metrics at GET /metrics
- Instrumentation suggestions:
  - Counter: github_events_received_total{event_type}
  - Counter: model_calls_total{model, outcome}
  - Histogram: model_call_duration_seconds{model}
  - Gauge: active_jobs
  - Gauge: queue_length

Tracing:
- Add OpenTelemetry tracing with sampling rules
- Instrument: webhook processing span, model call spans, GitHub API spans
- Export to OTLP collector → Jaeger/Tempo/Datadog/Lightstep

Logs:
- Structured JSON logs (timestamp, level, request_id, installation, repo, event_type, action)
- Include a request_id or trace id
- Log levels configurable via LOG_LEVEL
- Send logs to central collector (Datadog, ELK, Loki)

Alerting & dashboards:
- Alerts:
  - High error rate for /github/webhook
  - model_call_duration > threshold for critical models
  - readiness check failing
  - queue length > threshold
- Dashboards:
  - Webhook throughput & latencies
  - Model usage & cost
  - Audit actions over time
  - Health overview

Examples:
- Prometheus scrape config and ServiceMonitor for the app
- Grafana dashboard showing metrics above

## Security & governance
- Store GitHub private key and AI tokens in a secrets vault
- Enforce least privileged GitHub App permissions (see recommended matrix below)
- Human approval for destructive org-level actions (protected path)
- Audit all automated changes with immutable event log
- Rate limit and circuit-break on model calls and GitHub API
- Rotate keys and tokens regularly

Recommended GitHub App scopes (example)
- Contents: read-only unless repo bootstrap needs write
- Pull requests: read & write (if commenting, labeling)
- Issues: read & write (if commenting)
- Checks: read & write
- Administration scopes only if required (avoid unless absolutely necessary)

## Backup, migrations & rollback
- Run DB migrations as a job with locking
- Back up audit DB regularly (daily snapshots)
- Provide a rollback image tag and run canary before full rollout
- Store migration scripts in VCS and CI job to run with approval

## CI/CD
- Build artifact in CI with reproducible tags
- Run static checks & integration tests
- Deploy via GitOps (ArgoCD) or pipeline with staged environments (canary → prod)
- Use image signing if required

## Troubleshooting & smoke tests
Smoke tests to run post-deploy:
- POST a sample webhook (signed) and confirm processing
- GET /ready and /metrics
- Trigger a model call via internal test route
- Confirm an audit log entry in DB

Common issues:
- Webhook 401: check GITHUB_WEBHOOK_SECRET mismatch
- GitHub API 403: check installation token/scopes
- Model timeouts: increase timeouts and check model endpoint health

## Next steps
- Generate Kubernetes manifests (I can produce them)
- Provide GitHub App permission matrix
- Add example Prometheus & Grafana dashboards
- Build deployment pipeline templates (GitHub Actions/ArgoCD)

