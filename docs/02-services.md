# 02 - Microservices Breakdown

## Orchestrator (`services/orchestrator`)

### Purpose

Runs real-time AI call intelligence pipeline:

- Speech-to-Text (Deepgram)
- LLM reasoning (OpenAI)
- Text-to-Speech (ElevenLabs)
- Conversation memory and compliance logic

### Key Files

- `app/main.py`: FastAPI app and WebSocket endpoint for call media
- `app/pipeline.py`: call loop and streaming orchestration
- `app/session_manager.py`: Redis-backed turn memory
- `app/compliance.py`: opt-out logic and disclosure helpers
- `app/deepgram_stream.py`: live STT
- `app/openai_stream.py`: streaming LLM output
- `app/elevenlabs_stream.py`: chunked TTS stream

### Important Runtime Behavior

- Maintains per-call queues for inbound PCM and outbound TTS bytes
- Drops interim transcripts and reacts on final transcripts
- Enforces opt-out logic before response generation
- Uses retry policy for LLM request robustness

## Media Gateway (`services/media-gateway`)

### Purpose

Bridges telephony RTP with orchestrator WebSocket media stream.

### Key Files

- `app/rtp_receiver.py`: RTP UDP listener and packet parser
- `app/codecs.py`: mu-law <-> linear16 conversion
- `app/ws_bridge.py`: RTP-to-WebSocket stream bridge
- `app/rtp_sender.py`: RTP packetization for outbound audio path
- `app/main.py`: service API and lifecycle

### Important Runtime Behavior

- Receives RTP from Asterisk and converts payload to linear16 frames
- Streams frames to orchestrator over persistent WebSocket
- Can send synthesized linear16 back as RTP to telephony leg

## Dialer Control (`services/dialer-control`)

### Purpose

Controls outbound call lifecycle and external integrations.

### Key Files

- `app/main.py`: `/calls/start` and `/calls/end`
- `app/vicidial_client.py`: disposition update callouts
- `app/asterisk_ari_client.py`: ARI originate hook
- `app/config.py`: external endpoint settings

### Important Runtime Behavior

- On start: initializes orchestrator state and starts media bridge
- On end: closes orchestrator call context and updates dialer disposition

## Frontend (`frontend`)

### Purpose

Operator dashboard for triggering outbound calls and reviewing events.

### Key Files

- `src/App.jsx`: call control UI
- `src/api.js`: backend API wrapper
- `Dockerfile`: production static build served by NGINX
