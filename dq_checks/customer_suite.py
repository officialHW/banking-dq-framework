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
def run_customer_suite(df=None):
    """
    Run all data quality checks on the customers table.
    Returns a list of results - passed and failed.
    """
    if df is None:
        df = load_table("customers")

    results = []

    # 1. Row count
    results.append(check_row_count(df, min_rows=1, max_rows=50000))

    # 2. null checks on crititcal fields
    for column in ["customer_id", "first_name", "last_name",
                   "account_type", "date_joined"]:
            results.append(check_no_nulls(df, column))

    # 3. Customer_id must be unique
    results.append(check_unique(df, "customer_id"))

    # 4. Credit score must be between 300 and 999
    results.append(check_value_range(df, "credit_score",
                                     min_value=500, max_value=999))
                                     
    # 5. Account type must be CURRENT or SAVINGS
    results.append(check_accepted_values(
         df, "account_type", ["CURRENT", "SAVINGS"]
    ))

    # 6. is-active must be 0 or 1
    results.append(check_accepted_values(df, "is_active", [0, 1]))

    return results

def run_customer_suite_strict(df=None):
    """
    Run all checks and raise immediately on first failure.
    Used by Behave step definitions.
    """
    if df is None:
        df = load_table("customers")

    results = run_customer_suite(df)
    for result in results:
        assert_check(result)
    return results