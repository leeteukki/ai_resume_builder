from crewai import Task

def define_tasks(code_summarizer, readme_writer, code_snippets):
    summarize_task = Task(
        description=f"Summarize the following code:\n\n{code_snippets}",
        expected_output="Concise summary of the codebase.",
        agent=code_summarizer,
        tools=[]  # ✅ 강제로 tool 비활성화 → LLM만 사용하게 함
    )

    write_readme_task = Task(
        description="Create a professional README based on the summary.",
        expected_output="Markdown-formatted README.md",
        agent=readme_writer,
        tools=[]  # ✅ 마찬가지로 tools 제거
    )

    return [summarize_task, write_readme_task]