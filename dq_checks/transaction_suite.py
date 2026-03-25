from dq_checks.base_expectations import (
    load_table,
    check_no_nulls,
    check_unique,
    check_value_range,
    check_referential_integrity,
    check_row_count,
    check_accepted_values,
    assert_check
)

def run_transaction_suite(df=None, customers_df=None):
    """
    Run all data quality checks on the transactions table.
    Returns a list of results, passed and failed.
    """
    if df is None:
        df = load_table("transactions")
    if customers_df is None:
        customers_df = load_table("customers")

    results = []

    # 1. Row count:must have between 1 ad 100000 rows
    results.append(check_row_count(df, min_rows=1, max_rows=100000))

    # 2. Null checks on critical fields
    for column in ["transaction_id", "customer_id", "amount",
                  "transaction_date", "trasaction_type", "status"]:
        results.append(check_no_nulls(df, column))

    # 3. Uniqueness: transaction_id must be unique
    results.append(check_unique(df, "transaction_id"))

    # 4. Amount must be between 0.01 and 1,000,000
    results.append(check_value_range(df, "amount",
                                    min_value=0.01, max_value=1000000))
    
    # 5. Referential integrity: every customer_id must exist in the customers table
    results.append(check_referential_integrity(
        df_child=df,
        df_parent=customers_df,
        child_key="customer_id",
        parent_key="customer_id"
    ))

    # 6. Transaction type must be DEBIT or CREDIT
    results.append(check_accepted_values(
        df, "transaction_type", ["DEBIT", "CREDIT"]
    ))

    # 7. Status must be from accepted values
    results.append(check_accepted_values(
        df, "status",
        ["COMPLETED", "PENDIONG", "FAILED", "CANCELLED"]
    ))

    # 8. Currency must be GBP
    results.append(check_accepted_values(df, "currency", ["GBP"]))

    return results

def run_transaction_suit_strict(df=None, customers_df=None):
    """
    Run all checks and alert immediatley on first failure.
    Used by Behave step definitions.
    """
    if df is None:
        df = load_table("transactions")
    if customers_df is None:
        customers_df = load_table("customers")

    results = run_transaction_suite(df, customers_df)
    for result in results:
        assert_check(result)
    return results