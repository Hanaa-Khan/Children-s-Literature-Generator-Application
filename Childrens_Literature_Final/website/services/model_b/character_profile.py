from website.services.shared.llm import call_gpt
import json

def get_midpoint_age(age_range: str) -> int:
    """Return midpoint age for age range."""
    return {
        "0-3": 2,
        "4-6": 5,
        "7-9": 8,
        "10-12": 11
    }.get(age_range, 5)


def generate_character_profile(
    character_name,
    age_range,
    character_type,
    character_gender,
    traits,
    cultural_profile
):
    """
    Create a character profile with SPECIFIC, LOCKED visual details.
    The LLM decides everything and we save it for consistency.
    """
    fixed_age = get_midpoint_age(age_range)
    cultural_context = cultural_profile.get("story_context", {})
    location = cultural_context.get("location", "varied")
    theme = cultural_context.get("theme", "adventure")
    cultural_background = cultural_profile.get("cultural_background", "diverse")
    
    prompt = f"""
Create a COMPLETE character design for a children's book that will be IDENTICAL in all images.

CHARACTER:
- Name: {character_name}
- Age: {age_range} years old (specifically {fixed_age} years)
- Type: {character_type}
- Gender: {character_gender}
- Personality: {', '.join(traits) if traits else 'friendly, curious'}
- Cultural Context: {cultural_background}
- Story Location: {location}
- Story Theme: {theme}

REQUIREMENTS:
1. Create EXACT visual details that WON'T CHANGE between images
2. Be VERY SPECIFIC about every feature
3. The character must look the SAME in every picture
4. Include culturally appropriate elements naturally

CREATE THESE EXACT DETAILS:

SKIN: Exact skin tone description (e.g., "light olive skin with warm undertones")
HAIR: Exact hair color and texture (e.g., "dark brown wavy hair")
HAIRSTYLE: Exact hairstyle that stays the same (e.g., "shoulder-length hair in a ponytail")
EYES: Exact eye color and shape (e.g., "large hazel eyes with thick lashes")
FACE: Exact facial features (e.g., "round face with a small nose and dimples")
BODY: Exact body proportions (e.g., "child proportions, 4 feet tall, slim build")
CLOTHING: Exact outfit description (e.g., "blue striped t-shirt, denim overalls, red sneakers")
COLORS: Exact color names for clothing (e.g., "blue shirt, denim overalls, red shoes")

Respond with this EXACT JSON format:
{{
    "name": "{character_name}",
    "age_description": "a {age_range} year old child",
    "visual_identity": {{
        "skin_tone": "exact skin description",
        "hair_description": "exact hair color and texture",
        "hairstyle": "exact hairstyle that won't change",
        "eye_description": "exact eye description",
        "facial_features": "exact facial features",
        "body_proportions": "exact body description",
        "clothing_description": "exact clothing that won't change",
        "clothing_colors": "exact color names"
    }},
    "personality_traits": ["list", "of", "traits"],
    "art_style": "soft watercolor children's book illustration"
}}
"""
    
    try:
        response = call_gpt(prompt, temperature=0.3) 
        profile = json.loads(response)
        visual = profile["visual_identity"]
        profile["locked_canonical_description"] = (
            f"{character_name}, a {age_range} year old {character_type}. "
            f"SKIN: {visual['skin_tone']}. "
            f"HAIR: {visual['hair_description']} in {visual['hairstyle']}. "
            f"EYES: {visual['eye_description']}. "
            f"FACE: {visual['facial_features']}. "
            f"BODY: {visual['body_proportions']}. "
            f"CLOTHING: {visual['clothing_description']} in {visual['clothing_colors']}. "
            f"This exact appearance must be identical in every image."
        )
        
        print(f"✅ Character locked: {visual['hairstyle']}, wearing {visual['clothing_description']}")
        return profile
        
    except Exception as e:
        print(f"Error creating character profile: {e}")
        return create_fallback_profile(character_name, age_range, character_type, character_gender, traits)


def create_fallback_profile(name, age_range, char_type, gender, traits):
    """Simple fallback with locked details."""
    return {
        "name": name,
        "age_description": f"a {age_range} year old child",
        "visual_identity": {
            "skin_tone": "medium warm skin",
            "hair_description": "dark brown hair",
            "hairstyle": "neat hairstyle",
            "eye_description": "brown eyes",
            "facial_features": f"friendly {age_range} year old face",
            "body_proportions": f"{age_range} year old child proportions",
            "clothing_description": "colorful comfortable clothes",
            "clothing_colors": "blue and white"
        },
        "locked_canonical_description": f"{name}, a {age_range} year old with consistent appearance.",
        "personality_traits": traits or ["friendly", "curious"],
        "art_style": "soft watercolor children's book illustration"
    }