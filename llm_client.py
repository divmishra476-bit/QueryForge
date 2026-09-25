import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

all_models = [m.id for m in client.models.list().data]
MODEL_NAME = all_models[0] if all_models else "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
You are QueryForge, an expert Text-to-SQL AI engine.
Your sole task is to convert user natural language questions into valid, highly efficient SQLite SQL queries using the provided Database Schema.

STRICT RULES:
1. Return ONLY the executable SQL query.
2. Do NOT wrap the query in markdown code blocks like ```sql ... ```.
3. Do NOT include any explanations, greetings, or conversation text.
4. Always construct safe, READ-ONLY (SELECT) queries.
"""

def generate_sql(user_question: str, schema: str) -> str:
    user_prompt = f"""
DATABASE SCHEMA:
{schema}

USER QUESTION:
{user_question}

Generate SQL Query:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0
    )

    sql_query = response.choices[0].message.content.strip()

    if sql_query.startswith("```"):
        lines = sql_query.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        sql_query = "\n".join(lines).strip()

    return sql_query


if __name__ == "__main__":
    print(f"Connected to Groq using model: {MODEL_NAME}\n")
    test_schema = "Table: employees\nColumns: id (INTEGER), name (TEXT), salary (REAL), department (TEXT)"
    test_question = "Engineering department ke saare bandon ki salary dikhao"

    print("🤖 --- TESTING LLM CLIENT (GROQ) --- \n")
    try:
        sql_result = generate_sql(test_question, test_schema)
        print("Generated SQL Query:")
        print(sql_result)
    except Exception as e:
        print("❌ Error:", e)