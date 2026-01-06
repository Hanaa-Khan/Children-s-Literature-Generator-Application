import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_images_a(plot_beats):
    """
    Generate 3 images for Model A, one for each story section.
    plot_beats: list of strings (beginning, middle, end)
    Returns list of 3 image URLs
    """
    if not isinstance(plot_beats, list) or len(plot_beats) == 0:
        plot_beats = ["An illustration for a children's story"] * 3

    urls = []
    for beat in plot_beats[:3]:
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"Illustration for a children's story: {beat}",
                size="1024x1024"
            )
            urls.append(response.data[0].url)
        except Exception as e:
            print("Image generation failed for beat:", beat, e)
            urls.append("/static/fallback_image.png")  

    while len(urls) < 3:
        urls.append("/static/fallback_image.png")

    return urls

