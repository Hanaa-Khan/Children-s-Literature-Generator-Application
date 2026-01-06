from website import db
from sqlalchemy import func
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    consent = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.Date, nullable=False)
    prompt = db.relationship('Prompt', backref='user', lazy=True)
    story = db.relationship('Story', backref='user', lazy=True)

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_range = db.Column(db.String(150), nullable=False)
    character_name = db.Column(db.String(150))
    character_type = db.Column(db.String(150))
    character_traits = db.Column(db.Text, nullable=True)
    character_gender = db.Column(db.String(50), nullable=True) 
    location = db.Column(db.String(150))
    theme = db.Column(db.String(150))
    specific_traditions = db.Column(db.Text, nullable=True)
    character_cultural_background = db.Column(db.String(150), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stories = db.relationship('Story', backref='prompt', lazy=True)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(1), default='a')  # 'a' or 'b'
    cultural_profile = db.Column(db.Text, nullable=True)  # NULL for Model A
    character_profile = db.Column(db.Text, nullable=True)  # NULL for Model A
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship("StoryImage", backref="story", lazy=True)

class StoryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("story.id"), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    phase = db.Column(db.String(20))  # "beginning", "middle", "end"
    phase_description = db.Column(db.Text, nullable=True)  # NULL for Model A
    created_at = db.Column(db.DateTime, default=datetime.utcnow)