from website.services.shared.llm import call_gpt

def generate_story(story_plan, cultural_profile):
    """
    Generates a children's story from a structured plan
    and explicit cultural context.
    """

    prompt = f"""
    You are a children's story writer.

    Write a complete story based STRICTLY on the following plan:

    STORY PLAN:
    {story_plan}

    CULTURAL CONTEXT:
    {cultural_profile}

    Requirements:
    - Follow the plot beats in order
    - Use culturally appropriate names, settings, and behaviors
    - Keep language suitable for the target age group
    - Do not introduce new characters or themes

    IMPORTANT:
    - The story MUST end with the exact line:

    The End.

    - Do not place any text after this line.
    """

    return call_gpt(prompt, temperature=0.7)
