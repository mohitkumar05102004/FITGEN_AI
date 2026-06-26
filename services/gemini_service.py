import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the latest stable Flash model
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_fitness_plan(user):

    prompt = f"""
You are an expert fitness coach and certified nutritionist.

Generate a personalized 7-day workout and diet plan.

User Details

Name: {user.name}
Age: {user.age}
Gender: {user.gender}
Height: {user.height}
Weight: {user.weight}

Goal: {user.goal}

Activity: {user.activity}

Diet: {user.diet}

Budget: {user.budget} INR/day

Workout Days: {user.workout_days}

Return ONLY valid JSON.

Do NOT use markdown.

Example:

{{
"workout": {{
"Monday":["Push Ups","Squats"],
"Tuesday":["Running","Plank"]
}},
"diet": {{
"Breakfast":"Oats",
"Lunch":"Rice + Dal",
"Dinner":"Paneer"
}},
"water":"3 Litres",
"motivation":"Stay consistent!"
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if Gemini returns it
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)