import re

# Bouncer ki Blacklist (Destructive Commands)
FORBIDDEN_PATTERNS = [
    r"\bDROP\b",
    r"\bDELETE\b",
    r"\bUPDATE\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bINSERT\b"
]

def validate_sql_query(query: str) -> dict:
    """
    Checks if the SQL query is safe to run.
    Only allows READ-ONLY (SELECT) operations.
    """
    clean_query = query.strip()
    
    # Check 1: Kya query SELECT se shuru ho rahi hai?
    if not (clean_query.upper().startswith("SELECT") or clean_query.upper().startswith("WITH")):
        return {
            "is_safe": False,
            "reason": "Security Alert: Only SELECT (Read-Only) queries are allowed!"
        }

    # Check 2: Kya query mein koi Blacklisted word (DROP, DELETE etc.) hai?
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, clean_query, re.IGNORECASE):
            keyword = pattern.replace(r"\b", "")
            return {
                "is_safe": False,
                "reason": f"Security Alert: Hazardous command '{keyword}' detected!"
            }

    # Check 3: Semicolon Check (Ek saath 2 queries ko block karna)
    statements = [stmt.strip() for stmt in clean_query.split(";") if stmt.strip()]
    if len(statements) > 1:
        return {
            "is_safe": False,
            "reason": "Security Alert: Running multiple SQL statements at once is blocked."
        }

    return {"is_safe": True, "reason": "Query is safe."}


# ==========================================
# TESTING THE BOUNCER
# ==========================================
if __name__ == "__main__":
    print("🛡️ --- TESTING SECURITY GUARDRAILS ---\n")
    
    # Test 1: Sahi Query (Dukaan se sirf samaan maang raha hai)
    q1 = "SELECT name, salary FROM employees WHERE salary > 70000;"
    print("Test 1:", validate_sql_query(q1))

    # Test 2: Galat Query (Dukaan todne ki koshish)
    q2 = "DROP TABLE employees;"
    print("Test 2:", validate_sql_query(q2))

    # Test 3: Chalaki (Pehle SELECT kiya, phir DELETE chipka diya)
    q3 = "SELECT * FROM sales; DELETE FROM sales;"
    print("Test 3:", validate_sql_query(q3))