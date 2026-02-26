# 04 - Setup and Run

## Prerequisites

- Docker Desktop / Docker Engine
- API keys for Deepgram, OpenAI, ElevenLabs
- Supabase project + service role key
- Optional: AWS credentials for S3 recording storage

## 1) Environment Configuration

Create runtime env file:

```bash
cp .env.example .env
```

Fill all required values in `.env`:

- AI provider keys
- Supabase credentials
- Telephony endpoints (Vicidial/Asterisk)
- AWS keys and bucket

## 2) Build and Start

```bash
docker compose up --build
```

## 3) Verify Health

- `GET http://localhost:8000/health`
- `GET http://localhost:8010/health`
- `GET http://localhost:8020/health`
- Open `http://localhost:3000`

## 4) Basic End-to-End Dry Test

1. Open dashboard
2. Fill lead phone and campaign
3. Click `Start Outbound Call`
4. Confirm call ID appears and logs update
5. Click `End Call`

## 5) Production Readiness Checklist

- Replace placeholder telephony hooks with real ARI/AMI call logic
- Ensure call recording upload to S3 is enabled
- Ensure Supabase writes are enabled in orchestrator pipeline
- Configure TLS, VPN routes, and firewall rules
- Add centralized observability and alerting
