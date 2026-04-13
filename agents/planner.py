from langchain.chat_models import ChatOpenAI
import os
import json

# ✅ Get API key from Streamlit Secrets
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it in Streamlit Secrets.")

# ✅ Initialize LLM (Groq)
llm = ChatOpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ✅ Planner Agent
def planner_agent(task: str):
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

    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        return {"error": f"LLM failed: {str(e)}"}

    # Clean markdown if model still adds it
    cleaned = response.replace("```json", "").replace("```", "").strip()

    # Convert to JSON
    try:
        data = json.loads(cleaned)
    except Exception:
        return {
            "error": "Invalid JSON output",
            "raw_response": response
        }

    return data


# ✅ Local test
if __name__ == "__main__":
    user_input = "Build a calculator web app with add, subtract, multiply and divide"

    result = planner_agent(user_input)

    print("\nPlanner Output:")
    print(json.dumps(result, indent=4))
