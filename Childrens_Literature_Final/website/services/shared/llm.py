import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(prompt, model="gpt-4.1", max_tokens=500, temperature=0.7):
    """
    Generic GPT text call
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    return response.choices[0].message.content

def generate_image(prompt, size="1024x1024"):
    """
    Generate an image using DALL·E 3
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size
    )

    return response.data[0].url
