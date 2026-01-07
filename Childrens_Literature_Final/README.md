# Personalized AI-Generated Children’s Storybook System

## Overview
This project presents a web-based system for generating personalized, illustrated children’s stories using artificial intelligence. The application allows users to provide personalization inputs such as age and character traits, which are then used to generate a coherent narrative and corresponding illustrations.  

The project was developed as part of a Master’s dissertation and explores challenges related to prompt engineering, narrative coherence, visual consistency, and cultural representation in AI-generated children’s media.

---

## Features
- Web-based user interface built with Flask
- Personalized story generation using large language models
- AI-generated illustrations with enforced style and character consistency
- Validation layer for narrative coherence and age-appropriate content
- Story export functionality (PDF format)
- Modular model architecture supporting multiple generation pipelines

---

## Tech Stack
- **Programming Language:** Python 3.11
- **Backend Framework:** Flask
- **Database:** SQLAlchemy (SQLite during development)
- **AI / NLP:** OpenAI API, Hugging Face Transformers, Sentence Transformers
- **Image Generation:** Custom model pipelines (Model A and Model B)
- **Frontend:** HTML, CSS, Jinja2 Templates
- **Utilities:** Torch, Pillow, WeasyPrint / FPDF

---

## Project Structure
website/
├── routes/ # Flask route definitions
├── models/
│ └── database.py # SQLAlchemy models
├── services/
│ ├── model_a/ # Story text generation pipeline
│ ├── model_b/ # Image generation and validation pipeline
│ └── shared/
│ └── llm.py # Shared LLM utilities
├── templates/ # Jinja2 HTML templates
├── static/ # CSS and static assets
├── app.py # Application entry point
└── requirements.txt


---

## Installation

### Prerequisites
- Python 3.11 or later
- pip
- Virtual environment tool (recommended)

### Setup Instructions

1. Clone the repository: Clone the repository:
```bash
git clone <repository-url>
'''

2. Create and activate a virtual environment:
cd <project-directory>
pip install -r requirements.txt

3. Install dependencies:
pip install -r requirements.txt

4. Create a .env file in the project root:
OPENAI_API_KEY=your_openai_api_key_here

## Running the Application
flask run
http://127.0.0.1:5000
