HUMANIZE_RULES = """
Write like a real person typing this themselves, not marketing copy or an AI assistant.
- No buzzwords: "game-changer", "unlock", "leverage", "seamless", "passionate about",
  "in today's fast-paced world", "dive into", "cutting-edge", "in conclusion".
- At most ONE emoji, only if it truly fits. Zero is usually better.
- One exclamation point max, only if earned.
- Vary sentence length on purpose — mix short and long.
- Be concrete ("cut load time from 4s to 900ms") instead of vague ("significantly improved").
- Contractions are fine (I'm, don't, it's).
"""

def build_variation_instruction(n: int) -> str:
    return (
        f"Generate {n} genuinely different versions (different angle/structure, not just "
        f"reworded synonyms). Separate each with a line: ---VERSION {{i}}---  "
        f"(replace {{i}} with the version number, 1 through {n})."
    )

README_TEMPLATE = """You are writing a GitHub profile/project README.
Context: {context}
{humanize_rules}
- Short intro about who they are / what they build
- What they're currently working on
- Tech stack, written naturally
- A project worth highlighting and why it mattered
- How to reach them, if relevant
Output clean Markdown, no surrounding code block.
{variation_instruction}
"""

LINKEDIN_POST_TEMPLATE = """You are writing a LinkedIn post.
Context: {context}
{humanize_rules}
- Open with a real hook, not "Excited to announce..."
- Short paragraphs, 1-3 sentences, line breaks (mobile-readable)
- End with something that invites a genuine response
- Roughly 80-180 words unless context calls for more
{variation_instruction}
"""

LINKEDIN_ABOUT_TEMPLATE = """You are writing a LinkedIn "About" section.
Context: {context}
{humanize_rules}
- First person, conversational
- Open with what they care about/do, not their job title
- Concrete specifics over adjectives
- End with what they're open to, if relevant
- Roughly 100-220 words
{variation_instruction}
"""

LINKEDIN_HEADLINE_TEMPLATE = """You are writing LinkedIn headlines (~220 characters).
Context: {context}
{humanize_rules}
- Not just "Job Title at Company"
- Say what they actually do, understandable in 2 seconds
- Vary structure across the 5 versions
- Under 220 characters each
- After the 5 headlines, add "Why headlines work" — 3-4 plain-language sentences of advice
{variation_instruction}
"""

CUSTOM_TEMPLATE = """You are writing: {content_type}
Context: {context}
{humanize_rules}
Match the natural conventions and length of this content type.
{variation_instruction}
"""

ROUTER_SYSTEM_PROMPT = """Classify this request into exactly one label, output only the label:
readme | linkedin_post | linkedin_about | linkedin_headline | custom

Request: {request}
"""
