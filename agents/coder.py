import os
import json
import requests

# 📁 File Writer
def write_file(project_name, file_name, content):
    os.makedirs(project_name, exist_ok=True)

    file_path = os.path.join(project_name, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created: {file_name}")


# 👨‍💻 Coder Agent
def coder_agent(plan: dict, architecture: dict):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {"error": "GROQ_API_KEY missing"}

    project_name = plan["project_name"].lower().replace(" ", "_")
    files = architecture["files"]

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    for file in files:
        print(f"⚡ Generating {file}...")

        prompt = f"""
        You are a professional software developer.

        Generate complete code for the file: {file}

        Project details:
        {plan}

        Rules:
        - Return ONLY code
        - No explanations
        - No markdown
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
            cleaned = content.replace("```", "").strip()

            write_file(project_name, file, cleaned)

        except Exception as e:
            print(f"❌ Error generating {file}: {e}")

    return f"🎉 Project '{project_name}' created successfully!"


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

    sample_architecture = {
        "files": [
            "index.html",
            "style.css",
            "script.js",
            "addition.js",
            "subtraction.js",
            "multiplication.js",
            "division.js"
        ]
    }

    result = coder_agent(sample_plan, sample_architecture)
    print(result)
