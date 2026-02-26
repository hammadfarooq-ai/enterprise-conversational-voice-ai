# 05 - Compliance Design (US Outbound)

## Scope

This system must enforce outbound calling compliance controls for US operations, including opt-out handling, recording disclosures, and auditable event history.

## Core Controls

## 1) Recording Disclosure

At call start, assistant should state:

> "This call may be recorded for quality and training. You can ask us to stop calling at any time."

Implementation anchor:

- `services/orchestrator/app/compliance.py`

## 2) Opt-Out Detection and DNC

Detected terms include:

- stop
- unsubscribe
- remove me
- do not call
- dnc
- opt out

When detected:

1. Confirm request and end conversation politely.
2. Mark lead as DNC in internal store.
3. Persist compliance event in Supabase.
4. Propagate disposition back to dialer.

## 3) Calling Window Logic

Required for production:

- Resolve lead local timezone by area code/profile data
- Block calls outside legal campaign window by state/federal policy
- Log denied attempts in compliance events table

## 4) Consent and Audit Trail

Store and retain:

- consent source
- consent timestamp
- revocation timestamp
- campaign and script version
- call outcome and disposition

Use immutable append-only compliance events in `compliance_events`.

## 5) Human Escalation

If model fails repeatedly or sensitive/legal topic appears:

- transfer to human agent
- log escalation reason
- preserve transcript boundary for QA review

## Important

Regulatory requirements vary by jurisdiction and can change. Validate with legal counsel before go-live.
