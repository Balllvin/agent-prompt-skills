---
name: provider-routing
description: Use for any LLM or model-provider work in an app - model routing, adding or swapping a model, model ids, prices, or context limits, OpenRouter calls and zero-data-retention (ZDR) policy, xAI / Grok API and SDK calls, reasoning effort, search tools, structured output, prompt caching, STT, TTS, image, or voice, provider fallbacks and timeouts, or OpenAI docs lookups. Triggers include /provider-routing, /xai-api-mastery, /prompt-cache-optimization, /openai-docs, /speech, /transcribe, "xAI", "Grok API", "OpenRouter", "model routing", "which model", "model price", "prompt caching", "cache hit rate", "TTS", "transcribe". Load it before touching the router, an OpenRouter client, or any xAI service, even for a one-line change.
---

# Provider Routing

Use this skill for LLM, xAI, OpenRouter, search-tool, prompt-cache, STT/TTS, image, and voice-session work. Provider behavior drifts weekly and wrong request shapes fail silently into fallbacks, so every rule here exists to keep one owner and verify against live docs.

**Live facts only.** Every model id, price, context or output limit, rate limit, and supported parameter you write into code, a PR, or a reply comes from a live source read this session: the provider's models API (`GET https://openrouter.ai/api/v1/models`, the xAI models endpoint) or its current docs page. Cite the URL next to the fact. Memory and another model's map are not sources.

**OWASP LLM checks this skill owns** (from https://genai.owasp.org/llm-top-10/; the full threat pass lives in the `security` skill):
- LLM02 sensitive disclosure: the ZDR `provider` object stays on every OpenRouter chat completion. A model with no ZDR host gets an explicit, documented exception that still sends `data_collection: deny` and the host denylist. Prompts, keys, and user data never reach logs.
- LLM10 unbounded consumption: every provider call has a fixed hang timeout, a max output token cap, and a known cost per call. Do not cap an agent loop with a turn budget; bound each call instead.

## Index

| Need | Where |
|---|---|
| Find the owner, workflow | [Workflow](#workflow) |
| Presets, search, fallback | [Routing rules](#routing-rules) |
| OpenRouter ZDR, host denylist | [OpenRouter privacy](#openrouter-privacy-and-trusted-hosts-mandatory) |
| Add or replace a model, reasoning effort | [Adding or replacing a model](#adding-editing-or-replacing-a-model-mandatory) |
| xAI Chat SDK shape, traces, deadlines | [xAI sections](#xai-chat-vs-responses-request-shape-mandatory), [xai-api-mastery](references/xai-api-mastery.md) |
| Prompt caching, cache keys | [Prompt caching](#prompt-caching), [prompt-cache-optimization](references/prompt-cache-optimization.md) |
| STT/TTS/image/voice in the product | [Speech and voice rules](#speech-and-voice-rules) |
| OpenAI API docs lookup | [openai-docs](references/openai-docs.md) |
| One-off OpenAI TTS or transcription (dev tooling, not product) | [speech](references/speech/index.md), [transcribe](references/transcribe/index.md) |

## Workflow

1. Search the current routing path before editing, for example:
   - `rg -n "router|complete_with|response_json|structured|preset|fallback" <backend>/`
   - `rg -n "x_search|web_search|web_fetch|openrouter|xai|grok|reasoning_effort|use_encrypted_content" <backend>/`
   - `rg -n "stt|tts|voice|scheduler" <backend>/`
2. Locate the one canonical owner for each concern and edit there, not at callsites:
   - Text routing (preset to model and provider), model and effort maps, provider request builders.
   - OpenRouter privacy preferences (one builder that every OpenRouter call uses).
   - Provider admission and rate limiting (one shared scheduler).
   - Per-path RPC deadlines, reasoning capture, STT/TTS/image clients, realtime voice leases.
3. Verify provider-specific behavior with **live** official docs when request shape, tool support, model ids, search config, response metadata, **or supported reasoning effort values** is uncertain:
   - OpenRouter: `GET https://openrouter.ai/api/v1/models` → `reasoning.supported_efforts` (not memory, not another model's map).
   - xAI: `docs.x.ai` plus the installed `xai-sdk` (`IncludeOptionMap`, `chat.create` signature).
4. Keep provider details inside routing and transport layers. Callers ask for presets or tool intent, not raw model ids.
5. Add request-shape tests when changing model resolution, search tools, structured output, fallback order, timeout, token accounting, reasoning effort maps, or provider metadata.

## Routing rules

- Expose a small set of user-facing presets (for example `fast`, `medium`, `high`) and a few dedicated internal presets (for example `structured`, `tool`, `scanner`). Compatibility aliases resolve inside the router.
- Raw provider model ids never leak into service callsites except through an explicit user model-settings contract.
- Search evidence and structured formatting are different jobs. Do not send research-gathering calls to the structured formatter just because the caller wants JSON. Gather evidence on a search-capable preset, then repair JSON.
- OpenRouter `web_fetch` is a server tool (`openrouter:web_fetch`), opt-in only, never attached to the structured formatter. xAI has no URL-pinned fetch; xAI paths use `web_search` / `x_search`.
- xAI Batch is for async bulk work only, behind one client and an opt-in flag. REST: POST `/v1/batches`, POST `/v1/batches/{id}/requests` with `batch_requests`, GET results, POST `/v1/batches/{id}:cancel`.
- With search tools enabled, OpenRouter calls attach OpenRouter web search and direct xAI calls attach xAI SDK search tools.
- X Search intent requires an xAI-backed attempt; do not silently downgrade X evidence to generic web search.
- Provider failure metadata preserves failed-attempt provenance when a fallback succeeds.
- Fallback changes are tier-aware, provider-aware, and tested in both directions.
- A routing latency claim is not a result until the limiter is named and another explanation is ruled out with a run. See [Explain the number](../build/references/principle-explain-the-number.md).

## OpenRouter privacy and trusted hosts (mandatory)

| Rule | Detail |
| --- | --- |
| ZDR | Every OpenRouter `/chat/completions` sets `provider.zdr: true` through one shared preferences builder. Exceptions are named, documented, and still send deny plus the denylist. |
| No train/collect | `provider.data_collection: "deny"` |
| Denylist hosts | Keep an explicit `provider.ignore` list of first-party hosts your data policy forbids (for example by jurisdiction). Review it when you add models. |
| Allowed third parties | Inference hosts in jurisdictions your policy allows |
| No free routes | Never ship `:free`. Prefer `:nitro`, then `:exacto` as the reliability fallback |
| Author ≠ host | A model's author slug is not its host. Keep the model id; block the first-party host if policy requires |

Wire the same `provider` object into every OpenRouter path (plain completions and function-tool loops). Merge `require_parameters: true` into that object for JSON; do not replace the ZDR fields.

## Adding, editing, or replacing a model (mandatory)

Every catalog add, edit, replace, or fallback-slot change passes **both** gates before shipping.

### Gate A: ZDR and trusted hosts (OpenRouter models)

1. Fetch hosts: `GET https://openrouter.ai/api/v1/models/{model_id}/endpoints`.
2. Filter to ZDR endpoints (or cross-check `/api/v1/endpoints/zdr`).
3. Drop denylisted provider slugs.
4. **PASS** only if at least one host remains (prefer two independent third parties).
5. If the model backs a JSON preset, at least one surviving host must list `structured_outputs`. `require_parameters: true` plus a `json_schema` `response_format` returns a non-retryable 404 ("No endpoints found that can handle the requested parameters") otherwise.
6. Wire the `:nitro` variant.
7. Do not add models that only run on denylisted first parties.
8. Record the surviving hosts and the date in your routing notes.

Models served directly by their own provider SDK (for example xAI) skip this OpenRouter host audit.

### Gate B: reasoning levels and cost per intelligence

Reasoning effort is part of the model contract. Wrong values fail OpenRouter requests or silently drop thinking. **Never copy another model's map or reuse a `medium`/`high`/`xhigh` template.**

1. **Fetch live `reasoning.supported_efforts`** from `GET https://openrouter.ai/api/v1/models` (the model object's `reasoning` field). For xAI, read current xAI docs. Models differ: some support only `low`/`high`/`max`, some `high`/`xhigh`, some none. A model with no `supported_efforts` gets **no** reasoning payload; do not invent values.
2. **Map public tiers deliberately**: `fast` → lightest supported, `medium` → default or mid, `high` → deepest useful supported effort on that model.
3. **Update every registry the model touches**: catalog ids, nitro variants, deprecated remaps, fixed presets that pin it, and every fallback chain.
4. **Choose model and effort from the intelligence vs cost-per-task Pareto frontier**, not sticker `$/M` prices:
   - Source: [Artificial Analysis models](https://artificialanalysis.ai/models), Intelligence Index vs Cost per Intelligence Index Task. Cost per task folds in input, cache, reasoning, and answer tokens; list prices miss verbosity and thinking overhead.
   - A candidate is on the frontier if no allowed model is both smarter and cheaper per task at the chosen effort.
   - `fast`: cheapest near-frontier effort that clears the quality floor. `medium`: best $/task for typical chat. `high` / agent tool loops: deepest effort that still earns its cost. Do not burn max effort on housekeeping jobs (scanners, summarizers, TTS scripts) without a measured need.
   - Re-check when replacing a model; the frontier moves.
5. **Add tests** for effort resolution on each tier, nitro and base ids, fixed presets, omit-effort models, and emergency fallback overrides.

## xAI Chat vs Responses request shape (mandatory)

If your xAI text calls use the **xAI Python Chat SDK** (`client.chat.create` → `chat.sample()` or stream), do not mix in Responses API (`/v1/responses`) vocabulary.

| Intent | Chat SDK (`client.chat.create`) | Responses API (`/v1/responses`) |
| --- | --- | --- |
| Encrypted reasoning | `use_encrypted_content=True` | `include: ["reasoning.encrypted_content"]` |
| Tool/search outputs | Chat `IncludeOption` only (see SDK `IncludeOptionMap`) | Different include vocabulary |

1. Request encrypted traces with `use_encrypted_content=True` only. Never put `reasoning.encrypted_content` in Chat `include`; the SDK raises `ValueError: Invalid include option` before the RPC, and the call silently falls through to your fallback provider.
2. Chat `include` takes only Chat `IncludeOption` values, for example `inline_citations`, `web_search_call_output`, `x_search_call_output`, `code_execution_call_output`, `mcp_call_output`, `verbose_streaming`. Re-check `IncludeOptionMap` when upgrading `xai-sdk`.
3. Enable encrypted capture only when reasoning effort is set **and not** `"none"`.
4. `store_messages` / `previous_response_id` are valid Chat params for continuity.
5. When wiring new xAI fields, verify against live `docs.x.ai` **and** the installed SDK. Follow [xai-api-mastery](references/xai-api-mastery.md). Never pick a model from memory.

## Displayable reasoning for chat traces (mandatory)

Encrypted blocks are for continuity and audit. They are not what the user sees.

- xAI Chat SDK: `reasoning_content` on the sample or stream chunk.
- OpenRouter: `message.reasoning` and displayable `reasoning_details` (`reasoning.summary`, `reasoning.text`). Encrypted-only details fall back to flat `message.reasoning`.
- Persist those summaries on the chat row the UI reads (for example `metadata.reasoning_steps`). Keep a separate audit table for raw traces.
- A traces UI must not show only tool counts when the provider returned a summary.

## xAI RPC deadline (mandatory)

`Client(timeout=...)` / `AsyncClient(timeout=...)` is the total gRPC RPC deadline, not an idle timeout. Official generate-text examples use `timeout=3600` for reasoning models. A `DEADLINE_EXCEEDED` at a round number of seconds is that client deadline firing.

- Give each path its own deadline setting: a short one for quick interactive tool calls, a long one (up to 3600 s) for long-running agent turns. Do not copy the short value onto the long path.
- Do not "fix" a deadline by retrying the same short call.
- A browser or proxy abort on a streaming request must sit at or above the server-side deadline.

## Agent turn step logs

Diagnose an agent turn from structured events, not from a generic tool failure.

| Event | Fields |
| --- | --- |
| `chat.turn_start` | `turn_id`, owner id, bounded query |
| `chat.completion` | round, `duration_ms`, model, `finish_reason`, `response_id`, tools requested, reasoning preview |
| `chat.tool` | kind, name, ok, call_id, bounded error |
| `chat.provider_error` | round, `duration_ms`, error |
| `chat.turn_end` | ok, tool usage, error |

Filter on `event` and `turn_id`. Never log bodies or full tool payloads. A failed tool result the model sees includes the cause (`read failed: DEADLINE_EXCEEDED`), not a generic `failed.`

## Prompt caching

Provider caches reuse only an exact leading prefix, and misses are invisible unless measured. Keep system text byte-stable (no dates, ids, or live values in `role=system`), append only, and derive the cache key from the system prefix plus owner scope. Direct xAI text sends it as `x-grok-conv-id`; OpenRouter as `session_id`. Caching lives in transport, not callsites. After a prompt or routing change, measure hit rates per tier. Details: [prompt-cache-optimization](references/prompt-cache-optimization.md).

## Speech and voice rules

Product audio goes through one shared scheduler so one global budget sees every call; a process-local limiter lets each worker think it has the whole quota.

- STT, TTS, and image generation each have one client module, and all of them use the shared scheduler.
- The `speech` and `transcribe` references use the OpenAI Audio API for one-off dev tasks. Their bundled CLI scripts were not carried over; call the API directly. Never wire them into product paths.
- Do not add ad hoc local transcription (local Whisper, Vosk, ffmpeg pipelines) next to the product STT path.
- Realtime voice sessions acquire and release shared leases; reconnects and rotations refresh the same lease.
- Preserve `tool_call_id`, turn ids, user attribution, and timeout settings across voice and tool paths.

## Verification checklist

- Current callsites and tests searched.
- Official provider docs or live model metadata checked when request behavior is uncertain.
- The router owns model id resolution and provider-specific knobs.
- OpenRouter payloads include ZDR plus the denylist (and `require_parameters` when JSON); exceptions are named.
- Wire ids are `:nitro` (or `:exacto` after a nitro failure), never `:free`.
- ZDR host audit passed and recorded for any new or replaced OpenRouter model.
- Reasoning effort maps come from **that model's live `supported_efforts`**; omit-effort models skip the payload.
- xAI Chat create kwargs never contain Responses-only include strings; encrypted capture is off for `"none"` effort.
- Model and effort choice justified against cost per task, not `$/M` alone.
- Search-tool request shape is asserted in tests; structured-output paths do not suppress required search evidence.
- Fallback metadata preserves primary failure context.
- Each path's deadline is its own setting, tested.
- Agent turns log step events with `turn_id`; tool errors include the cause; bodies are not logged.
- User settings failures degrade to defaults unless authorization requires otherwise.
