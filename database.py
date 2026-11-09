import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def init_db(db_path="accounting_demo.db"):
    # Agregamos check_same_thread=False para evitar conflictos de hilos en Streamlit
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    # Tabla de Ventas Diarias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_sales (
            sale_id TEXT PRIMARY KEY,
            date TEXT,
            category TEXT,
            product_name TEXT,
            units INTEGER,
            unit_price REAL,
            cost_price REAL,
            tax_rate REAL
        )
    """)
    
    # Tabla de Libro Diario (Pólizas Contables)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS general_journal (
            entry_id TEXT,
            date TEXT,
            account_code TEXT,
            account_name TEXT,
            debit REAL,
            credit REAL,
            description TEXT
        )
    """)
    
    # Generar datos de ejemplo si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM daily_sales")
    if cursor.fetchone()[0] == 0:
        np.random.seed(42)
        start_date = datetime.now() - timedelta(days=180)
        categories = ["Electronics", "Office Supplies", "Hardware", "Maintenance Services"]
        products = {
            "Electronics": [("Wireless Mouse", 45.0, 20.0), ("Mechanical Keyboard", 120.0, 60.0)],
            "Office Supplies": [("Ergonomic Chair", 250.0, 110.0), ("Desk Organizer", 35.0, 12.0)],
            "Hardware": [("SSD 1TB", 95.0, 50.0), ("Monitor 27\"", 300.0, 150.0)],
            "Maintenance Services": [("Annual Tech Support", 500.0, 100.0), ("Emergency Diagnostic", 150.0, 30.0)]
        }
        
        sales_data = []
        journal_data = []
        
        for i in range(1, 1001):
            sale_id = f"SALE-{i:04d}"
            date = (start_date + timedelta(days=np.random.randint(0, 180))).strftime("%Y-%m-%d")
            category = np.random.choice(categories)
            prod_info = products[category][np.random.randint(0, len(products[category]))]
            product_name, unit_price, cost_price = prod_info[0], prod_info[1], prod_info[2]
            units = np.random.randint(1, 5)
            tax_rate = 0.16
            
            sales_data.append((sale_id, date, category, product_name, units, unit_price, cost_price, tax_rate))
            
            subtotal = units * unit_price
            tax = subtotal * tax_rate
            total = subtotal + tax
            total_cost = units * cost_price
            
            journal_data.append((f"JE-{i}-1", date, "1101", "Cash & Receivables", total, 0.0, f"Sale {sale_id}"))
            journal_data.append((f"JE-{i}-2", date, "4101", "Sales Revenue", 0.0, subtotal, f"Revenue {sale_id}"))
            journal_data.append((f"JE-{i}-3", date, "2102", "VAT Payable", 0.0, tax, f"Tax {sale_id}"))
            journal_data.append((f"JE-{i}-4", date, "5101", "Cost of Goods Sold", total_cost, 0.0, f"COGS {sale_id}"))
            journal_data.append((f"JE-{i}-5", date, "1201", "Inventory", 0.0, total_cost, f"Inventory reduction {sale_id}"))

        cursor.executemany("INSERT INTO daily_sales VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sales_data)
        cursor.executemany("INSERT INTO general_journal VALUES (?, ?, ?, ?, ?, ?, ?)", journal_data)
        conn.commit()
        
    return conn