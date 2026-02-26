# Enterprise Conversational Voice AI

Production-grade outbound Conversational Voice AI platform for the US market, integrating:

- Vicidial predictive dialer
- Asterisk PBX and SIP trunk
- Async AI orchestration (Deepgram + OpenAI + ElevenLabs)
- Supabase for call/transcript/compliance data
- Amazon S3 for recordings
- Docker/Kubernetes deployment patterns

## Project Structure

```text
enterprise-conversational-voice-ai/
  docs/
  frontend/
  infra/
  services/
    dialer-control/
    media-gateway/
    orchestrator/
  shared/
  sql/
  .env.example
  docker-compose.yml
```

## Quick Start

1. Copy environment template:

```bash
cp .env.example .env
```

2. Fill secrets and URLs in `.env`:
- OpenAI
- Deepgram
- ElevenLabs
- Supabase
- AWS S3
- Vicidial/Asterisk

3. Start services:

```bash
docker compose up --build
```

4. Access:
- Frontend dashboard: `http://localhost:3000`
- Dialer Control API: `http://localhost:8020`
- Orchestrator: `http://localhost:8000`
- Media Gateway: `http://localhost:8010`

## Documentation

See full docs in `docs/`:

- `docs/01-architecture.md`
- `docs/02-services.md`
- `docs/03-api-reference.md`
- `docs/04-setup-and-run.md`
- `docs/05-compliance.md`
- `docs/06-deployment-and-scaling.md`
- `docs/07-security-and-latency.md`
- `docs/08-troubleshooting.md`

## Current Implementation Status

- Complete monorepo scaffold created
- Async microservices with real-time streaming pipeline hooks
- RTP ingest and WebSocket bridge implemented
- AI pipeline service abstraction implemented
- Dashboard and call-control APIs implemented
- SQL schema and deployment manifests implemented

## Next Integration Tasks

1. Wire real Asterisk ARI ExternalMedia bridge channels
2. Connect Supabase and S3 write paths end-to-end
3. Add production authN/authZ for APIs and dashboard
4. Add observability stack (Prometheus/Grafana/Loki/OTEL)
5. Add load/performance test suite for concurrent calls
