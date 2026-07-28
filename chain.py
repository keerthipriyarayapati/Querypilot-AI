from prompt_template import prompt
from llm import llm
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = prompt | llm | parser