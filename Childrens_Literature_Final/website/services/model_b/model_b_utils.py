"""
Utility functions for Model B to handle nullable database fields
"""

def get_cultural_context_from_prompt(prompt):
    """
    Extract cultural context from a Prompt object, handling nullable fields.
    """
    if not prompt:
        return {}
    
    context = {
        "age_range": prompt.age_range or "5-8",
        "character_name": prompt.character_name or "Child",
        "character_type": prompt.character_type or "human child",
        "location": prompt.location or "",
        "theme": prompt.theme or "adventure",
        "character_traits": prompt.character_traits or ""
    }
    
    if hasattr(prompt, 'cultural_preference'):
        context["cultural_preference"] = prompt.cultural_preference or ""
    
    if hasattr(prompt, 'include_multicultural'):
        context["include_multicultural"] = prompt.include_multicultural or False
    
    if hasattr(prompt, 'specific_traditions'):
        context["specific_traditions"] = prompt.specific_traditions or ""
    
    if hasattr(prompt, 'story_cultural_background'):
        context["story_cultural_background"] = prompt.story_cultural_background or ""
    
    if hasattr(prompt, 'story_region'):
        context["story_region"] = prompt.story_region or ""
    
    return context


def should_use_model_b(prompt):
    """
    Determine if Model B should be used based on prompt data.
    """
    if not prompt:
        return False
    
    model_b_fields = [
        'cultural_preference',
        'include_multicultural',
        'specific_traditions',
        'story_cultural_background',
        'story_region'
    ]
    
    for field in model_b_fields:
        if hasattr(prompt, field):
            value = getattr(prompt, field)
            if value: 
                return True
    
    return False