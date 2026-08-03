import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from retriever import get_relevant_schema
from chain import chain
from sql_validator import validate_sql
from executor import execute_query
from question_classifier import classify_question


def process_question(question):

    if not classify_question(question):
        return {
        "success": False,
        "error": "❌ This application only supports questions related to the uploaded database."
        }
    """
    Generates SQL, validates it,
    executes it, and returns the result.
    """

    # ----------------------------------------
    # Retrieve Relevant Schema
    # ----------------------------------------

    retrieved = get_relevant_schema(question)

    if not retrieved["success"]:

        return {
            "success": False,
            "error": "❌ This question is not related to the uploaded database."
        }

    schema = retrieved["schema"]

    # ----------------------------------------
    # Generate SQL
    # ----------------------------------------

    sql_query = chain.invoke(
        {
            "schema": schema,
            "question": question
        }
    )

    # ----------------------------------------
    # Validate SQL
    # ----------------------------------------

    if not validate_sql(sql_query):

        return {
            "success": False,
            "error": "Unsafe SQL detected."
        }

    # ----------------------------------------
    # Execute SQL
    # ----------------------------------------

    result = execute_query(sql_query)

    return {
        "success": True,
        "schema": schema,
        "sql": sql_query,
        "result": result
    }


if __name__ == "__main__":

    question = input("Ask your question: ")

    output = process_question(question)

    if output["success"]:

        print("\nRetrieved Schema:\n")
        print(output["schema"])

        print("\nGenerated SQL:\n")
        print(output["sql"])

        print("\nQuery Result:\n")
        print(output["result"])

    else:

        print("\n" + output["error"])