import database
import security
import llm_client

def run_agent(user_question: str, max_retries: int = 2) -> None:
    database.setup_database()
    schema = database.get_database_schema()

    print(f"\n❓ User Question: {user_question}")
    
    current_question = user_question
    sql_query = llm_client.generate_sql(current_question, schema)
    print(f"\n🤖 Generated SQL:\n{sql_query}")

    for attempt in range(max_retries + 1):
        security_check = security.validate_sql_query(sql_query)
        if not security_check["is_safe"]:
            print(f"\n🛡️ {security_check['reason']}")
            return

        db_response = database.execute_query(sql_query)
        
        if db_response["success"]:
            print("\n✅ Execution Successful!")
            print(f"Columns: {db_response['columns']}")
            print("Results:")
            if db_response["data"]:
                for row in db_response["data"]:
                    print(row)
            else:
                print("  ⚠️ (No matching records found in database)")
            return
        
        error_message = db_response["error"]
        print(f"\n⚠️ Execution Failed (Attempt {attempt + 1}): {error_message}")
        
        if attempt < max_retries:
            print("🔄 Self-Healing Loop Triggered: Sending error back to LLM...")
            current_question = f"""
The generated SQL query failed on the database.

Failed SQL Query:
{sql_query}

Database Error Message:
{error_message}

Original Request:
{user_question}

Please correct the SQL query based on the schema and error message.
"""
            sql_query = llm_client.generate_sql(current_question, schema)
            print(f"\n🔧 Corrected SQL:\n{sql_query}")

    print("\n❌ Self-healing failed to resolve the issue after maximum attempts.")


if __name__ == "__main__":
    user_prompt = "Engineering department ke un bandon ke naam aur salary dikhao jinki salary 80000 se upar hai"
    run_agent(user_prompt)