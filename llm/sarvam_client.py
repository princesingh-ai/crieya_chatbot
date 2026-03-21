import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)


def chat(messages, tools=None):
    request = {
        "model": "sarvam-105b",
        "messages": messages,
    }

    if tools:
        request["tools"] = tools

    return client.chat.completions(**request)