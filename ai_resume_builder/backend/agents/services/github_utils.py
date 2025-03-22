import os
import git
import shutil
import time
import hashlib
import tiktoken

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# -------------------------------
# 토큰 계산기
# -------------------------------
def count_tokens(text, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


# -------------------------------
# 파일 해시 생성 (요약 캐싱용)
# -------------------------------
def get_content_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# -------------------------------
# 코드 블록을 안전하게 요약하는 함수 (자동 재시도)
# -------------------------------
def safe_summarize_code(code_text, model="gpt-4", max_retries=3, delay=5):
    llm = ChatOpenAI(temperature=0.3, model=model)

    prompt = PromptTemplate(
        input_variables=["code"],
        template="""
You are an expert in summarizing GitHub repositories.
Summarize the following code:
{code}
"""
    )

    chain = prompt | llm

    for attempt in range(max_retries):
        try:
            if count_tokens(code_text, model=model) > 80000:
                raise ValueError("Token limit exceeded for GPT-4.")
            return chain.invoke({"code": code_text})
        except Exception as e:
            print(f"⚠️ GPT summarization failed (attempt {attempt+1}): {e}")
            time.sleep(delay)
    return "⚠️ Summarization failed after retries."


# -------------------------------
# GitHub 저장소 클론
# -------------------------------
def clone_repo(github_url, clone_dir="repo_temp"):
    repo_name = github_url.strip().split("/")[-1]
    repo_path = os.path.join(clone_dir, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    git.Repo.clone_from(github_url, repo_path)
    return repo_name, repo_path


# -------------------------------
# 대형 파일 분할: 라인 기준으로 나누기
# -------------------------------
def split_by_lines(code, max_lines=150):
    lines = code.split("\n")
    return ["\n".join(lines[i:i+max_lines]) for i in range(0, len(lines), max_lines)]


# -------------------------------
# GitHub 전체 분석 및 안정형 요약
# -------------------------------
def analyze_github_repo(github_url):
    repo_name, repo_path = clone_repo(github_url)
    summaries = []
    cache = set()

    print(f"📦 Analyzing repo: {repo_name}")

    for root, _, files in os.walk(repo_path):
        for file in files:
            if not file.endswith((".py", ".js", ".ts")):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    if not content.strip():
                        continue

                    file_hash = get_content_hash(content)
                    if file_hash in cache:
                        print(f"⏩ Skipping already processed file: {file}")
                        continue

                    cache.add(file_hash)

                    # 🔹 split if large
                    if count_tokens(content) > 60000:
                        chunks = split_by_lines(content, max_lines=150)
                    else:
                        chunks = [content]

                    for idx, chunk in enumerate(chunks):
                        display_name = f"{file} (part {idx+1})" if len(chunks) > 1 else file
                        print(f"🔍 Summarizing {display_name}...")

                        summary = safe_summarize_code(chunk)
                        summaries.append(f"\n## {display_name}\n{summary}")

            except Exception as e:
                print(f"⚠️ Failed to process file {file_path}: {e}")

    # 🔸 전체 통합 요약 (모든 결과를 다시 요약)
    all_summaries = "\n\n".join(summaries)

    print("🧠 Generating final overall summary...")
    final_summary = safe_summarize_code(all_summaries)

    return repo_name, final_summary
