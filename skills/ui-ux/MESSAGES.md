# Messages to the person

Rules for any text the app sends a person on its own: push or bot alerts, question cards, digests, automation results, and the chips that point at them. The person reads these on a phone between other things. They did not ask for this message, so it has to earn the interruption.

## What goes wrong

A typical first version of a price-move alert:

```
What. BLND dropped sharply.

Evidence. BLND -2.7% today at 1.08. prior close 1.11. Blend Labs, Inc. Prior card for this point at 2026-09-28T13:46:09.598741+00:00.
No earlier print is in the scan ring.

Why. You were notified because BLND moved -2.7%.

So what. Deep dive writes the brief. Mute hides this name for 24 hours.
[Deep dive] [Mute 24h]
This question has no skip option.
```

Users push back on exactly these things: odd formatting, internal words, a full stop after every fragment, raw timestamps, no way to skip, and too many messages. A rewrite that ends "Want me to dig in?" also fails: if the app already has the data, it should say why. Better:

```
Coherent (COHR) dropped 4.5% today to $282.45. Volume is 2.3x normal.

Morgan Stanley downgraded it to Equal-Weight from Overweight and Citi set a $260 target. Its score in your ranking fell to 41/70 from 48/70.

In the news today:
• Coherent prices $1B convertible notes offering (Reuters)

You're seeing this because you hold it and it moved more than 2.5%. You also hold LITE, which trades alongside it.
[Deep dive] [Mute 24h]                        Skip
```

And when nothing specific happened:

```
Blend Labs (BLND) is off 2.7% today, at $1.08.

Nothing new on the company today. It is moving with the market.

Flagged because you hold it and it moved more than 2.5%.
```

## Rules

1. **What, why, and why you got it, as sentences.** The first sentence says what happened, with the name and the number. The next paragraph says why. The last line says why this message reached the person. Never ask whether to find out why: say why. Never write "What", "Why", "Evidence", or "So what" as headings.
2. **Build the text from structured fields, not from logs.** Keep the values (name, number, headlines, filings, holdings) as fields on the row and write the sentences from those. Prose fact lists are for models. They never reach the person verbatim.
3. **No internal vocabulary.** Banned in user text: internal queue or scan names, cooldowns, signal enum values, node, packet, tier, bucket names, legal boilerplate, and any raw enum. Translate each one into plain words.
4. **No machine formatting.** No ISO timestamps; use a local clock (`16:00`) or a relative time, and only when it matters. No raw floats. Use a currency sign where it is known and drop corporate suffixes. A list is `•` bullets with no trailing periods. A link sits on its own line.
5. **Check everything, say only what happened.** Run every check (news, rating changes, your own scores), mention only what happened, and never list what did not. When every check ran and nothing happened, say so in one line. If a check failed, never claim nothing happened.
6. **Answer the next question.** Connect it to what the person owns or decided ("It cuts against your thesis", "You also hold LITE, which trades alongside it"). Infer what they would ask next and put the answer in the message.
7. **Always skippable, in one tap.** Every question has a Skip. The first real choice is the filled button, the others are outlined, and Skip is a quiet text button. Each waiting chip has its own skip, and a strip of chips offers Skip all.
8. **Short title for chips.** A queue chip shows a title the producer set (`BLND −2.7%`, `NVDA news`), never a truncated first sentence.
9. **Send less, in code.** Never make the person tune settings to stop spam. Dedupe on the person, the event, and the day, not on the job that produced the message; many schedules can scan the same data. Cap the day's total. A quiet run sends nothing.
10. **Vary the wording.** Pick verbs by size (slipped, fell, plunged; edged up, rose, surged) and rotate phrasings deterministically, so a day of messages does not read like one template.
11. **Deterministic, then tested.** Same row, same text. A golden test locks the full text of one real example, and a sweep test asserts that no internal word, heading, or ISO date appears for any signal.

## Checklist before shipping a message producer

- [ ] Pull 20 real sent messages from your notification log, read them the way the person would, and count how many arrived per day.
- [ ] Would a friend who knows the domain text it this way? If not, rewrite it.
- [ ] The first line stands alone as a phone notification preview.
- [ ] No heading words, no ISO times, no internal words, no dump of prose facts.
- [ ] Every message says why it happened and why the person got it.
- [ ] Skip is present on the card and the chip, and the chip title is short.
- [ ] Dedupe and cap are per person, per event, per day, and a test runs two producers for the same person.
