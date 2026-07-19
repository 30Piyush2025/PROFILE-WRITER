# Profile Writer

An AI agent that writes GitHub READMEs, LinkedIn posts, LinkedIn About sections, and
LinkedIn headlines — built to sound like a person wrote them, not a language model.
Every request returns 5 genuinely different options so you pick the one that fits,
instead of getting stuck with whatever the model felt like generating first.

## Why this exists

Most AI-generated LinkedIn content reads the same way: "Excited to announce," three
buzzwords in a row, an emoji stacked on every line, and a closing line that could've
been copy-pasted from a thousand other posts. This project sets out to fix that by
baking a strict humanization rulebook into every prompt — no filler phrases, at most
one emoji, no exclamation-point stacking, and a deliberate push toward specific,
concrete details over vague self-praise.

## How it works

The agent is built with **LangGraph**, not a single flat prompt-and-response chain.
A router node reads the request and decides which content type it's dealing with;
that decision routes execution to a dedicated generator node, and each generator
node calls the LLM once, asking for 5 distinct variations in a single response.

```
        ┌─────────┐
input ─▶│ router  │
        └────┬────┘
             │
   ┌─────────┼──────────┬──────────────┬────────────┐
   ▼         ▼           ▼              ▼            ▼
readme  linkedin_post  linkedin_about  headline    custom
   │         │           │              │            │
   └─────────┴───────────┴──────────────┴────────────┘
                          ▼
                       output (5 options)
```

If you already know what you want (README, post, About, headline), you pick it
directly from a menu and skip the router entirely. If you type a free-text request
instead — "write me a Twitter bio" or "draft a cover letter opener" — the router
classifies it and sends it down a generic `custom` path, so the agent isn't locked
to just four content types.

The LLM backend is **Groq**, running Llama 3.3 70B, chosen for speed and a generous
free tier. Swapping to a different provider (OpenAI, Gemini, a local model) only
requires changing the one function that constructs the LLM client — nothing else in
the graph needs to know or care which provider is behind it.

## What makes the output sound less like AI

Every generator shares one rulebook before it writes anything:

- No stock buzzwords — "game-changer," "unlock," "leverage," "seamless," "passionate
  about," "in today's fast-paced world," and similar phrases are explicitly banned
  in the prompt.
- At most one emoji, and only if it earns its place. Zero is treated as the default.
- One exclamation point max per piece of content.
- Sentence length is deliberately varied — short, punchy lines mixed with longer
  ones, instead of the flat, uniform rhythm that gives AI writing away.
- Concrete specifics are pushed over vague self-description: "cut load time from 4s
  to 900ms" instead of "significantly improved performance."
- Contractions are encouraged, because real people use them.

This rulebook is applied identically across README generation, LinkedIn posts, About
sections, and headlines, so the tone stays consistent no matter what you're asking
the agent to write.

## Content types supported

| Type | What it produces |
|---|---|
| GitHub README | Profile or project README with intro, current work, stack, and highlights |
| LinkedIn post | A short, mobile-readable post with a real hook and a closing that invites a reply |
| LinkedIn About | First-person summary that leads with what you do, not your job title |
| LinkedIn headline | Five headline options plus a short explanation of what makes a headline work |
| Anything else | Routed through a free-text classifier into a generic generator — Twitter bios, elevator pitches, cover letter openers, and similar formats |

## Running it

The project runs cleanly as a Python script or inside Google Colab.

```bash
pip install langgraph langchain-groq langchain-core
```

Set your Groq API key (get one at console.groq.com/keys):

```bash
export GROQ_API_KEY=your_key_here
```

Then run the agent, pick a content type from the menu, paste in context about
yourself or your project, and review the 5 generated options.

## Project structure

- `state.py` — shared state definition passed between graph nodes
- `prompts.py` — the humanization rulebook and per-content-type templates
- `graph.py` — LangGraph node definitions, routing logic, and the Groq LLM call
- `main.py` — interactive CLI that drives the whole thing

## Extending it

Adding a new content type as its own menu item takes three small additions: a
template in `prompts.py`, a generator function and node in `graph.py`, and a menu
entry in `main.py`. Anything not explicitly added still works through the `custom`
path — the router will classify it and hand it off automatically.

## Notes

This was built as a learning project around LangGraph's node/routing model and
prompt-level control over tone. It's not meant to replace writing in your own voice
— it's meant to give you a fast first draft with the buzzword and emoji noise
already stripped out, so editing takes less effort than starting from a blank page.
