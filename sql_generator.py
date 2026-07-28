import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from retriever import get_relevant_schema
from chain import chain
from sql_validator import validate_sql
from executor import execute_query


def process_question(question):
    """
    Generates SQL, validates it, executes it,
    and returns all the results.
    """

    schema = get_relevant_schema(question)

    sql_query = chain.invoke(
        {
            "schema": schema,
            "question": question
        }
    )

    if not validate_sql(sql_query):
        return {
            "success": False,
            "error": "Unsafe SQL detected."
        }

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

        print(output["error"])