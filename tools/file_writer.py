import os

def write_file(project_name: str, file_name: str, content: str):
    try:
        # Create project folder
        project_path = os.path.join(os.getcwd(), project_name)
        os.makedirs(project_path, exist_ok=True)

        # Support nested folders (e.g., src/app.js)
        file_path = os.path.join(project_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "status": "success",
            "file": file_name,
            "path": file_path
        }

    except Exception as e:
        return {
            "status": "error",
            "file": file_name,
            "message": str(e)
        }
