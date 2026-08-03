import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import os
import shutil
import gc

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from document_creator import create_documents

PERSIST_DIRECTORY = "./chroma_db"


def get_embeddings():
    """
    Load embedding model.
    """
    return OllamaEmbeddings(
        model="nomic-embed-text"
    )


def create_vector_store():
    """
    Creates a new vector store if it doesn't exist,
    otherwise loads the existing one.
    """

    embeddings = get_embeddings()

    if os.path.exists(PERSIST_DIRECTORY):

        print("Loading existing vector store...")

        vector_store = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings
        )

    else:

        print("Creating new vector store...")

        documents = create_documents()

        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )

        print("Vector store created successfully!")

    return vector_store


def refresh_vector_store():
    """
    Refreshes the vector store whenever
    database schema changes.
    """

    if os.path.exists(PERSIST_DIRECTORY):

        # Force Python to release references
        gc.collect()

        try:
            shutil.rmtree(PERSIST_DIRECTORY)

            print("Old vector store deleted.")

        except PermissionError:

            print("Vector store currently in use.")
            print("Please restart the application and try again.")
            return None

    vector_store = create_vector_store()

    print("Vector store refreshed successfully!")

    return vector_store


if __name__ == "__main__":

    create_vector_store()