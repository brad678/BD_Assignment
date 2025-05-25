import os
import dotenv
import json
import time
from typing import List
from pydantic import BaseModel, ValidationError
from openai import AzureOpenAI

# Pydantic model for validation
class MeetingNotes(BaseModel):
    summary: str
    action_items: List[str]

def get_aoai_client():
    # Azure OpenAI config
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g., 'gpt-4o-mini'

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-12-01-preview",  # 
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    return client, DEPLOYMENT_NAME

# Prompt function
def build_prompt(transcript: str) -> str:
    return f"""
    You are a meeting assistant.
    1. Summarize the meeting transcript below in exactly two sentences.
    2. Then list all action items mentioned, each as a separate bullet beginning with a dash.
    Return the result strictly as JSON with keys: "summary" and "action_items".
    
    Transcript:
    {transcript}
"""


def extract_meeting_notes(transcript: str, retries: int = 1) -> dict:
    
    client, DEPLOYMENT_NAME = get_aoai_client()
    
    prompt = build_prompt(transcript)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                temperature=0,
                messages=messages
            )
            content = response.choices[0].message.content
            data = json.loads(content)
            return MeetingNotes(**data).model_dump()
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt < retries:
                messages.insert(0, {"role": "system", "content": "Please output valid JSON only."})
                time.sleep(1)
            else:
                raise ValueError(f"Failed after {retries + 1} attempts. Error: {e}")
