from langchain_core.prompts import PromptTemplate


with open("prompts/sql_prompt.txt", "r") as file:
    template = file.read()

prompt = PromptTemplate.from_template(template)
