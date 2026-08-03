import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from vector_store import create_vector_store


def get_relevant_schema(question, k=2):
    """
    Retrieves the most relevant schema for the user's question.
    Also returns whether the retrieved schema is relevant.
    """

    vector_store = create_vector_store()

    # Retrieve documents along with similarity scores
    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

    if not results:
        return {
            "success": False,
            "schema": ""
        }

    schema = ""

    relevance_found = False

    for doc, score in results:

        schema += doc.page_content + "\n\n"

        # Lower score = more similar
        if score < 1.0:
            relevance_found = True

    return {
        "success": relevance_found,
        "schema": schema
    }


if __name__ == "__main__":

    result = get_relevant_schema("Show total revenue")

    print(result)