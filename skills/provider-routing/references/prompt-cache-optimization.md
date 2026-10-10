---
name: prompt-cache-optimization
description: >
  Build and change prompts so LLM prefill/prompt caches hit. Use when writing or
  editing system prompts, message ordering, conversation/session-id derivation, or
  provider routing that affects xAI / OpenRouter prompt caching, or when a tier
  shows a near-zero cache hit rate.
---

# Prompt cache

Provider caches reuse the exact leading prefix. Misses are invisible unless measured.

## Rules

1. Keep a byte-stable leading prefix.
   - System/developer text and static few-shots must be identical across calls that share a cache.
   - Do not put dates, tickers, live quotes, or other per-run values in the system prompt. Put them in the user message.
   - Example: a daily job keeps the run date in a user-message `DATE:` line only.
2. Derive the conversation/session key from the system prefix + owner scope only.
   - Hash provider + model + the leading system/developer messages + owner scope (application, caller, user id, workspace id, subject).
   - Do not hash the first user message. With no system/developer message, fall back to the first message.
   - Keep owner scope in the key. Different owners must never share a provider id.
   - Send the same key to xAI as `conversation_id` (`x-grok-conv-id`) and to OpenRouter as `session_id` (max 256 chars).  Send it on every path, including agentic tool loops.
3. Append only. Do not edit, drop, or reorder earlier messages. Compact old turns into the system block; do not slide the window.
4. Order: instructions, few-shots, reference docs, then volatile input.
5. After a prompt or routing change, measure hit rate per tier from logged `cached_tokens`, `cache_write_tokens`, input/output tokens, and `cost` on each provider call (a small script over your logs or usage table). A tier near 0% is a bug unless the system prompt is tiny and the user message always changes.

## Check

- Same system + two user messages → same key. Two owners → different keys. Changed system → different key.
- OpenRouter request body carries `session_id`.
