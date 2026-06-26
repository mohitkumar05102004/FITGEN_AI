from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

models = client.models.list()

print("\nFREE MODELS\n")

for model in models.data:
    model_id = model.id
    if ":free" in model_id:
        print(model_id)
        