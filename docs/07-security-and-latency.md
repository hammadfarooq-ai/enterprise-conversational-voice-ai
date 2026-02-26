# 07 - Security and Latency

## Security Best Practices

## Network and Transport

- Use TLS for all public APIs and WebSocket ingress
- Use SIP-TLS and SRTP where carrier and PBX support it
- Place telephony/media nodes behind VPN and private networking
- Deny-by-default firewall policy; allow only required ports

## Secrets and Access

- Store secrets in secret manager, not in repository
- Rotate API keys on schedule
- Apply least-privilege IAM for S3 and runtime workloads
- Add RBAC for operator dashboard and admin endpoints

## Data Protection

- Encrypt recordings at rest (S3 SSE-KMS)
- Encrypt sensitive fields in database
- Mask PII in application logs
- Preserve immutable audit entries for compliance events

## Latency Optimization

## Pipeline-Level

- Stream audio frames continuously; avoid request-response batching
- Use incremental STT and incremental LLM response generation
- Trigger early TTS synthesis on partial model output where possible
- Keep short context windows and compact prompts

## Runtime-Level

- Use async queues with bounded sizes to avoid memory spikes
- Reuse long-lived provider connections where SDK allows
- Co-locate PBX, media-gateway, and orchestrator in low-latency zones
- Keep codec conversions minimal and telephony-native (8k where possible)

## Operational Metrics

Track and alert on:

- end-to-end turn latency (user speech end -> assistant audio start)
- STT partial/final latency
- LLM first-token latency
- TTS first-byte latency
- packet loss and jitter rate
