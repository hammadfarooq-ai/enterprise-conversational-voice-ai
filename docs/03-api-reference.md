# 03 - API Reference

## Dialer Control Service

Base URL: `http://localhost:8020`

### `GET /health`

Response:

```json
{
  "ok": true,
  "service": "dialer-control"
}
```

### `POST /calls/start`

Request:

```json
{
  "call_id": "call-123",
  "lead_phone": "+15550001111",
  "campaign_name": "insurance-q1",
  "metadata": {
    "source": "dashboard"
  }
}
```

Response:

```json
{
  "ok": true,
  "call_id": "call-123"
}
```

### `POST /calls/end`

Request:

```json
{
  "call_id": "call-123",
  "disposition": "completed"
}
```

Response:

```json
{
  "ok": true,
  "call_id": "call-123",
  "disposition": "completed"
}
```

## Orchestrator Service

Base URL: `http://localhost:8000`

### `GET /health`

Response:

```json
{
  "ok": true,
  "service": "orchestrator"
}
```

### `POST /calls/start`

Initializes call context in Redis.

### `POST /calls/end`

Terminates active call tasks and session state.

### `WS /ws/media/{call_id}`

Bidirectional binary stream endpoint:

- Inbound: linear16 PCM audio chunks
- Outbound: synthesized audio chunks (provider format currently passthrough)

## Media Gateway Service

Base URL: `http://localhost:8010`

### `GET /health`

Response:

```json
{
  "ok": true,
  "service": "media-gateway"
}
```

### `POST /calls/{call_id}/bridge/start`

Starts RTP-to-orchestrator media bridge for a call.

Optional query params:

- `asterisk_rtp_host`
- `asterisk_rtp_port`
