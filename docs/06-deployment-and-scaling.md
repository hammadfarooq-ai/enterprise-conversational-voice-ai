# 06 - Deployment and Scaling

## Docker Deployment

Primary local/prototype deployment:

```bash
docker compose up --build
```

Services started:

- `redis`
- `orchestrator`
- `media-gateway`
- `dialer-control`
- `frontend`

## Kubernetes Deployment

Manifests are available in `infra/k8s/`:

- `orchestrator-deploy.yaml`
- `media-gateway-deploy.yaml`
- `hpa.yaml`

Apply sequence:

```bash
kubectl apply -f infra/k8s/orchestrator-deploy.yaml
kubectl apply -f infra/k8s/media-gateway-deploy.yaml
kubectl apply -f infra/k8s/hpa.yaml
```

## Horizontal Scaling Strategy

- Scale `orchestrator` by active call load and CPU
- Scale `media-gateway` by RTP port and packet processing load
- Keep services stateless; use Redis for session state sharing
- Use load balancer with WebSocket support for orchestrator ingress

## NGINX Reverse Proxy

Reference config in:

- `infra/nginx/nginx.conf`

Capabilities:

- Proxies `/api/` to dialer-control
- Proxies `/ws/` to orchestrator with upgrade headers

## Production Topology Recommendations

- Dedicated low-latency subnet for telephony/media services
- Separate control-plane and data-plane network paths
- Multiple media-gateway instances pinned close to PBX region
- Multi-AZ Redis and managed Postgres/Supabase reliability patterns
