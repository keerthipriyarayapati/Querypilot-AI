from llm import llm


def classify_question(question):
    """
    Returns True if the question is related to the uploaded
    database or SQL querying, otherwise returns False.
    """

    prompt = f"""
You are a classifier.

Determine whether the user's question is related to querying the uploaded database.

Return ONLY one word:

YES
or
NO

Examples:

Question: Show total revenue
Answer: YES

Question: List all customers
Answer: YES

Question: What is the average salary?
Answer: YES

Question: Who is Virat Kohli?
Answer: NO

Question: Tell me a joke.
Answer: NO

Question: Write Python code.
Answer: NO

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content.strip().upper()

    return answer == "YES"