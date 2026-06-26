import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Order matters.
# Fastest & most reliable free models first.
MODELS = [
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "openai/gpt-oss-120b:free",
    "openai/gpt-oss-20b:free",
    "meta-llama/llama-3.2-3b-instruct:free"
]


def clean_json(text):
    """Remove markdown if AI returns it."""
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")

    if text.startswith("```"):
        text = text.replace("```", "")

    if text.endswith("```"):
        text = text.replace("```", "")

    return text.strip()


def generate_fitness_plan(user):

    prompt = f"""
You are a professional fitness trainer and certified nutritionist.

Create a personalized 7-day workout and diet plan.

User Details

Name: {user.name}
Age: {user.age}
Gender: {user.gender}

Height: {user.height} cm
Weight: {user.weight} kg

Goal: {user.goal}

Activity Level: {user.activity}

Diet Preference: {user.diet}

Budget: ₹{user.budget} per day

Workout Days: {user.workout_days}

Return ONLY valid JSON.

Example:

{{
    "workout": {{
        "Monday": [
            "Push-ups",
            "Squats",
            "Running"
        ],
        "Tuesday": [
            "Bench Press",
            "Deadlift"
        ]
    }},
    "diet": {{
        "Breakfast": "Oats + Milk",
        "Lunch": "Rice + Dal",
        "Dinner": "Paneer + Salad"
    }},
    "water": "3 Litres",
    "motivation": "Stay consistent!"
}}

Do not write any explanation.
Do not use markdown.
Return only JSON.
"""

    last_error = None

    for model_name in MODELS:

        print("=" * 60)
        print("Trying model:", model_name)

        for attempt in range(3):

            try:

                response = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            "role": "system",
            "content": "You are an expert fitness coach and nutritionist."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.7,
    max_tokens=2000,
    extra_headers={
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "FitGenAI"
    }
)

                text = response.choices[0].message.content

                text = clean_json(text)

                data = json.loads(text)

                print("SUCCESS")
                print("Model Used:", model_name)

                return data

            except json.JSONDecodeError:

                print("AI returned invalid JSON")
                print(text)

                last_error = Exception("Invalid JSON returned by AI")
                break

            except Exception as e:

                print("Attempt", attempt + 1, "failed")
                print(e)

                last_error = e

                if "429" in str(e):
                    print("Rate limited... waiting 10 seconds")
                    time.sleep(10)
                else:
                    break

    raise last_error

def ask_ai(message):
    prompt = f"""
    You are FitGen AI.

You are an expert fitness trainer and nutritionist.

Answer the user's question in simple language.

Keep the answer below 200 words.

Question:

{message}
"""

    last_error = None

    for model_name in MODELS:

        try:

            response = client.chat.completions.create(

                model=model_name,

                messages=[

                    {

                        "role": "system",

                        "content": "You are an expert fitness coach."

                    },

                    {

                        "role": "user",

                        "content": prompt

                    }

                ],

                temperature=0.7,

                max_tokens=500,

                extra_headers={

                    "HTTP-Referer": "http://localhost:5000",

                    "X-Title": "FitGenAI"

                }

            )

            return response.choices[0].message.content

        except Exception as e:

            last_error = e

    return f"Error: {last_error}"