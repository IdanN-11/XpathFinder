import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")
BASE_URL = "https://api.x.ai/v1"
GROK_API_KEY=""

def ask_grok(html_doc="", prompt="", extra_context=""):
    """
    Send HTML and prompt to Grok API and return a dictionary of XPaths.
    html_doc, prompt, extra_context are all optional strings.
    """

    # Combine HTML, prompt, and extra context
    user_input = ""
    if html_doc:
        user_input += f"HTML:\n{html_doc}\n\n"
    if prompt:
        user_input += f"Prompt:\n{prompt}\n\n"
    if extra_context:
        user_input += f"Extra:\n{extra_context}\n\n"

    # Instruction to Grok
    system_prompt = (
        "You are an expert in HTML and web automation. "
        "Given the HTML and instructions, provide XPaths for the fields requested. "
        "Return a JSON object with keys as field names and values as XPaths. "
        "If a field has no XPath, you may skip it. "
        "Do not include any explanation or text outside the JSON. "
    )

    payload = {
        "model": "grok-2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0
    }

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/chat/completions"

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("❌ Grok API returned HTTP error:", err)
        print("Response body:", response.text)
        return {}
    except requests.exceptions.RequestException as err:
        print("❌ Network error when contacting Grok API:", err)
        return {}

    # Log full raw response
    print("🔹 Grok raw response:", response.text)

    res_data = response.json()

    # Extract content safely
    choices = res_data.get("choices")
    if not choices:
        print("❌ Grok API did NOT return choices.")
        return {}

    content = choices[0].get("message", {}).get("content", "")
    print("🔹 Grok content:", content)

    # Strip backticks and optional "json" tag
    content_clean = re.sub(r"^```(json)?\s*|```$", "", content.strip(), flags=re.IGNORECASE)
    print("🔹 Cleaned Grok content:", content_clean)

    # Parse JSON safely
    try:
        xpaths = json.loads(content_clean)
        if not isinstance(xpaths, dict):
            print("❌ Grok response is not a dict, ignoring")
            return {}
        return xpaths
    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON from Grok response, returning empty dict")
        return {}



