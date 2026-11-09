Markdown
# 📊 AI-Powered Corporate Accounting & Financial Intelligence Agent

An end-to-end automated corporate accounting system and financial intelligence hub designed for SMEs. It bridges traditional double-entry bookkeeping with modern AI agents, automated financial statement generation, advanced leverage metrics, and a local natural language financial analyst powered by **Ollama (Qwen)**.

---

## 🚀 Key Features

- **Automated Double-Entry Accounting Engine:** Automatically translates daily sales transactions into balanced general journal entries (Revenue, COGS, VAT, Inventory, and Receivables).
- **Comprehensive Financial Statements:** Real-time generation of Income Statements, balance summaries, and audit trails.
- **Corporate & Financial Leverage Metrics:** Computes key performance indicators including **GAO** (Operating Leverage), **GAF** (Financial Leverage), **GAT** (Total Leverage), **ROA**, **ROE**, and net margins.
- **Local AI Financial Analyst:** Integrates with local LLMs via Ollama (`Qwen`) to allow conversational data querying (e.g., *"Which product generated the highest revenue?"*, *"Explain our financial leverage status"*).
- **Smart Streamlit Dashboard:** Interactive filtering by date range and product categories, dynamic charts, audit checks, and a dedicated print-friendly view.
- **SME-Ready & Reproducible:** Easily adaptable to custom databases and production environments.

---

## 🛠️ Project Architecture

```text
ai-accounting-agent/
├── data/                 # Sample datasets or custom database files
├── app.py                # Main Streamlit intelligent dashboard & UI
├── database.py           # SQLite initialization & double-entry automation
├── engine.py             # Accounting engine & financial indicator formulas
├── agent.py              # Ollama/Qwen local AI integration layer
├── requirements.txt      # Python dependencies
├── .gitignore            # Excluded temporary files and local DBs
└── README.md             # Project documentation
⚙️ Prerequisites & Requirements
Python 3.10+ installed on your system.
```

Ollama installed and running locally with a Qwen model pulled:

Bash
ollama pull qwen:7b  # or qwen2.5:7b
ollama serve
📦 Installation & Local Setup
Clone the repository:

Bash
git clone [https://github.com/YOUR_USERNAME/ai-accounting-agent.git](https://github.com/YOUR_USERNAME/ai-accounting-agent.git)
cd ai-accounting-agent
Install dependencies:

Python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Run the Streamlit Dashboard:

Bash
python -m streamlit run app.py
Open your browser at http://localhost:8501.

🔌 Customizing for Client Databases (SME Adaptation)
To connect this system to an existing SME database, modify database.py to point to your target database (PostgreSQL, MySQL, or a custom SQLite file) and map your transactional schemas to match the daily_sales table structure:

Python
# Example schema expectation for daily transactions
{
    "sale_id": "STR",
    "date": "YYYY-MM-DD",
    "category": "STR",
    "product_name": "STR",
    "units": "INT",
    "unit_price": "FLOAT",
    "cost_price": "FLOAT",
    "tax_rate": "FLOAT"
}
🛡️ License
This project is licensed under the MIT License - see the LICENSE file for details.


---

<ElicitationsGroup message="Para seguir mejorando o documentando tu proyecto en GitHub:">
  <Elicitation label="Agregar un diagrama de arquitectura Mermaid al README" query="Muéstrame cómo agregar un diagrama de arquitectura Mermaid profesional en el README.md para ilustrar el flujo multi-agente y contable."/>
  <Elicitation label="Configurar GitHub Actions para pruebas automáticas y CI/CD" query="Cómo configurar un pipeline de GitHub Actions para ejecutar pruebas unitarias y verificar el linter automáticamente en cada commit."/>
</ElicitationsGroup>
