import os
from dotenv import load_dotenv
from sarvamai import SarvamAI
from core.loaders import load_config

config = load_config()
model_name = config["model"]["name"]

load_dotenv()

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)


def chat(messages, tools=None):
    return client.chat.completions(model=model_name, messages=messages, tools=tools)