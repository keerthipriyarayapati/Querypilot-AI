import streamlit as st

from upload_handler import upload_csv_files
from sql_generator import process_question

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI SQL Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION STATE ----------------

if "uploaded_tables" not in st.session_state:
    st.session_state.uploaded_tables = []

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🤖 AI SQL Generator for Data Analysts")

    st.markdown("---")

    st.subheader("Navigation")

    st.button("🏠 Dashboard", use_container_width=True)
    st.button("📂 Upload Data", use_container_width=True)
    st.button("📜 Query History", use_container_width=True)
    st.button("⚙ Settings", use_container_width=True)

    st.markdown("---")

    st.success("Backend Connected")

# ---------------- HEADER ----------------

st.title("🤖 AI SQL Generator")

st.caption("Ask. Generate. Analyze.")

st.write(
    "Generate PostgreSQL queries from natural language using **Llama 3 + RAG + PostgreSQL**."
)

st.divider()

# ======================================================
# Upload Section
# ======================================================

st.subheader("📂 Upload Dataset")

uploaded_files = st.file_uploader(
    "Upload one or more CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if st.button("📤 Upload Files", use_container_width=True):

    if uploaded_files:

        with st.spinner("Uploading datasets and refreshing vector database..."):

            response = upload_csv_files(uploaded_files)

            if response["success"]:

                st.success("Datasets uploaded successfully!")

                st.session_state.uploaded_tables = response["tables"]

            else:

                st.error(response["message"])

    else:

        st.warning("Please choose at least one CSV file.")

st.divider()

# ======================================================
# Dashboard Layout
# ======================================================

left, right = st.columns([3,1])

# ======================================================
# LEFT PANEL
# ======================================================

with left:

    st.subheader("💬 Ask a Question")

    question = st.text_input(
        label="",
        placeholder="Example: Show total revenue..."
    )

    # Generate SQL Button
    if st.button("🚀 Generate SQL", use_container_width=True):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating SQL..."):

                response = process_question(question)

                if response["success"]:

                    # ---------------- Retrieved Schema ----------------

                    st.divider()

                    st.subheader("📚 Retrieved Schema")

                    st.code(
                        response["schema"],
                        language="text"
                    )

                    # ---------------- Generated SQL ----------------

                    st.divider()

                    st.subheader("📝 Generated SQL")

                    st.code(
                        response["sql"],
                        language="sql"
                    )

                    # ---------------- Query Results ----------------

                    st.divider()

                    st.subheader("📊 Query Results")

                    if response["result"] is not None:

                        st.dataframe(
                            response["result"],
                            use_container_width=True
                        )

                        csv = response["result"].to_csv(index=False)

                        st.download_button(
                            label="📥 Download Results",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

                    else:

                        st.warning("Query executed successfully but returned no data.")

                else:

                    st.error(response["error"])

# ======================================================
# RIGHT PANEL
# ======================================================

with right:

    st.subheader("📚 Schema Explorer")

    if st.session_state.uploaded_tables:

        for table in st.session_state.uploaded_tables:

            with st.expander(f"📄 {table}", expanded=False):

                st.write("Columns will be displayed here in the next module.")

    else:

        st.info("No datasets uploaded.")

    st.divider()

    st.subheader("📈 System Status")

    st.success("✅ PostgreSQL Connected")
    st.success("✅ ChromaDB Ready")
    st.success("✅ Llama 3 Ready")

    st.divider()

    st.subheader("ℹ Tech Stack")

    st.markdown("""
**LLM:** Llama 3

**Embeddings:** Nomic Embed Text

**Vector Database:** ChromaDB

**Relational Database:** PostgreSQL

**Framework:** Streamlit

**Language:** Python
""")
