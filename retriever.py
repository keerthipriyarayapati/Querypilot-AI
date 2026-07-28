import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from vector_store import create_vector_store


def get_relevant_schema(question, k=2):

    vector_store = create_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k
    )

    schema = ""

    for doc in results:
        schema += doc.page_content + "\n\n"

    return schema


if __name__ == "__main__":

    schema = get_relevant_schema("Show total revenue")

    print(schema)