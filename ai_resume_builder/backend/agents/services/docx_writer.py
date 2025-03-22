import os
from docx import Document
from docx.shared import Pt, RGBColor

def generate_resume_docx(projects, template_path="templates/resume_template.docx", output_path="generated_resume.docx"):
    """
    여러 프로젝트 정보를 기반으로 이력서를 생성합니다.

    Args:
        projects (list): 각 프로젝트에 대한 딕셔너리 리스트.
                         각 딕셔너리는 다음 키를 포함할 수 있음:
                         - "name": 프로젝트 이름
                         - "description": 프로젝트 설명/요약
                         - "link": GitHub URL 등 프로젝트 링크
        template_path (str): 사용할 이력서 템플릿 경로. 템플릿이 없으면 새 문서를 생성.
        output_path (str): 생성된 이력서를 저장할 파일 경로.

    Returns:
        str: 생성된 이력서 파일의 경로 (output_path).
    """
    # 템플릿 파일이 존재하면 로드, 없으면 새 Document 생성
    if os.path.exists(template_path):
        doc = Document(template_path)
    else:
        doc = Document()
        # 기본 제목 추가
        title = doc.add_heading("Developer Resume", level=0)
        title.alignment = 1  # 가운데 정렬
        doc.add_paragraph("This resume has been automatically generated based on your GitHub projects.")

    # 프로젝트별 정보 추가
    doc.add_heading("Projects", level=1)
    for project in projects:
        # 프로젝트 이름 (헤딩)
        project_name = project.get("name", "Unnamed Project")
        doc.add_heading(project_name, level=2)

        # 프로젝트 설명 (tuple 등 처리)
        description = project.get("description", "No description provided.")
        if not isinstance(description, str):
            description = str(description[0]) if isinstance(description, tuple) else str(description)
        para_desc = doc.add_paragraph(description)
        para_desc.style.font.size = Pt(11)

        # 프로젝트 링크
        link = project.get("link", "")
        if link:
            para_link = doc.add_paragraph()
            run_link = para_link.add_run("Project Link: " + link)
            run_link.font.size = Pt(10)
            run_link.font.color.rgb = RGBColor(0, 0, 255)  # 파란색으로 표시

        # 구분선 추가
        doc.add_paragraph("---------------------------")

    # 생성된 문서를 저장
    doc.save(output_path)
    return output_path

# 단독 실행 시 테스트 코드
if __name__ == "__main__":
    # 예시 프로젝트 리스트
    sample_projects = [
        {
            "name": "AutoGen",
            "description": "AutoGen is a framework for building multi-agent systems that automate complex tasks.",
            "link": "https://github.com/microsoft/autogen"
        },
        {
            "name": "LangChain",
            "description": "LangChain is a framework for developing applications powered by language models.",
            "link": "https://github.com/hwchase17/langchain"
        }
    ]

    output_file = generate_resume_docx(sample_projects)
    print(f"Resume generated and saved to: {output_file}")
