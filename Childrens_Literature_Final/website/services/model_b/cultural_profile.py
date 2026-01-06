
from website.services.shared.llm import call_gpt 

def build_cultural_profile(user_metadata, cluster_context): 
    """ Build a simplified cultural profile. """ 
    profile = { 
        "user_context": { 
            "age_group": "7-9", 
            "location": cluster_context.get("location", ""), 
            "theme": cluster_context.get("theme", "adventure"), 
            "character_background": cluster_context.get("cultural_background", "") 
        }, 
        "cultural_inputs": { 
            "background": cluster_context.get("cultural_background", ""), 
            "traditions": cluster_context.get("specific_traditions", ""), 
            "region": cluster_context.get("region", "") 
        },
        "storytelling_guidelines": [ 
            "Create authentic characters", 
            "Include cultural elements naturally", 
            "Focus on positive representation", 
            "Make it age-appropriate" 
        ] 
    } 
    return profile