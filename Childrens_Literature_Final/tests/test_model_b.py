import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from website.services.model_b import model_b
from website.services.model_b.cultural_profile import build_cultural_profile
from website.services.model_b.story_plan import generate_story_plan
from website.services.model_b.story_generation import generate_story
from website.services.model_b.validation import validate_story
from website.services.model_b.image_generation import generate_images

# --- Fake inputs for testing ---
fake_user_input = "A story about a brave little girl"
fake_user_metadata = {"age_group": "5-7", "region": "UK"}
fake_cluster_context = {"theme": "courage"}

# --- Stage 1: Cultural profile ---
def test_cultural_profile():
    profile = build_cultural_profile(fake_user_metadata, fake_cluster_context)
    assert isinstance(profile, dict)
    assert "region" in profile

# --- Stage 2: Story plan ---
def test_story_plan():
    profile = build_cultural_profile(fake_user_metadata, fake_cluster_context)
    plan = generate_story_plan(fake_user_input, profile)
    assert isinstance(plan, dict)
    assert "plot_beats" in plan

# --- Stage 3: Story generation ---
def test_story_generation():
    profile = build_cultural_profile(fake_user_metadata, fake_cluster_context)
    plan = generate_story_plan(fake_user_input, profile)
    story_text = generate_story(plan, profile)
    assert isinstance(story_text, str)
    assert len(story_text) > 0

# --- Stage 4: Validation ---
def test_story_validation():
    profile = build_cultural_profile(fake_user_metadata, fake_cluster_context)
    plan = generate_story_plan(fake_user_input, profile)
    story_text = generate_story(plan, profile)
    validated_story = validate_story(story_text, profile)
    assert isinstance(validated_story, str)
    assert len(validated_story) > 0

# --- Stage 5: Image generation ---
def test_image_generation():
    profile = build_cultural_profile(fake_user_metadata, fake_cluster_context)
    plan = generate_story_plan(fake_user_input, profile)
    images = generate_images(plan, profile)
    assert isinstance(images, list) or isinstance(images, dict)
