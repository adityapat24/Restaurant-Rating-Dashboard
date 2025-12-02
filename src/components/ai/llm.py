import sqlite3
import google.generativeai as genai
import pandas as pd


# ===========================================
# 1. Load SQL file → SQLite (in-memory)
# ===========================================
def load_sql_db(sql_file: str):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    with open(sql_file, "r") as f:
        sql_script = f.read()

    cur.executescript(sql_script)
    conn.commit()
    return conn


# ===========================================
# 2. Extract schema (RAG context)
# ===========================================
def extract_schema(sql_file: str):
    with open(sql_file, "r") as f:
        lines = f.readlines()

    schema = []
    keep = False
    for line in lines:
        if line.strip().upper().startswith("CREATE TABLE"):
            keep = True
        if keep:
            schema.append(line)
        if keep and line.strip().endswith(");"):
            keep = False

    return "".join(schema)


# ===========================================
# 3. Gemini → SQL (Query Generation)
# ===========================================
def llm_generate_sql(question: str, schema: str, model):
    prompt = f"""
You are an expert in SQL and data analysis.

Given the SQL schema below, generate a SINGLE SQLite-compatible SQL query 
that answers the user's question.

--- SCHEMA ---
{schema}
--------------

Question: "{question}"

Return only the SQL. No explanation.
"""
    response = model.generate_content(prompt)
    sql = response.text.strip("`").strip()
    return sql


# ===========================================
# 4. Execute SQL → Pandas
# ===========================================
def run_sql(conn, sql_query: str):
    return pd.read_sql_query(sql_query, conn)


# ===========================================
# 5. Gemini → Final Answer (Optional reasoning on data)
# ===========================================
def llm_generate_final_answer(question: str, df: pd.DataFrame, model):
    data_str = df.to_string(index=False)

    prompt = f"""
You are a data analyst.

User question:
{question}

Here is the SQL result table:
{data_str}

Explain the answer in clear natural language.
"""

    response = model.generate_content(prompt)
    return response.text


# ===========================================
# 6. RAG Pipeline (end-to-end)
# ===========================================
def rag_answer(question: str, sql_file: str, api_key: str):
    # Init LLM
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Load SQL DB and schema
    conn = load_sql_db(sql_file)
    schema = extract_schema(sql_file)

    # Stage 1 — NL → SQL
    sql_query = llm_generate_sql(question, schema, model)
    print("\n[Generated SQL]\n", sql_query)

    # Stage 2 — Execute SQL
    df = run_sql(conn, sql_query)
    print("\n[SQL Results]\n", df)

    # Stage 3 — Structured → Final NL Answer
    answer = llm_generate_final_answer(question, df, model)
    return answer