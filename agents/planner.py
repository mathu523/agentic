import os
import json
import requests

# ✅ Planner Agent
def planner_agent(task: str):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {"error": "GROQ_API_KEY is missing"}

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are a software planning assistant.

    Return ONLY valid JSON.
    Do NOT include markdown (no ```).

    JSON format:
    {{
        "project_name": "string",
        "features": ["feature1", "feature2"],
        "tech_stack": ["tech1", "tech2"]
    }}

    Request:
    {task}
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


# ✅ Local test
if __name__ == "__main__":
    user_input = "Build a calculator web app with add, subtract, multiply and divide"

    result = planner_agent(user_input)

    print("\nPlanner Output:")
    print(json.dumps(result, indent=4))
