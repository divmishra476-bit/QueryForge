import re

FORBIDDEN_PATTERNS = [
    r"\bDROP\b",
    r"\bDELETE\b",
    r"\bUPDATE\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bINSERT\b",
    r"\bGRANT\b",
    r"\bREVOKE\b"
]

def validate_sql_query(query: str) -> dict:
    clean_query = query.strip()
    
    if not (clean_query.upper().startswith("SELECT") or clean_query.upper().startswith("WITH")):
        return {
            "is_safe": False,
            "reason": "Security Alert: Only SELECT (Read-Only) queries are allowed!"
        }

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, clean_query, re.IGNORECASE):
            keyword = pattern.replace(r"\b", "")
            return {
                "is_safe": False,
                "reason": f"Security Alert: Hazardous command '{keyword}' detected!"
            }

    statements = [stmt.strip() for stmt in clean_query.split(";") if stmt.strip()]
    if len(statements) > 1:
        return {
            "is_safe": False,
            "reason": "Security Alert: Running multiple SQL statements at once is blocked."
        }

    return {"is_safe": True, "reason": "Query is safe."}


if __name__ == "__main__":
    q1 = "SELECT name, salary FROM employees WHERE salary > 70000;"
    q2 = "DROP TABLE employees;"
    q3 = "SELECT * FROM sales; DELETE FROM sales;"

    print(validate_sql_query(q1))
    print(validate_sql_query(q2))
    print(validate_sql_query(q3))