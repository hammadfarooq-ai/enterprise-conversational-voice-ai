# 08 - Troubleshooting Guide

## Service Does Not Start

Checks:

1. Confirm `.env` exists and has required keys
2. Run `docker compose config` to validate compose file
3. Check logs:

```bash
docker compose logs -f orchestrator
docker compose logs -f media-gateway
docker compose logs -f dialer-control
```

## No Audio in Conversation

Possible causes:

- RTP not reaching media-gateway UDP port
- Payload codec mismatch (mu-law vs expected format)
- WebSocket disconnect between media-gateway and orchestrator
- Outbound RTP destination not configured on bridge start

Actions:

- Validate RTP ingress on `5004/udp`
- Verify `media_orch_ws_url` in env
- Confirm bridge endpoint called with correct call ID

## STT/LLM/TTS Failures

Checks:

- API keys valid and active
- provider endpoint reachable from runtime network
- model and voice IDs configured correctly

Actions:

- inspect orchestrator logs for retry/fallback activity
- verify provider quotas and account limits

## Call Ends Unexpectedly

Possible causes:

- opt-out phrase detected
- unhandled exception in pipeline task
- websocket disconnected from upstream

Actions:

- inspect logs for `call_id`
- inspect compliance event traces
- verify dialer-control end-call event path

## Dashboard Cannot Trigger Calls

Checks:

- frontend can reach dialer-control URL
- CORS/network rules in deployment path
- dialer-control health endpoint is up

## Recommended Monitoring Alerts

- High websocket disconnect rate
- LLM retry burst above threshold
- TTS timeout error rate
- RTP packet loss and jitter anomaly
- Call start success rate drop
