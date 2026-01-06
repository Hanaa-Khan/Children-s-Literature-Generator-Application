from website.services.model_a.text_generation import generate_story_a
from website.services.model_a.image_generation import generate_images_a

def split_into_three_beats(story_text: str):
    lines = [l for l in story_text.splitlines() if l.strip()]
    if len(lines) < 3:
        return [story_text, story_text, story_text]
    third = len(lines) // 3
    return [
        " ".join(lines[:third]),
        " ".join(lines[third: 2*third]),
        " ".join(lines[2*third:])
    ]

def run_model_a(user_input: dict, user_metadata: dict = None, cluster_context: dict = None) -> dict:
    prompt_text = user_input.get("prompt_text", "")
    if not prompt_text:
        raise ValueError("Prompt text missing")

    story_text = generate_story_a(prompt_text)
    plot_beats = split_into_three_beats(story_text)
    images = generate_images_a(plot_beats)
    if not images or len(images) < 3:
        images = ["/static/fallback_image.png"] * 3

    return {
        "story_text": story_text,
        "images": images[:3],
        "character_profile": {},
        "cultural_profile": {}
    }
