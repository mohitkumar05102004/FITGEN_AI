import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_fitness_plan(user):
    prompt = f"""
Generate a personalized 7-day workout and diet plan.

Name: {user.name}
Age: {user.age}
Gender: {user.gender}
Height: {user.height} cm
Weight: {user.weight} kg
Goal: {user.goal}
Activity: {user.activity}
Diet: {user.diet}
Budget: ₹{user.budget}
Workout Days: {user.workout_days}

Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert fitness coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content