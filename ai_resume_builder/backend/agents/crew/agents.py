from crewai import Agent
from langchain_community.chat_models import ChatOllama

llm_summarizer = ChatOllama(model="llama3", base_url="http://localhost:11434")
llm_writer = ChatOllama(model="mistral", base_url="http://localhost:11434")

code_summarizer = Agent(
    role="Code Summarizer",
    goal="Summarize GitHub repository source code into key insights.",
    backstory="A senior software engineer with expertise in large codebases.",
    llm=llm_summarizer,
    verbose=True
)

readme_writer = Agent(
    role="README Writer",
    goal="Generate a professional and helpful README file based on the summarized code.",
    backstory="An experienced technical writer specialized in developer documentation.",
    llm=llm_writer,
    verbose=True
)