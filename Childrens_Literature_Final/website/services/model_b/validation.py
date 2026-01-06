from website.services.shared.llm import call_gpt


def validate_story(story_text, cultural_profile):
    prompt = f"""
You are a quality reviewer for a children's story system.

Your task:
- ONLY make changes if there is a clear issue with:
  - cultural sensitivity
  - age appropriateness
- DO NOT remove or flatten:
  - personality traits
  - cultural details
  - character identity
- DO NOT rewrite the story structure unless required.
- Preserve the original voice and events.

CULTURAL + TRAIT CONTEXT (DO NOT CHANGE):
{cultural_profile}

STORY:
{story_text}

Return ONLY the final corrected story text.
Do not include headings, explanations, or commentary.
"""

    reviewed_story = call_gpt(prompt, temperature=0.1)
    return clean_story(reviewed_story)

def clean_story(text):
    unwanted_headers = [
        "**Review for Cultural Sensitivity and Age Appropriateness**",
        "**Cultural Sensitivity:**",
        "**Age Appropriateness:**",
        "**Suggestions and Edits:**"
    ]
    for header in unwanted_headers:
        text = text.replace(header, "")
    return text.strip()

