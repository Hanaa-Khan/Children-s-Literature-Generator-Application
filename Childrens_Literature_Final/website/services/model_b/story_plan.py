from website.services.shared.llm import call_gpt
import json


def generate_story_plan(user_input, cultural_profile):
    """
    Generate a 3-part children's story plan with STRICT trait and cultural consistency.
    This function does not overwrite user inputs.
    """

    character_name = user_input.get("character_name", "Child")
    age_range = user_input.get("age_range", "7-9")
    character_type = user_input.get("character_type", "human")
    location = user_input.get("location", "a familiar place")
    theme = user_input.get("theme", "adventure")

    traits = user_input.get("traits", [])
    if isinstance(traits, str):
        traits = [t.strip() for t in traits.split(",") if t.strip()]
    if not traits:
        traits = ["curious", "kind"]

    traits_text = ", ".join(traits)

    cultural_context = {
        "cultural_analysis": cultural_profile.get("cultural_analysis", {}),
        "principles": cultural_profile.get("principles", {}),
        "region": cultural_profile.get("user_context", {}).get("region", ""),
    }

    prompt = f"""
You are creating a story PLAN (not the full story) for a children's book.

CHARACTER PROFILE (DO NOT CHANGE):
- Name: {character_name}
- Age range: {age_range}
- Type: {character_type}
- Personality traits: {traits_text}

STORY CONTEXT (DO NOT CHANGE):
- Location: {location}
- Theme: {theme}

CULTURAL GUIDANCE:
{json.dumps(cultural_context, indent=2)}

IMPORTANT CONSTRAINTS:
- Do NOT change the character name, age, traits, or cultural context
- Do NOT introduce new personality traits
- Every plot beat MUST clearly reflect at least one of the listed traits
- Keep language appropriate for ages {age_range}
- Keep the tone positive and culturally respectful

TASK:
Create a simple 3-part story plan:
1. Beginning: Introduce the character and setting
2. Middle: A challenge or adventure that tests the character's traits
3. End: A positive resolution using the character's traits

Return VALID JSON ONLY in this exact format:
{{
  "title": "Short child-friendly title",
  "plot_beats": [
    "Beginning beat (mentions at least one trait)",
    "Middle beat (mentions at least one trait)",
    "End beat (mentions at least one trait)"
  ],
  "moral": "Simple lesson connected to the traits"
}}
"""

    try:
        response = call_gpt(prompt, temperature=0.4)
        plan = json.loads(response)

        if "plot_beats" not in plan or len(plan["plot_beats"]) != 3:
            raise ValueError("Invalid plot beats")

        return plan

    except Exception:

        return {
            "title": f"{character_name}'s {theme.capitalize()} Adventure",
            "plot_beats": [
                f"Beginning: {character_name} shows their {traits_text} nature in {location}.",
                f"Middle: A challenge helps {character_name} use their {traits_text} traits.",
                f"End: {character_name} succeeds by being {traits_text}."
            ],
            "moral": f"Being {traits_text} helps us overcome challenges."
        }
