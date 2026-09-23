import sqlite3

DB_NAME = "queryforge.db"

# ==========================================
# 1. SANDBOX DB SETUP & DUMMY DATA
# ==========================================
def setup_database(db_name: str = DB_NAME):
    """
    Creates a sandbox database with sample tables and records
    for safe testing without touching production data.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        salary REAL,
        hire_date TEXT
    );
    """)

    # Create Sales Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        amount REAL,
        region TEXT,
        sale_date TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    );
    """)

    # Insert initial records if table is empty
    cursor.execute("SELECT COUNT(*) FROM employees;")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO employees (name, department, salary, hire_date)
        VALUES (?, ?, ?, ?);
        """, [
            ("Rahul Sharma", "Engineering", 85000, "2022-01-15"),
            ("Ananya Verma", "Sales", 65000, "2023-03-10"),
            ("Aarav Patel", "Sales", 70000, "2021-11-01"),
            ("Priya Nair", "Engineering", 90000, "2020-05-20"),
            ("Vikram Singh", "HR", 55000, "2024-02-01")
        ])

        cursor.executemany("""
        INSERT INTO sales (employee_id, amount, region, sale_date)
        VALUES (?, ?, ?, ?);
        """, [
            (2, 1200.50, "North", "2026-01-10"),
            (2, 850.00, "South", "2026-01-15"),
            (3, 2300.00, "North", "2026-02-01"),
            (3, 1500.00, "West", "2026-02-18"),
            (2, 3100.00, "East", "2026-03-05")
        ])
        conn.commit()
        print("✅ Database & Sample Tables initialized successfully!")

    conn.close()


# ==========================================
# 2. DYNAMIC SCHEMA INSPECTOR
# ==========================================
def get_database_schema(db_name: str = DB_NAME) -> str:
    """
    Inspects any SQLite database dynamically and returns its 
    schema layout (Tables & Columns) as a string for LLM Context.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query sqlite_master to get all user-created tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()  # List of tuples, e.g., [('employees',), ('sales',)]

    schema_list = []

    for table_tuple in tables:
        table_name = table_tuple[0]
        
        # PRAGMA command inspects column details of a specific table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        
        # col[1] = Column Name, col[2] = Data Type
        columns_formatted = [f"{col[1]} ({col[2]})" for col in columns_info]
        table_schema = f"Table: {table_name}\nColumns: {', '.join(columns_formatted)}"
        schema_list.append(table_schema)

    conn.close()
    return "\n\n".join(schema_list)


# ==========================================
# 3. QUERY EXECUTION ENGINE
# ==========================================
def execute_query(query: str, db_name: str = DB_NAME) -> dict:
    """
    Executes a SQL query. 
    Returns data on success, or captures raw SQL exception error string on failure.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        
        # Check if query returns data (SELECT) or modifies DB (INSERT/UPDATE)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            conn.close()
            return {"success": True, "columns": columns, "data": rows, "error": None}
        else:
            conn.commit()
            conn.close()
            return {"success": True, "columns": [], "data": "Query executed successfully", "error": None}

    except sqlite3.Error as e:
        conn.close()
        # Exception string return karenge taaki Self-Healing agent is error ko padh kar SQL auto-fix kare
        return {"success": False, "columns": [], "data": None, "error": str(e)}


# ==========================================
# TEST BLOCK
# ==========================================
if __name__ == "__main__":
    setup_database()
    
    print("\n🔍 --- EXTRACTED DB SCHEMA ---")
    print(get_database_schema())

    print("\n🧪 --- TEST QUERY EXECUTION ---")
    test_result = execute_query("SELECT name, department, salary FROM employees WHERE salary > 70000;")
    print("Success:", test_result["success"])
    print("Columns:", test_result["columns"])
    print("Data:", test_result["data"])