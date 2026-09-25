import sqlite3

def setup_database(db_name="queryforge.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        hire_date TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        amount REAL NOT NULL,
        region TEXT NOT NULL,
        sale_date TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM employees;")
    if cursor.fetchone()[0] == 0:
        employees_data = [
            ("Rahul Sharma", "Engineering", 85000.0, "2022-01-15"),
            ("Priya Nair", "Engineering", 90000.0, "2021-06-20"),
            ("Amit Verma", "Sales", 60000.0, "2023-03-10"),
            ("Neha Gupta", "Marketing", 65000.0, "2022-11-01"),
            ("Siddharth Rao", "Sales", 72000.0, "2020-08-05")
        ]
        cursor.executemany("""
        INSERT INTO employees (name, department, salary, hire_date)
        VALUES (?, ?, ?, ?);
        """, employees_data)

        sales_data = [
            (3, 15000.0, "North", "2023-04-01"),
            (5, 22000.0, "South", "2023-04-03"),
            (3, 18000.0, "North", "2023-04-10"),
            (5, 30000.0, "West", "2023-04-12")
        ]
        cursor.executemany("""
        INSERT INTO sales (employee_id, amount, region, sale_date)
        VALUES (?, ?, ?, ?);
        """, sales_data)

        conn.commit()

    conn.close()


def get_database_schema(db_name="queryforge.db") -> str:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    schema_str = ""
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        col_desc = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        schema_str += f"Table: {table}\nColumns: {col_desc}\n\n"

    conn.close()
    return schema_str.strip()


def execute_query(query: str, db_name="queryforge.db") -> dict:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            conn.close()
            return {"success": True, "columns": columns, "data": data, "error": None}
        else:
            conn.commit()
            conn.close()
            return {"success": True, "columns": [], "data": [], "error": None}
    except sqlite3.Error as e:
        conn.close()
        return {"success": False, "columns": [], "data": [], "error": str(e)}


if __name__ == "__main__":
    setup_database()
    print("Database Initialized.")
    print("\n--- SCHEMA ---")
    print(get_database_schema())
    print("\n--- TEST EXECUTION ---")
    res = execute_query("SELECT name, department, salary FROM employees WHERE salary > 70000;")
    print("Success:", res["success"])
    print("Columns:", res["columns"])
    print("Data:", res["data"])