import os
import git

def clone_repo(github_url, clone_dir="repo_temp"):
    repo_name = github_url.strip().split("/")[-1]
    repo_path = os.path.join(clone_dir, repo_name)

    if not os.path.exists(repo_path):
        git.Repo.clone_from(github_url, repo_path)
    return repo_name, repo_path

def extract_code_snippets(repo_path, max_files=5):
    code_texts = []
    count = 0
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts")):
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    snippet = content[:1500]
                    code_texts.append(f"### {file}\n```python\n{snippet}\n```")
                    count += 1
                    if count >= max_files:
                        return "\n\n".join(code_texts)
    return "\n\n".join(code_texts)