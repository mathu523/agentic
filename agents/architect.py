import os
import json
import requests


# 🏗️ Architect Agent
def architect_agent(plan: dict):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {"error": "GROQ_API_KEY missing"}

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a software architect.

    Based on this project plan, generate a file structure.

    Return ONLY valid JSON.
    Do NOT include markdown.

    Format:
    {{
        "files": ["file1", "file2", "file3"]
    }}

    Plan:
    {plan}
    """

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        content = result["choices"][0]["message"]["content"]

        # Clean markdown if present
        cleaned = content.replace("```json", "").replace("```", "").strip()

        return json.loads(cleaned)

    except Exception as e:
        return {
            "error": str(e),
            "raw_response": response.text if 'response' in locals() else None
        }


# 🚀 Test
if __name__ == "__main__":
    sample_plan = {
        "project_name": "calculator_web_app",
        "features": [
            "addition",
            "subtraction",
            "multiplication",
            "division"
        ],
        "tech_stack": ["HTML", "CSS", "JavaScript"]
    }

    result = architect_agent(sample_plan)

    print("\n✅ Architect Output:")
    print(json.dumps(result, indent=4))
