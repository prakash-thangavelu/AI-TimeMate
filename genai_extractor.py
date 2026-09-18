import streamlit as st
import json
import azure_config
from openai import AzureOpenAI
from datetime import datetime, timedelta
from pathlib import Path
from string import Template

# Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_config.AZURE_OPENAI_ENDPOINT,
    api_key=azure_config.AZURE_OPENAI_KEY,
    api_version=azure_config.AZURE_OPENAI_API_VERSION
)

def extract_timesheet(raw_text: str) -> dict:
    assigned_project = st.session_state["assigned_project"]

    #inform the model about current
    current_date = datetime.now()
    today = current_date.strftime("%Y-%m-%d")

    # Format as "YYYY-MM-DD (DayName)"
    today_with_day = current_date.strftime("%Y-%m-%d (%A)")

    # Calculate Monday of current week
    this_monday = current_date - timedelta(days=current_date.weekday())
    this_friday = this_monday + timedelta(days=4)

    # Calculate Monday of last week
    last_monday = this_monday - timedelta(days=7)
    last_friday = last_monday + timedelta(days=4)

    # 1. Read the text file content
    template_content = Path("prompts/extraction_prompt.txt").read_text(encoding="utf-8")

    # 2. Pass string content to string.Template
    prompt_template = Template(template_content)

    # 3. Substitute values
    prompt = prompt_template.safe_substitute(
        TODAY_WITH_DAY=today_with_day,
        PROJECT_NAME=assigned_project,
        TODAY=today,
        THIS_MONDAY=this_monday,
        THIS_FRIDAY=this_friday,
        LAST_MONDAY=last_monday,
        LAST_FRIDAY=last_friday,
        RAW_TEXT=raw_text
    )

    # print(prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract structured timesheet data and return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  # more stable JSON
    )

    # raw_output = response.choices[0].message["content"]
    raw_output = response.choices[0].message.content


    try:
        return json.loads(raw_output)
    except Exception:
        # fallback: return raw text so UI won't crash
        return {
            "error": "Invalid JSON",
            "raw": raw_output
        }
