# ARP Template Composite Executor

Use this repo as a starting point for building an **ARP compliant Composite Executor** service.

This minimal template implements the Composite Executor API using only the SDK packages:
`arp-standard-server`, `arp-standard-model`, and `arp-standard-client`.

Composite execution internals (decomposition/mapping/evaluation) are intentionally implementation-defined. This template keeps the protocol surface small so you can plug in your preferred framework while preserving spec-aligned request/response envelopes.

Implements: ARP Standard `spec/v1` Composite Executor API (contract: `ARP_Standard/spec/v1/openapi/composite-executor.openapi.yaml`).

## Requirements

- Python >= 3.10

## Install

```bash
python3 -m pip install -e .
```

## Local configuration (optional)

For local dev convenience, copy the template env file:

```bash
cp .env.example .env.local
```

`src/scripts/dev_server.sh` auto-loads `.env.local` (or `.env`).

## Run

- Composite Executor listens on `http://127.0.0.1:8083` by default.

```bash
python3 -m pip install -e '.[run]'
python3 -m arp_template_composite_executor
```

> [!TIP]
> Use `bash src/scripts/dev_server.sh --host ... --port ... --reload` for dev convenience.

## Using this repo

To build your own composite executor, fork this repository and replace the composite engine while preserving request/response semantics.

If all you need is to change composite behavior, edit:
- `src/arp_template_composite_executor/executor.py`

Outgoing client wrapper (composite -> coordinator):
- `src/arp_template_composite_executor/run_coordinator_client.py`

### Default behavior

- `begin_composite_node_run` always returns `accepted=true` with a placeholder message.
- No background execution is performed by default (template is protocol-surface-first).

### Notes on API surface

- In `spec/v1`, the Composite Executor API is intentionally minimal (begin + health/version).
- More lifecycle surfaces (patch proposals, sub-NodeRun requests, completion reporting) can be layered on as the standard evolves.

## Quick health check

```bash
curl http://127.0.0.1:8083/v1/health
```

## Configuration

CLI flags:
- `--host` (default `127.0.0.1`)
- `--port` (default `8083`)
- `--reload` (dev only)

## Validate conformance (`arp-conformance`)

```bash
python3 -m pip install arp-conformance
arp-conformance check composite-executor --url http://127.0.0.1:8083 --tier smoke
arp-conformance check composite-executor --url http://127.0.0.1:8083 --tier surface
```

## Helper scripts

- `src/scripts/dev_server.sh`: run the server (flags: `--host`, `--port`, `--reload`).
- `src/scripts/send_request.py`: send a begin request from a JSON file.

  ```bash
  python3 src/scripts/send_request.py --request src/scripts/request.json
  ```

## Authentication

For out-of-the-box usability, this template defaults to auth-disabled unless you set `ARP_AUTH_MODE` or `ARP_AUTH_PROFILE`.

To enable JWT auth, set either:
- `ARP_AUTH_PROFILE=dev-secure-keycloak` + `ARP_AUTH_SERVICE_ID=<audience>`
- or `ARP_AUTH_MODE=required` with `ARP_AUTH_ISSUER` and `ARP_AUTH_AUDIENCE`

## Upgrading

When upgrading to a new ARP Standard SDK release, bump pinned versions in `pyproject.toml` (`arp-standard-*==...`) and re-run conformance.
