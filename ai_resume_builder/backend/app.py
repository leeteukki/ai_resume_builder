import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.crew.crew_runner import run_crew_pipeline
from agents.services.docx_writer import generate_resume_docx

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    github_url = data.get("github_url")

    if not github_url:
        return jsonify({"error": "GitHub URL is required"}), 400

    try:
        # Crew 실행 (README.md 생성)
        readme_path, readme_content = run_crew_pipeline(github_url)

        # ✅ 이력서 생성
        projects = [{
            "name": github_url.strip().split("/")[-1],
            "description": readme_content,
            "link": github_url
        }]
        resume_path = generate_resume_docx(projects)  # docx 파일 생성

        # ✅ .docx 파일을 base64 인코딩해서 JSON으로 보내기
        with open(resume_path, "rb") as f:
            resume_bytes = f.read()
            resume_base64 = base64.b64encode(resume_bytes).decode("utf-8")

        return jsonify({
            "success": True,
            "readmes": [
                {
                    "repo_name": projects[0]["name"],
                    "readme_md": readme_content
                }
            ],
            "resume_docx": resume_base64  # ✅ base64 인코딩된 docx 파일
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)