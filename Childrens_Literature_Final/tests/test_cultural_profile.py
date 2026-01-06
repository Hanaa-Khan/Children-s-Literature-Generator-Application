# tests/test_cultural_profile.py

import pytest
from website.services.model_b.cultural_profile import build_cultural_profile

def test_build_cultural_profile_minimal():
    # Minimal mock inputs
    user_metadata = {"name": "Test User"}
    cluster_context = {
        "location": "Mexico",
        "theme": "adventure",
        "cultural_background": "Mayan",
        "specific_traditions": "food, festivals",
        "region": "Yucatan"
    }

    profile = build_cultural_profile(user_metadata, cluster_context)

    # Check main structure
    assert "user_context" in profile
    assert "cultural_inputs" in profile
    assert "storytelling_guidelines" in profile

    # Check user_context fields
    uc = profile["user_context"]
    assert uc["age_group"] == "7-9"
    assert uc["location"] == "Mexico"
    assert uc["theme"] == "adventure"
    assert uc["character_background"] == "Mayan"

    # Check cultural_inputs fields
    ci = profile["cultural_inputs"]
    assert ci["background"] == "Mayan"
    assert ci["traditions"] == "food, festivals"
    assert ci["region"] == "Yucatan"

    # Check storytelling guidelines
    guidelines = profile["storytelling_guidelines"]
    assert isinstance(guidelines, list)
    assert "Create authentic characters" in guidelines
