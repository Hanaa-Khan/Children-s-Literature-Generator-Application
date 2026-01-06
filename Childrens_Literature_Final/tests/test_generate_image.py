# test_generate_image.py
from website.services.shared.llm import generate_image

# Example prompt
prompt = """
CHILDREN'S BOOK ILLUSTRATION - SINGLE CHARACTER

Character: Maya, 8-year-old child, consistent appearance
Appearance: Medium warm skin, dark brown hair in ponytail, brown eyes
Clothing: Blue t-shirt, red sneakers
Scene: Maya is walking down a Tokyo street holding a red balloon. Only one character, single moment in time, background shows buildings and cherry blossoms.
Style: Soft watercolor children's book illustration, bright colors
"""
prompt2 = """
CHILDREN'S BOOK ILLUSTRATION - SINGLE CHARACTER

Character: Maya, 8-year-old child, consistent appearance
Appearance: Medium warm skin, dark brown hair in ponytail, brown eyes
Clothing: Blue t-shirt, red sneakers
Scene: Maya is walking down a Tokyo street and she leys go of a red balloon. Only one character, single moment in time, background shows buildings and cherry blossoms.
Style: Soft watercolor children's book illustration, bright colors
"""

prompt3 = """
CHILDREN'S BOOK ILLUSTRATION - SINGLE CHARACTER

Character: Maya, 8-year-old child, consistent appearance
Appearance: Medium warm skin, dark brown hair in ponytail, brown eyes
Clothing: Blue t-shirt, red sneakers
Scene: Maya is walking down a Tokyo street and her red balloon is floating away. Only one character, single moment in time, background shows buildings and cherry blossoms.
Style: Soft watercolor children's book illustration, bright colors
"""

# Generate image
try:
    img_url = generate_image(prompt)
    print("Generated image URL:", img_url)
    img_url = generate_image(prompt2)
    print("Generated image URL:", img_url)
    img_url = generate_image(prompt3)
    print("Generated image URL:", img_url)
except Exception as e:
    print("Error generating image:", e)
