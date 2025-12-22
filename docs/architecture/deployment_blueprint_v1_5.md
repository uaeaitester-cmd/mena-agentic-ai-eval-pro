MENA Eval Platform – Version 1.5
Production Deployment Blueprint
Enterprise‑Grade Architecture for On‑Premise and Cloud Environments

1. Introduction
This document provides the complete production deployment architecture for MENA Eval Platform v1.5, designed for enterprise environments such as banks, government agencies, telecom operators, and AI solution providers across the MENA/GCC region.

The blueprint defines:

System architecture

Deployment topology

Scaling strategy

Performance expectations

Security and governance requirements

Monitoring and observability

Infrastructure components

Production readiness criteria

This document is based on:

The finalized v1.5 architecture

Full integration test results (52/52 passing)

Complete performance benchmarking (Sections 1–3)

Enterprise requirements for AI governance and multilingual evaluation (EN/FA/AR)

2. High‑Level Architecture Overview
The platform is composed of the following core components:

API Gateway / Load Balancer

API Service (REST v1.5)

Evaluation Worker Service (Pipeline v1.5)

Semantic Model Service (Embedding & Semantic Metrics)

Queue Layer (Batch & High‑Load Processing)

Cache Layer (Embeddings & Evaluation Caching)

History & Metadata Store (Database)

Monitoring & Logging Stack

Security & Access Control Layer

2.1 Data Flow Summary
Code
Client → Load Balancer → API Service
    → (Sync) Evaluation Worker → Semantic Model Service → Cache → DB
    → (Async/Batch) Queue → Worker → Semantic Service → Cache → DB
    → Logs & Metrics → Monitoring Stack
3. API Layer
3.1 Responsibilities
Expose all v1.5 endpoints:

/api/v1/evaluate

/api/v1/batch_evaluate

/api/v1/history/*

/api/v1/catalogs/*

/api/v1/health

Authentication & authorization

Rate limiting & throttling

Input validation

Response schema enforcement

Basic request logging

3.2 Deployment Model
Technology: FastAPI (recommended), ASGI server (uvicorn/gunicorn)

Topology: 2–3 replicas behind a load balancer

Scaling: Horizontal scaling preferred

Stateless: No session stored on instances

3.3 Rate Limiting
Per API key:

5–10 req/sec for single evaluations

1–2 req/sec for batch evaluations

Global throttling to prevent overload

4. Evaluation Worker Service
4.1 Responsibilities
Each worker executes the full v1.5 evaluation pipeline:

Preprocessing (normalization, language detection, tokenization)

Rule‑based metrics (quality, fluency, toxicity, bias)

AI‑powered metrics (semantic_quality, semantic_fluency, ml_toxicity, ml_bias)

Scenario‑based scoring

Confidence calculation

Postprocessing

Optional history persistence

4.2 Deployment
Multiple worker processes per instance

Connects to:

Semantic Model Service

Cache

Queue (for batch)

History DB

4.3 Scaling Strategy
Horizontal scaling (add more worker instances)

Vertical scaling (increase CPU/RAM per instance)

4.4 Performance Expectations (Based on Benchmarking)
Single evaluation: ~39ms

Large batch throughput: ~9.5 items/sec

Concurrency peak: ~8–9 req/sec per deployment unit

5. Semantic Model Service
5.1 Purpose
Benchmarking identified semantic processing as the primary bottleneck:

~50% of total latency

~341MB memory footprint

Significant concurrency degradation

Therefore, semantic processing is isolated into a dedicated service.

5.2 Responsibilities
Host and manage embedding/semantic models

Provide internal API for:

Embedding generation

Semantic metric computation

Perform:

Batching

Caching

Warmup

Health checks

5.3 API Interface
POST /semantic/embed

Input: texts: List[str], optional lang

Output: embeddings: List[List[float]]

GET /semantic/health

Model readiness, memory usage, warmup status

5.4 Deployment
1–2 replicas

CPU or GPU (optional for v2.0)

Memory: 2–8GB depending on model size

6. Queue Layer
6.1 Purpose
Used for:

Batch evaluations

High‑load scenarios

Long‑running jobs

Load leveling

6.2 Technology Options
Redis Queue (recommended)

RabbitMQ

AWS SQS / Azure Queue (cloud deployments)

6.3 Batch Flow
Client submits batch

API enqueues job

Worker dequeues and processes

Results stored in DB

Client retrieves via history or job status

7. Cache Layer
7.1 What Is Cached
Embeddings (primary)

Evaluation results (optional)

Static catalogs and configs

7.2 Technology
Redis (in‑memory)

TTL recommended for embeddings (e.g., 7 days)

7.3 Benefits
Reduced semantic load

Lower latency

Improved batch performance

8. Data Storage
8.1 History Store
Stores:

Inputs (or hashed inputs)

Model outputs

All 8 metrics

Confidence

Scenario

Timestamps

Project/user identifiers

Technology: PostgreSQL (recommended)

8.2 Catalogs & Configurations
Scenario definitions

Model metadata

Weight configurations

Feature flags

Stored in DB or versioned config files.

9. Security & Governance
9.1 Authentication
API keys (minimum requirement)

Optional OAuth/OpenID Connect

9.2 Data Protection
Full On‑Premise support (no external calls)

TLS/HTTPS mandatory

DB encryption recommended

Optional PII masking

9.3 Audit Logging
Every evaluation request logged

Config changes logged

Retention: 6–12 months

10. Observability
10.1 Logging
Structured JSON logs

Request ID, latency, status code, errors

Separate logs for:

API

Workers

Semantic Service

10.2 Monitoring Metrics
API latency (avg, p95, p99)

Worker evaluation duration

Semantic model latency

Queue depth

CPU/memory usage

Error rate

10.3 Alerting Thresholds
p95 latency > 500ms

Memory > 80%

Error rate > 1%

Queue depth > threshold

Semantic service unresponsive

11. Sizing & Capacity Planning
11.1 Benchmark‑Based Reality
Single eval: 39ms

Batch throughput: 9.5 items/sec

Concurrency peak: 8–9 req/sec

Peak memory: 1.2GB

11.2 Minimum Deployment (MVP)
API: 2 cores, 1GB RAM

Workers: 4 cores, 1.7GB RAM

Semantic Service: 4 cores, 2GB RAM

Redis (queue + cache)

PostgreSQL

Lightweight monitoring stack

11.3 Enterprise Deployment (Recommended)
API: 2–3 replicas (2–4 cores each)

Workers: 3–5 replicas (4 cores each)

Semantic Service: 1–2 replicas (CPU or GPU)

Redis (HA)

PostgreSQL (HA)

Full monitoring stack

Targets:

p95 < 500ms

≥50 req/sec with horizontal scaling

Memory < 80% under load

12. Failure Handling & Resilience
12.1 Failure Modes
Semantic service slowdown

Queue overload

Worker crash

DB unavailability

API overload

12.2 Mitigation
Circuit breaker

Retry with exponential backoff

Graceful degradation (rule‑based only mode)

Health checks & auto‑restart

Load shedding

13. Deployment Models
13.1 On‑Premise (Primary Target)
Fully isolated deployment

No outbound internet

Integration with internal security systems

13.2 Cloud
Azure / AWS / GCP

Kubernetes or container‑based deployment

Hybrid options supported

14. Production Readiness Checklist
Functionality
[ ] All v1.5 endpoints operational

[ ] Confidence scoring validated

[ ] Multilingual support verified

Performance
[ ] Single eval latency meets benchmark

[ ] Batch throughput validated

[ ] Concurrency behavior understood and accepted

Security
[ ] TLS enabled

[ ] API keys configured

[ ] Audit logging active

Reliability
[ ] Health checks configured

[ ] Retry & circuit breaker policies defined

[ ] Fallback mode available

Monitoring
[ ] Dashboards deployed

[ ] Alerts configured

Operations
[ ] Backup strategy defined

[ ] Log retention policy set

[ ] Deployment & rollback procedures documented

15. Roadmap Alignment (v2.0 & Dashboard)
This architecture is intentionally designed to support:

v2.0 Enhancements
GPU acceleration

8‑bit/4‑bit quantization

Async pipeline

Worker pools

Advanced batching

Dashboard v1.0
Real‑time metrics visualization

Evaluation history browsing

Scenario configuration UI

Project‑level analytics

End of Document