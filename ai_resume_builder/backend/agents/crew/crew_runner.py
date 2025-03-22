import os
from crewai import Crew
from .agents import code_summarizer, readme_writer
from .tasks import define_tasks
from .utils import clone_repo, extract_code_snippets

def run_crew_pipeline(github_url: str):
    try:
        print("🚀 GitHub 저장소 클론 중...")
        repo_name, repo_path = clone_repo(github_url)

        print("📁 코드 파일 스캔 중...")
        code_snippets = extract_code_snippets(repo_path)

        if len(code_snippets) > 3000:
            print("✂️ 코드 요약 길이 제한 적용됨 (3000자)")
            code_snippets = code_snippets[:3000] + "\n\n...(truncated)"

        print("📋 Crew 태스크 정의 중...")
        tasks = define_tasks(code_summarizer, readme_writer, code_snippets)

        print("🧑‍💻 Crew 구성 및 실행 중...")
        crew = Crew(
            agents=[code_summarizer, readme_writer],
            tasks=tasks,
            verbose=True,
            max_iterations=10,         # 기본은 5
            max_execution_time=900     # 15분
        )

        print("🚦 Crew 실행 시작 (kickoff)...")
        result = crew.kickoff()
        print("✅ Crew 실행 완료!")

        # 결과 저장
        output_path = f"generated_readmes/{repo_name}_README.md"
        os.makedirs("generated_readmes", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        return output_path, result

    except Exception as e:
        print("❌ CREW 실행 중 에러 발생:", str(e))
        raise