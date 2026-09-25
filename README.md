# ⚡ QueryForge: Production-Grade Text-to-SQL AI Agent

QueryForge is an intelligent, modular, and security-first Text-to-SQL AI engine designed to translate natural language questions into executable SQLite SQL queries. Powered by **Groq (Llama-3)** models, it incorporates AST/Regex-based **Security Guardrails** and an autonomous **Self-Healing Loop** to handle database runtime errors gracefully.

---

## 🏗️ Architecture & Data Flow

+------------------+      +-------------------+      +--------------------+
|  User Question   | ---> |   LLM Client      | ---> |  Security Guard    |
|   (CLI / Input)  |      | (Groq API Llama3) |      | (Read-Only Safety) |
+------------------+      +-------------------+      +--------------------+
|
v
+------------------+      +-------------------+      +--------------------+
| Output Results / | <--- | SQLite Execution  | <--- | SQL Query Check    |
| Terminal Display |      |      Sandbox      |      |   (Pass / Fail)    |
+------------------+      +-------------------+      +--------------------+
|
(If Execution Error)
|
v
+-------------------+
| Self-Healing Loop | (Feedback Error to LLM)
+-------------------+


---

## ✨ Key Features

- **Modular Engine Architecture**: Strict separation of concerns across dedicated modules (`database.py`, `security.py`, `llm_client.py`, `main.py`).
- **Dynamic Model Selection**: Auto-filters active chat endpoints via the Groq API to prevent model deprecation issues and handle model access dynamically.
- **Security Guardrails**: AST and Regex-based SQL validation enforcing strict read-only (`SELECT`) queries while blocking dangerous DDL/DML operations (`DROP`, `DELETE`, `UPDATE`, `INSERT`, multi-statement execution).
- **Self-Healing Feedback Loop**: Intercepts database runtime execution errors and feeds error traces back into the LLM context for automated, real-time query repair.
- **Deterministic Code Generation**: Enforces zero-temperature prompting with markdown-stripping parsers to deliver pure SQL queries without conversational boilerplate.

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **LLM Provider**: Groq API (Llama-3 Models)
- **Database Engine**: SQLite3
- **Configuration & Security**: `python-dotenv`

---

## 🚀 Getting Started

### 1. Prerequisites & Installation

Clone the repository and set up a virtual environment:

```bash
git clone [https://github.com/YOUR_USERNAME/QueryForge.git](https://github.com/YOUR_USERNAME/QueryForge.git)
cd QueryForge

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
2. Environment Setup
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_actual_groq_api_key_here
(Refer to .env.example for reference. Never commit .env to Git).

3. Execution
Run the main orchestrator script:

Bash
python main.py
📂 Project Structure
Plaintext
QueryForge/
├── .env.example          # Environment variable template
├── .gitignore             # Ignore rules for secrets & DB artifacts
├── database.py            # SQLite sandbox setup, schema reading, & execution
├── security.py            # AST & regex-based read-only security guardrails
├── llm_client.py          # Groq API client with dynamic model filtering
├── main.py                # Main orchestrator & self-healing execution loop
└── requirements.txt       # Project dependencies

💼 Resume Description Points
QueryForge (Text-to-SQL AI Agent): Engineered an autonomous Text-to-SQL agent leveraging Groq Llama-3 LLMs and SQLite, converting natural language queries into optimized SQL statements.

Implemented AST Security Guardrails: Built a deterministic SQL validation engine using AST and regex parsing to block malicious or destructive database operations (DROP, DELETE, multi-statement execution).

Architected Self-Healing Loop: Developed an iterative feedback mechanism that captures database runtime errors and re-prompts the LLM with exception traces, automatically resolving syntax and schema mismatch issues.

Modular Design: Structured code base adhering to production standards with strict secret separation (.env), dynamic model selection, and zero-temperature query formatting
