import sqlite3
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/banking.db")

# --- TRANSACTIONS TABLE ---
# Test data is hardcoded rather than randomnised intemtionally to ensure consistency in testing outcomes.
# Reproducible test data ensures consistent results across all environments and makes failures explainable and auditable.
# Includes delibrate bad rows to prove tests framework catches failures.
transactions = pd.DataFrame({
    "transaction_id": [
        "T001", "T002", "T003", "T004", "T005", "T006", "T007", "T008", "T001", "T009" # T001 is a duplicate
    ],
    "customer_id": [ 
        "C001", "C002", "C001", "C003", "C002", "C004", "C001", "C003", "C001", "C999" # C999 does not exist in customers table
    ],
    "amount": [
        250.00, 1500.00, 75.50, 3200.00, 89.99, 450.00, -50.00, 620.00, 250.00, 1100.00 # -50.00 is invalid amount
    ],
    "transaction_date": [
        "2024-03-20", "2024-03-20","2024-03-21", "2024-03-21", "2024-03-22", "2024-03-22", "2024-03-23", "2024-03-23", "2024-03-20", "2024-03-24"
    ],
    "transaction_type": [
        "DEBIT", "CREDIT", "DEBIT", "CREDIT", "DEBIT", "CREDIT", "DEBIT", "CREDIT", "DEBIT", "CREDIT"
    ],
    "status": [
        "COMPLETED", "COMPLETED", "COMPLETED", "COMPLETED", "COMPLETED", "COMPLETED", "COMPLETED", "COMPLETED", "COMPLETED", "COMPLETED"
    ],
    "currency": [
        "GBP", "EUR", "GBP", "GBP", "GBP", "GBP", "GBP", "GBP", "GBP", "GBP"
    ]
})

transactions.to_sql("transactions", conn, if_exists="replace", index=False)
print(f"transactions table: {len(transactions)} rows loaded")

# --- CUSTOMERS TABLE ---
customers = pd.DataFrame({
    "customer_id": ["C001","C002","C003","C004","C005"],
    "first_name":  ["Henry","Sarah","Michael","Emma","David"],
    "last_name":   ["Williams","Johnson","Williams","Brown","Jones"],
    "email": [
        "henry.williams@email.com",
        "sarah.johnson@email.com",
        None,                           # deliberately null email
        "emma.brown@email.com",
        "david.jones@email.com"
    ],
    "account_type": ["CURRENT","SAVINGS","CURRENT","CURRENT","SAVINGS"],
    "credit_score": [750, 820, 690, 780, 455],  # 455 is below minimum (500)
    "date_joined":  ["2020-01-15","2019-06-22","2021-03-10","2022-08-05","2018-11-30"],
    "is_active":    [1, 1, 1, 1, 0]
})

customers.to_sql("customers", conn, if_exists="replace", index=False)
print(f"customers table: {len(customers)} rows loaded")

conn.close()
print("\nDatabase created at data/banking.db")
print("Deliberately bad data included:")
print("  - T001 is duplicated (appears twice)")
print("  - T007 has a negative amount (-50.00)")
print("  - C999 in transactions has no matching customer record")
print("  - C003 has a null email")
print("  - C005 has a credit score of 455 (below minimum 500)")
