from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def generate_readme(repo_name: str, project_summary: str) -> str:
    """
    주어진 프로젝트 이름과 요약 내용을 바탕으로, 전문적인 README.md 파일의 마크다운 텍스트를 생성합니다.
    
    Args:
        repo_name (str): GitHub 저장소 이름
        project_summary (str): GitHub 저장소의 코드 분석 및 요약 내용
        
    Returns:
        str: 생성된 README.md 내용 (Markdown 형식)
    """
    # LLM 초기화 (필요에 따라 model_name 및 temperature 조정)
    llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")

    # README 생성용 프롬프트 템플릿
    prompt_template = PromptTemplate(
        input_variables=["repo_name", "project_summary"],
        template="""
You are a professional technical writer who specializes in writing high-quality README.md files for GitHub projects.
Based on the following project details, generate a comprehensive README.md that includes the following sections:
1. **Project Name:** The name of the project.
2. **Overview:** A brief description of what the project does.
3. **Features:** Key functionalities and unique aspects.
4. **Installation:** Instructions on how to install and set up the project.
5. **Usage:** Examples and guidelines for using the project.
6. **Contributing:** Guidelines for contributors.
7. **License:** A placeholder if the license is not specified.
8. **Contact:** Information for further communication.

Project Name: {repo_name}

Project Description:
{project_summary}

Generate the README in markdown format. Make sure the output is clear, concise, and professional.
"""
    )

    # LLMChain를 생성하여 프롬프트와 LLM을 연결
    chain = LLMChain(prompt=prompt_template, llm=llm)
    readme_md = chain.run(repo_name=repo_name, project_summary=project_summary)
    
    return readme_md

# 샘플 실행 (단독 실행 시)
if __name__ == "__main__":
    # 예시 입력
    sample_repo_name = "autogen"
    sample_summary = (
        "AutoGen is a framework that provides a multi-agent system for automating "
        "complex tasks using language models. It allows agents to collaborate via "
        "group chats, perform iterative reasoning, and integrate with external tools."
    )
    
    readme = generate_readme(sample_repo_name, sample_summary)
    print("Generated README.md:\n")
    print(readme)
