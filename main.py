
import requests
import json
import os
from openai import OpenAI

# Ladataan konfiguraatio
with open("config.json", "r") as f:
    config = json.load(f)

TOPIC = config["topic"]
LANGUAGE = config.get("language", "fi")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# OpenAI API
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def fetch_news(topic):
    # Placeholder: voit korvata esim. RSS-feedillä tai web-scraperilla
    return f"Tässä on esimerkkisisältö aiheesta '{topic}'."

def summarize(text, topic):
    prompt = f"Tiivistä seuraava sisältö viikkokatsaukseksi aiheesta '{topic}' ({LANGUAGE}):\n\n{text}"
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()

def post_to_slack(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise Exception(f"Slack posting failed: {response.text}")

if __name__ == "__main__":
    source_text = fetch_news(TOPIC)
    summary = summarize(source_text, TOPIC)
    post_to_slack(summary)
