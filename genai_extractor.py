import os
import json
import azure_config
from openai import AzureOpenAI

# Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_config.AZURE_OPENAI_ENDPOINT,
    api_key=azure_config.AZURE_OPENAI_KEY,
    api_version=azure_config.AZURE_OPENAI_API_VERSION
)

def extract_timesheet(raw_text: str) -> dict:
    """
    Convert natural language timesheet text → structured JSON.
    """

    prompt = f"""
You are an assistant that extracts structured timesheet data.

Input:
{raw_text}

Return JSON with keys:
- date (YYYY-MM-DD or null)
- project (string or null)
- tasks (list of short bullet strings)
- start_time (HH:MM or null)
- end_time (HH:MM or null)
- total_hours (float or null)

If something is missing, use null.
Only output valid JSON. No explanation.
"""

    response = client.responses.create(
        model="gpt-4o-mini",   # Your company allowed model
        input=prompt,
        response_format={"type": "json_object"}
    )

    json_text = response.output[0].content[0].text
    return json.loads(json_text)
