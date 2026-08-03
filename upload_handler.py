import pandas as pd

from database import engine
from vector_store import refresh_vector_store


def upload_csv_files(uploaded_files):

    uploaded_tables = []

    try:

        for uploaded_file in uploaded_files:

            df = pd.read_csv(uploaded_file)

            df.columns = df.columns.str.lower()

            table_name = uploaded_file.name.replace(".csv", "").lower()

            df.to_sql(
                table_name,
                engine,
                if_exists="replace",
                index=False
            )

            uploaded_tables.append(table_name)

        refresh_vector_store()

        return {
            "success": True,
            "tables": uploaded_tables,
            "message": "Upload Successful"
        }

    except Exception as e:

        return {
            "success": False,
            "tables": [],
            "message": str(e)
        }