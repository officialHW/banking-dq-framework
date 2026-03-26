import os

# Database configuration
DB_PATH = os.getenv("DB_PATH", "data/banking.db")

# GCP configuration (for production BigQuery connection)
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
GCP_DATASET = os.getenv("GCP_DATASET", "raw_data")

# Table names
TRANSACTIONS_TABLE = "transactions"
CUSTOMERS_TABLE = "customers"

# Expectation suite names
TRANSACTIONS_SUITE = "transactions_suite"
CUSTOMERS_SUITE = "customers_suite"

# Checkpoint names
TRANSACTIONS_CHECKPOINT = "transactions_checkpoint"
CUSTOMERS_CHECKPOINT = "customers_checkpoint"

# Row count thresholds
TRANSACTIONS_MIN_ROWS = 1
TRANSACTIONS_MAX_ROWS = 100000
CUSTOMERS_MIN_ROWS = 1
CUSTOMERS_MAX_ROWS = 50000

# Valid ranges
AMOUNT_MIN = 0.01
AMOUNT_MAX = 1000000
CREDIT_SCORE_MIN = 500
CREDIT_SCORE_MAX = 999

# Accepted values
VALID_TRANSACTION_TYPES = ["DEBIT", "CREDIT"]
VALID_STATUSES = ["COMPLETED", "PENDING", "FAILED", "CANCELLED"]
VALID_CURRENCIES = ["GBP"]
VALID_ACCOUNT_TYPES = ["CURRENT", "SAVINGS"]