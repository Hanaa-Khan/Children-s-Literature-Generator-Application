from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import traceback
from flask import send_file
from .models.database import StoryImage, db, User, Prompt, Story
from website.services.model_a.model_a import run_model_a
from website.services.model_b.model_b import run_model_b

routes = Blueprint('routes', __name__)

# ---------- Home Page ------------
@routes.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print("FULL FORM DATA:", request.form)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_str = request.form.get('event_date')
        consent = request.form.get('consent') == 'on'
        if not consent:
            flash('You must give consent before generating a story.', 'error')
            return redirect(url_for('routes.home'))

        if not first_name or not last_name or not date_str:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('routes.home'))

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "error")
            return redirect(url_for('routes.home'))

        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                consent=consent,
                date=date_obj
            )
            db.session.add(new_user)
            db.session.commit()
            print("NEW USER ID:", new_user.id)
        except Exception as e:
            db.session.rollback()
            print("ERROR saving new user:", e)
            flash("Error saving user. Please try again.", "error")
            return redirect(url_for('routes.home'))

        return redirect(url_for('routes.create_story', user_id=new_user.id))

    return render_template('home.html')


# --------- Create Story Page -----------
@routes.route('/create_story', methods=['GET', 'POST'])
def create_story():
    user_id_str = request.args.get('user_id') or request.form.get('user_id')
    if not user_id_str:
        return "User ID missing", 400
    user_id = int(user_id_str)

    if request.method == 'POST':
        print("FORM:", request.form)
        age_range = request.form.get('age_range')
        character_name = request.form.get('character_name')
        character_gender = request.form.get('character_gender', 'unspecified') 
        character_type = request.form.get('character_type')
        traits_list = request.form.getlist('traits')
        traits = ", ".join(traits_list) if traits_list else None
        location = request.form.get('location')
        theme = request.form.get('theme')
        model_choice = request.form.get('model_choice') or 'b'
        character_cultural_background = request.form.get('character_cultural_background', '')
        specific_traditions = request.form.get('specific_traditions', '')

        new_prompt = Prompt(
            age_range=age_range,
            character_name=character_name or None,
            character_type=character_type or None,
            character_traits=traits if traits is not None else None,
            location=location or None,
            theme=theme or None,
            character_gender=character_gender,
            specific_traditions=specific_traditions if specific_traditions else None,
            character_cultural_background=character_cultural_background if character_cultural_background else None,
            user_id=user_id
        )
        
        try:
            db.session.add(new_prompt)
            db.session.commit()
            print(f"Prompt saved with ID: {new_prompt.id}, Model: {model_choice}, Gender: {character_gender}")
        except Exception as e:
            db.session.rollback()
            print("Error saving prompt:", e)
            flash("Error saving prompt. Please try again.", "error")
            return redirect(url_for('routes.create_story', user_id=user_id))

        return redirect(url_for('routes.view_story', 
                              user_id=user_id, 
                              prompt_id=new_prompt.id,
                              model=model_choice))

    user = User.query.get(user_id)
    return render_template('create_story.html', user_id=user_id, user=user)


# ---------- View Story Page -------------
@routes.route('/view_story', methods=['GET'])
def view_story():
    prompt_id = request.args.get('prompt_id')
    prompt = Prompt.query.get(prompt_id)
    
    if not prompt:
        return "Prompt not found", 404
    
    user_id = prompt.user_id
    model_choice = choose_model_for_user(user_id)

    parts = []
    parts.append(f"This story is for children aged {prompt.age_range}.")
    
    if prompt.character_name:
        parts.append(f"The main character is named {prompt.character_name}.")
    
    if prompt.character_type:
        parts.append(f"The character is a {prompt.character_type}.")
    
    if prompt.character_gender:
        parts.append(f"The character is {prompt.character_gender}.")
    
    if prompt.character_traits:
        parts.append(f"Character traits: {prompt.character_traits}.")
    
    if prompt.location:
        parts.append(f"Setting: {prompt.location}.")
    
    if prompt.theme:
        parts.append(f"Theme: {prompt.theme}.")

    if prompt.character_cultural_background:
        parts.append(f"Culturally inspired by: {prompt.character_cultural_background}.")
        
    if prompt.specific_traditions:
        parts.append(f"Traditions included: {prompt.specific_traditions}.")
        

    final_prompt = " ".join(parts).strip()
    print("FINAL PROMPT:", final_prompt)
    
    return render_template("view_story.html", 
                         final_prompt=final_prompt,
                         prompt=prompt,
                         model_choice=model_choice,
                         user_id=prompt.user_id)

# --------- Generate Story API -------------
@routes.route("/generate_story_api")
def generate_story_api():
    prompt_text = request.args.get("prompt")
    user_id = request.args.get("user_id")
    prompt_id = request.args.get("prompt_id")
    model_choice = choose_model_for_user(user_id)
    story_text = ""
    images = []
    character_profile = {}
    cultural_profile = {}
    user = User.query.get(user_id)
    prompt_obj = Prompt.query.get(prompt_id) if prompt_id else None

    try:
        # Calling Model B
        if model_choice == "b" and user and prompt_obj:
            raw_traits = prompt_obj.character_traits or ""
            traits_list = [
                t.strip()
                for t in raw_traits.replace(";", ",").split(",")
                if t.strip()
            ]
            if not traits_list:
                traits_list = ["curious", "kind"]

            traits_text = ", ".join(traits_list)
            user_input_dict = {
                "prompt_text": prompt_text,
                "character_name": prompt_obj.character_name or "Child",
                "age_range": prompt_obj.age_range or "4-6",
                "character_type": prompt_obj.character_type or "human",
                "traits": traits_list,
                "traits_text": traits_text,  
                "location": prompt_obj.location or "",
                "theme": prompt_obj.theme or "adventure",
                "character_gender": prompt_obj.character_gender or "unspecified"
            }
            user_metadata = {
                "first_name": user.first_name,
            }
            cluster_context = {
                "cultural_background": prompt_obj.character_cultural_background or "",
                "specific_traditions": prompt_obj.specific_traditions or "",
            }
            print("USING TRAITS:", traits_list)
            result = run_model_b(
                user_input=user_input_dict,
                user_metadata=user_metadata,
                cluster_context=cluster_context
            )
            story_text = result.get("story_text", "")
            images = result.get("images", [])
            character_profile = result.get("character_profile", {})
            cultural_profile = result.get("cultural_profile", {})

            if not images:
                raise ValueError("Model B returned no images")

        #  Calling Model A
        elif model_choice == "a":
            print("USING MODEL A")

            result = run_model_a(
                user_input={
                    "prompt_text": prompt_text
                },
                user_metadata={},
                cluster_context={}
            )

            story_text = result["story_text"]
            images = result["images"]
            character_profile = result.get("character_profile", {})
            cultural_profile = result.get("cultural_profile", {})

        else:
            raise ValueError("Invalid model choice or missing data")


    except Exception as e:
        print("Primary generation failed:", e)
        traceback.print_exc()

        try:
            print("FALLING BACK TO MODEL A")

            result = run_model_a(
                user_input={"prompt_text": prompt_text},
                user_metadata={},
                cluster_context={}
            )

            story_text = result["story_text"]
            images = result["images"]
            character_profile = result.get("character_profile", {})
            cultural_profile = result.get("cultural_profile", {})
            model_choice = "a"

        except Exception as e2:
            print("Fallback also failed:", e2)
            story_text = "Error generating story. Please try again."
            images = ["/static/fallback_image.png"] * 3


    # Save story
    title = story_text.splitlines()[0][:200] if story_text else "Untitled Story"

    if story_text and user_id:
        new_story = Story(
            title=title,
            content=story_text,
            user_id=int(user_id),
            prompt_id=int(prompt_id) if prompt_id else None,
            model_used=model_choice,
            cultural_profile=json.dumps(cultural_profile) if cultural_profile else None,
            character_profile=json.dumps(character_profile) if character_profile else None
        )
        db.session.add(new_story)
        db.session.commit()

        phases = ["beginning", "middle", "end"]
        for i, img_url in enumerate(images[:3]):
            db.session.add(
                StoryImage(
                    story_id=new_story.id,
                    image_url=img_url,
                    phase=phases[i]
                )
            )
        db.session.commit()

    return jsonify({
        "story": story_text,
        "images": images,
        "model_used": model_choice,
        "success": True
    })

def choose_model_for_user(user_id: int) -> str:
    user_id = int(user_id)
    if user_id % 2 == 0:
        return "b"
    return "a"


