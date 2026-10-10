# Agent and LLM threats

Maps OWASP Top 10 for LLM Applications 2025 (https://genai.owasp.org/llm-top-10/) and OWASP Top 10 for Agentic Applications 2026 (ASI01 to ASI10, https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) onto the usual surfaces of an app that runs agents. Each row ends in a check you can run or read.

Core rule: text an agent reads is data. Content from an uploaded document, a web page, a chat or bot message, a webhook body, third-party API text, or another tool's output never authorizes a payment, an order, a key, a file write, or a message.

## Surfaces to list first

- **Agent tools**: where tools are defined and which have side effects (writes, sends, payments, code execution).
- **Context sources**: uploaded files, fetched pages, emails, chat messages, search results the agent reads.
- **Agents**: each agent, its tool set, and the channels it listens on (web chat, bots, scheduled automations).
- **Sandboxes**: where agent-written code runs, its egress policy, and which credentials it holds.
- **Programmatic access**: MCP servers, CLIs, API keys, and their scopes.

## LLM Top 10 2025

| Id | Risk | Typical surface | Check |
|----|------|------------------|-------|
| LLM01 | Prompt injection (direct and indirect) | Documents, web fetch results, bot messages, webhooks, tool output feeding an agent with side-effecting tools | Trace every path from untrusted text to a side-effecting tool. The side effect needs a user approval or a server-side policy the model cannot argue past. Plant an instruction in a fixture source and assert no tool call follows. |
| LLM02 | Sensitive information disclosure | Account and personal data in prompts; provider logs | Route every call through one router with a zero-retention provider policy. No secrets or keys in prompts or tool results. Logs carry ids, not bodies. |
| LLM03 | Supply chain | Models, provider routes, vendored skills and plugins | No free or unpinned model routes. Scan any new skill or plugin for scripts, network calls, and injection phrases before merge. See `supply-chain.md`. |
| LLM04 | Data and model poisoning | Agent memory, shared docs that agents read | Memory writes record provenance. A source the user did not author cannot write durable memory that later selects tools. |
| LLM05 | Improper output handling | Model markdown in web and mobile UIs and bots; model-built CLI args, SQL, paths | Render through a sanitizer; no `dangerouslySetInnerHTML` of raw model text. No shell strings from model output; argv lists only. Path tools resolve inside granted roots. |
| LLM06 | Excessive agency | Payment or order tools, send tools, file writes, code execution | Least privilege per agent. Proposals, not submissions. Allowlist commands. Irreversible money movement unreachable from every key and tool. Write a deny test per rule. |
| LLM07 | System prompt leakage | Agent templates | Prompts hold no secrets, so leakage is harmless. Security never depends on the model keeping the prompt hidden. |
| LLM08 | Vector and embedding weaknesses | Memory, document search | Retrieval filters by user and workspace before ranking. Cross-user retrieval is a finding. |
| LLM09 | Misinformation | Numeric answers, recommendations | Numbers come from tool results with source and freshness, not model recall. Stale data is labeled. |
| LLM10 | Unbounded consumption | Agent loops, public entry points | A fixed per-call hang timeout, per-user cost ceilings, and rate limits on bot and MCP entry points. |

## Agentic Top 10 2026 (the risks LLM Top 10 underweights)

| Risk | Typical surface | Check |
|------|------------------|-------|
| Agent goal hijack | Documents or web pages steering a scheduled automation | Automations run with the same approval gates as chat turns. No gate is skipped because a run is scheduled. |
| Tool misuse | File, send, and payment tools | Tool args validated server-side, not by the tool description. Destructive tools declare it. |
| Identity and privilege abuse | User API keys, short-lived sandbox keys | Sandbox keys are short-lived, scoped to one workspace, and rejected on money and admin routes. Test a sandbox key against those routes and another workspace. |
| Agentic supply chain | MCP servers, plugins, skills | Pin versions; review new tools' descriptions for injection text. |
| Unexpected code execution | Code sandboxes, local exec tools | Code runs only in the sandbox. Sandbox egress is limited; the sandbox holds no user key or third-party credential. A local dev sandbox provider is not reachable in production. |
| Memory and context poisoning | See LLM04 | Same check. |
| Insecure inter-agent communication | Agents sharing documents or channels | One agent's output is untrusted input to another. A low-privilege agent cannot reach a high-privilege agent's tools through it. |
| Cascading failures | Schedulers, heartbeat automations | A failed tool result cannot be read as success; errors reach the log with a run id. |
| Human-agent trust exploitation | Approval cards, previews, bot approvals | The approval surface shows the server's canonical action, not model prose. Bot webhooks check their secret header with a constant-time compare. |
| Rogue agents | Autonomy settings, kill switch | Autonomy defaults off; the kill switch fails safe; both enforced server-side on every action. |

## Review steps for an agent diff

1. List new or changed tools and their side effects.
2. For each, name the untrusted inputs that can reach its arguments.
3. Find the server-side gate. If the only gate is the prompt, it is a finding.
4. Confirm a deny test exists, or write one.
