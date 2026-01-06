import pytest
from website import create_app, db
from datetime import date
from website.models.database import User, Prompt
import json

# create a Flask app with test config
@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_data(app):
    with app.app_context():
        user = User(
            first_name="Alice",
            last_name="Smith",
            consent=True,
            date=date(2026, 1, 6)  
        )
        db.session.add(user)
        db.session.commit()

        prompt = Prompt(
            user_id=user.id,
            age_range="7-9",
            character_name="Charlie",
            character_type="human",
            character_gender="female",
            character_traits="curious, kind",
            location="forest",
            theme="adventure",
            character_cultural_background="Brazil",
            specific_traditions="food"
        )
        db.session.add(prompt)
        db.session.commit()

        yield user, prompt


def test_generate_story_api_model_a(client, sample_data):
    user, prompt = sample_data
    response = client.get("/generate_story_api", query_string={
        "prompt": f"This story is for children aged {prompt.age_range}. The main character is named {prompt.character_name}.",
        "user_id": user.id,
        "prompt_id": prompt.id,
        "model": "a"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "story" in data
    assert isinstance(data["images"], list)  
    assert data["model_used"] == "a"
