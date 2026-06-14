# Prompts

Prompt templates live in `apps/api/app/ai/prompts.py`.

## System Prompt

The system prompt defines Salaar AI as a public civic guidance assistant for Pakistan. It states:

- guidance is general public guidance, not legal advice
- supported languages are English, Urdu, and Roman Urdu
- supported MVP domains are limited to the three requested domains
- official Pakistani knowledge-base context should be preferred
- the assistant must not invent phone numbers, forms, deadlines, addresses, legal sections, or procedures

## Prompt Types

- `CLASSIFICATION_PROMPT`
- `MISSING_FIELDS_PROMPT`
- `FOLLOW_UP_PROMPT`
- `REPORT_PROMPT`
- `SAFETY_PROMPT`

## Prompt Rules

- Ask missing questions one by one or in small groups.
- For workplace harassment, prioritize safety and privacy.
- Never blame the victim.
- Ask only for relevant facts.
- Always remind the user to collect a complaint number, diary number, report number, token number, receiving copy, or stamped copy where relevant.
- If no reliable official Pakistani source exists in the knowledge base, say that the information could not be verified from the current official-source knowledge base.
