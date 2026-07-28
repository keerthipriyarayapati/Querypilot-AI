import re

from langchain_core.documents import Document
from schema_extractor import get_database_schema

def create_documents():
    schema = get_database_schema()

    tables = re.split(r'(?=Table:)', schema)

    tables = [table.strip() for table in tables if table.strip()]

    documents = []

    for table in tables:

        first_line = table.split("\n")[0]
        table_name = first_line.replace("Table:", "").strip()

        doc = Document(
            page_content=table,
            metadata={
                "table_name": table_name,
                "source": "postgresql"
            }
        )

        documents.append(doc)

    return documents

if __name__ == "__main__":

    documents = create_documents()

    print(f"\nTotal Documents Created: {len(documents)}\n")

    for i, doc in enumerate(documents, start=1):

        print("=" * 60)
        print(f"Document {i}")
        print("=" * 60)

        print("Metadata:")
        print(doc.metadata)

        print("\nPage Content:")
        print(doc.page_content)

        print()