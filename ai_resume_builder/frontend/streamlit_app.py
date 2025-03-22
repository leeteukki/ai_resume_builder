import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="AI Dev Profile Builder",
    layout="wide",
    page_icon="🤖"
)

st.title("🤖 AI Dev Profile Builder")
st.markdown("GitHub 프로젝트 URL을 입력하면 AI가 자동으로 `README.md`와 `.docx 이력서`를 생성해줍니다.")

# 좌우 컬럼 나누기 (왼쪽: 입력 / 오른쪽: 로그)
col_left, col_right = st.columns([2, 1])  # 비율 2:1

with col_left:
    st.subheader("📌 GitHub 주소 입력")
    urls_input = st.text_area(
        "한 줄에 하나씩 입력해주세요",
        placeholder="https://github.com/사용자/프로젝트명",
        height=150
    )
    url_list = [url.strip() for url in urls_input.split("\n") if url.strip()]
    start_button = st.button("🚀 분석 시작")

with col_right:
    st.subheader("🖥️ 진행 로그")
    log_area = st.empty()  # 로그 출력 영역

def push_log(logs, new_msg):
    logs.append(new_msg)
    log_area.markdown("🪵 **작업 로그:**\n" + "\n".join(f"- {log}" for log in logs))

# 분석 시작 시
if start_button and url_list:
    logs = []
    with st.spinner("에이전트들이 열심히 작업 중입니다... 🧠"):
        try:
            push_log(logs, "🔍 백엔드 요청 보내는 중...")

            response = requests.post(
                "http://localhost:8000/analyze",
                json={"github_url": url_list[0]}
            )

            push_log(logs, "📦 백엔드 응답 처리 중...")
            data = response.json()

            push_log(logs, "📄 README.md 렌더링 중...")
            st.success("🎉 분석 완료! 아래에서 결과를 확인하세요.")
            push_log(logs, "✅ 완료!")

            # 3. 프로젝트별 README 결과 출력
            st.subheader("📄 생성된 README.md 미리보기")
            for item in data["readmes"]:
                with st.expander(f"📘 {item['repo_name']}"):
                    st.code(item["readme_md"], language="markdown")

            # 4. 이력서 다운로드
            st.subheader("📋 통합 이력서 다운로드")
            resume_bytes = base64.b64decode(data["resume_docx"])
            st.download_button(
                label="📥 이력서 다운로드 (resume.docx)",
                data=resume_bytes,
                file_name="resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            log_area.error(f"❌ 오류 발생: {e}")
else:
    st.info("👆 위에 GitHub 주소를 입력하고 '분석 시작'을 눌러주세요.")