from website.services.shared.llm import generate_image, call_gpt

def summarize_scene(scene_text: str, max_words: int = 15) -> str:
    """
    Summarize a scene into ONE atomic sentence: single action, single pose.
    """
    prompt = f"""
Summarize the following story scene into ONE concise sentence (max {max_words} words),
focusing ONLY on the main character's single action in a single pose.
Output must describe ONE action, NO multiple actions or poses.

Scene:
{scene_text}

Output:
"""
    try:
        summary = call_gpt(prompt, temperature=0.3).strip()
        return f"Single pose, performing only this action: {summary}"
    except Exception as e:
        print(f"⚠️ Error summarizing scene: {e}")
        return f"Single pose, performing only this action: {scene_text}"


def generate_images(
    story_plan,
    character_name,
    age_range,
    character_type,
    character_profile,
    cultural_profile
):
    """
    Generate 3 clean images for a story:
    - Single pose, single action
    - Correct species, age, and ethnicity/fur
    - Story-appropriate background only
    """
    print(f"🎨 Generating images for {character_name}...")

    visual = character_profile["visual_identity"]
    character_desc = (
        f"{character_name}, a {age_range}-year-old {character_type}, "
        f"{visual['skin_tone']} skin/fur, {visual.get('hair_description','n/a')} in {visual.get('hairstyle','n/a')}, "
        f"{visual.get('eye_description','friendly eyes')} eyes, wearing {visual['clothing_description']}."
    )

    plot_beats = story_plan.get("plot_beats", ["Beginning", "Middle", "End"])
    scene_types = ["Beginning", "Middle", "End"]

    images = []

    for i, scene in enumerate(plot_beats[:3]):
        single_action = summarize_scene(scene)
        location = cultural_profile.get("story_context", {}).get(
            "location", "a simple, child-friendly background"
        )

        prompt = f"""
CHILDREN'S BOOK ILLUSTRATION

IMPORTANT RULES:
- EXACTLY ONE character in the image
- SINGLE POSE: do not show front + back, no multiple angles
- SINGLE ACTION: character performs only the described action
- Character fully integrated with the background
- DO NOT include any clones, reflections, extra characters, or random objects
- NO color palettes or irrelevant items unless story-specific

CHARACTER DESCRIPTION:
{character_desc}

SCENE ({scene_types[i]}):
{single_action}. Background: {location}

CAMERA AND POSE:
- Medium shot, centered, facing direction appropriate for action
- Do not rotate or show multiple angles

STYLE:
{character_profile.get('art_style', "Soft watercolor children's book illustration")},
child-friendly, clear focus on character, natural integration with background.
"""

        try:
            img_url = generate_image(prompt)
            images.append(img_url or "/static/fallback_image.png")
            print(f"  ✓ {scene_types[i]} generated: single pose, background only")
        except Exception as e:
            print(f"  ✗ Error generating {scene_types[i]}: {e}")
            images.append("/static/fallback_image.png")

    print(f"✨ Images generated: {len(images)}")
    return images
