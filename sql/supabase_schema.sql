create extension if not exists "uuid-ossp";

create table if not exists calls (
  id uuid primary key default uuid_generate_v4(),
  lead_phone text not null,
  campaign_name text not null,
  started_at timestamptz not null default now(),
  ended_at timestamptz,
  disposition text not null default 'in_progress',
  sentiment_avg numeric(5,2) default 0,
  opt_out boolean not null default false,
  recording_s3_uri text,
  metadata jsonb not null default '{}'::jsonb
);

create table if not exists call_turns (
  id uuid primary key default uuid_generate_v4(),
  call_id uuid not null references calls(id) on delete cascade,
  speaker text not null check (speaker in ('user', 'assistant', 'system')),
  text text not null,
  sentiment numeric(5,2) default 0,
  latency_ms int default 0,
  created_at timestamptz not null default now()
);

create table if not exists compliance_events (
  id uuid primary key default uuid_generate_v4(),
  call_id uuid not null references calls(id) on delete cascade,
  event_type text not null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_call_turns_call_id_created_at
on call_turns (call_id, created_at);

create index if not exists idx_compliance_events_call_id_created_at
on compliance_events (call_id, created_at);
