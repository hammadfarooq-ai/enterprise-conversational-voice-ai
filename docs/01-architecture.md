# 01 - System Architecture

## Goal

Build a production-grade outbound Conversational Voice AI system for the US market with sub-second streaming interaction and high-volume concurrency.

## High-Level Diagram

```text
Vicidial -> Dialer Control API -> Asterisk PBX/SIP -> Media Gateway (RTP)
       -> Orchestrator (STT -> LLM -> TTS)
       -> Media Gateway -> Asterisk live call

Orchestrator -> Redis (session memory, low latency)
Orchestrator -> Supabase (transcripts, compliance, analytics)
Media/Recordings -> S3
```

## Call Flow

1. Campaign starts in Vicidial.
2. `dialer-control` receives call start request and initializes call context in `orchestrator`.
3. `media-gateway` receives RTP audio from Asterisk and forwards PCM frames over WebSocket to `orchestrator`.
4. `orchestrator` streams audio to Deepgram for transcription.
5. Final user utterances are processed by OpenAI with conversation memory context.
6. Assistant text is synthesized by ElevenLabs.
7. Synthesized audio is streamed back toward media-gateway and injected into call media path.
8. Events and turns are persisted to Supabase; recordings are pushed to S3.

## Design Principles

- Async and non-blocking across all services
- Event-driven microservice boundaries
- Stateless compute services with externalized state
- Horizontal scaling with shared Redis/Supabase
- Retry logic and graceful fallback behavior

## Service Responsibilities

- `dialer-control`: telephony orchestration APIs and external dialer hooks
- `media-gateway`: RTP ingest/egress, codec conversion, WS bridge
- `orchestrator`: AI conversation logic, memory, compliance checks
- `frontend`: operator controls and near-real-time operational visibility

## Data Plane vs Control Plane

- Data Plane: RTP/PCM/TTS audio streaming path (`media-gateway` + `orchestrator`)
- Control Plane: call lifecycle APIs, campaign actions, dispositions (`dialer-control`)
