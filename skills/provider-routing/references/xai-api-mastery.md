---
name: xai-api-mastery
description: Expert navigator for the official xAI Grok API documentation and Python SDK. Use when a user asks about xAI or Grok API integration, authentication, model selection, pricing, rate limits, streaming, structured outputs, tool use, files and collections, vision, image or video generation, voice, migration, SDK code generation, or troubleshooting. Always verify against live docs.x.ai pages and prefer the official `xai-sdk` for Python unless the user explicitly asks for raw HTTP, OpenAI compatibility, or another language.
---

# xAI API Mastery

Provide current, production-grade xAI API guidance from live official sources. Browse first, cite exact docs pages, and treat `docs.x.ai` plus the official `xai-org/xai-sdk-python` repository as the source of truth.

## Use This Workflow

1. Start with the official docs entry points:
   - `https://docs.x.ai/overview`
   - `https://docs.x.ai/developers/quickstart`
   - `https://docs.x.ai/developers/models`
   - `https://docs.x.ai/developers/rest-api-reference/inference`
2. Open the capability-specific page that matches the task: chat, tools, image understanding, image generation, video, voice, files, collections, batches, debugging errors, rate limits, or migration guides.
3. Search with precise terms instead of broad browsing. Good queries include `streaming`, `structured outputs`, `function calling`, `web search`, `x search`, `code execution`, `image understanding`, `voice agent`, `speech to text`, `text to speech`, `files`, `collections`, `batches`, `responses`, `grpc`, and `regional endpoints`.
4. Check freshness on every page used. Look for the page's `Last updated` date and include concrete dates whenever the question depends on current models, pricing, limits, or product availability.
5. Cross-check the official SDK repo when docs are thin or examples matter:
   - `https://github.com/xai-org/xai-sdk-python`
6. If public docs do not cover the feature, say that clearly, summarize what you checked, and point the user to xAI Console, release notes, or official xAI announcements.

## Prefer the Official SDK

- Default to Python plus `xai-sdk`.
- Start Python examples with:

```bash
pip install xai-sdk
```

- Prefer `from xai_sdk import Client, AsyncClient` and the SDK's chat helpers for Python examples.
- Do not default to raw `requests`, `httpx`, `curl`, the OpenAI compatibility layer, or third-party clients unless the user explicitly asks for low-level control, compatibility mode, or a non-Python target.
- If a docs page shows multiple integration surfaces side by side, choose the `xai-sdk` example first for Python and mention compatibility alternatives only as secondary options.
- Do not recommend a model from memory. Re-open the live models page before advising on model choice.

## Source Selection

- Use Quickstart for installation, API keys, and first-request patterns.
- Use Models and Pricing for model choice, context windows, aliases, rate limits, pricing, and migration-sensitive guidance.
- Use the capability page for feature behavior and request shape.
- Use the REST API reference for exact field names, endpoint behavior, and compatibility notes.
- Use the official SDK repository for idiomatic Python examples, releases, and example code when the docs are too abstract.

## Answering Rules

- Link to every source page you used.
- Separate confirmed facts from inference.
- Keep code snippets small, runnable, and production-friendly.
- Prefer environment-variable authentication with `XAI_API_KEY`; never hardcode secrets.
- Call out REST-versus-SDK or REST-versus-gRPC differences when they affect the answer.
- Ignore compatibility examples unless the user asked for them.
- If docs disagree or one page is newer, say so and prefer the newer page.

## Useful Notes

- The older path `https://docs.x.ai/developers/api-reference` currently redirects to the canonical inference reference at `https://docs.x.ai/developers/rest-api-reference/inference`; cite the canonical URL.
- The docs site and model lineup change frequently. Re-check live pages instead of relying on this skill for model names, prices, or limits.

## Reasoning traces (Chat SDK vs Responses)

If your text Grok calls use the Chat SDK (`client.chat.create`), do not use `/v1/responses` vocabulary.

- High model: `grok-4.7`. Keep `reasoning_effort="high"` (API default).
- Displayable summary: stream or sample `reasoning_content` (Grok 4.7 summarized reasoning). That is what chat Traces must persist and show.
- Encrypted continuity: Chat SDK `use_encrypted_content=True`. Never put `reasoning.encrypted_content` in Chat `include` (Responses-only; SDK raises `ValueError: Invalid include option`).
- Effort: `reasoning_effort` on Chat create (`low` / `medium` / `high` / `xhigh` on grok-4.7). Default is `high`. Cannot disable on grok-4.7/4.6/4.5. `"xhigh"` is grok-4.6 and later.
- Docs: https://docs.x.ai/developers/model-capabilities/text/reasoning and https://docs.x.ai/developers/grok-4-7 (Last checked 2026-09-21). Re-open those pages before changing request shape.

## Client timeout is a gRPC deadline

`xai_sdk.Client(timeout=...)` and `AsyncClient(timeout=...)` bound the whole RPC, not idle time. Official generate-text examples use `timeout=3600` for reasoning models (Last checked 2026-09-20). Re-open https://docs.x.ai/docs/guides/chat before changing that number.

`DEADLINE_EXCEEDED` at ~120s means the client deadline, not xAI dropping an idle stream. Do not retry the same short deadline as the fix. Raise the deadline for long tool loops. OpenAI-compat JS examples use `timeout: 360000` (ms, 6 minutes). With the Python gRPC SDK, copy the 3600s Python example, not the JS millisecond value.

Keep separate deadline settings per path (a short one for quick tool calls, a long one for long agent turns). Do not merge them. See `/provider-routing`.

## Diagnose agent turns

Log one structured event per step. Use `event`, `turn_id`, `tool`, `error`, `reasoning`, `finish_reason`, `response_id` as fields.

- `chat.completion`: round, duration, model, tools requested, reasoning preview
- `chat.tool`: name, ok, bounded error. The tool result the model gets must carry that same cause.
- `chat.provider_error`: the RPC or exception text

Do not log source bodies or full arguments. Filter logs on `turn_id`. Persist displayable `reasoning_content` on the chat row as well. Logs are for live diagnosis; the traces view is for the user.
