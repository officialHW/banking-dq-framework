from behave import given, when, then
from matplotlib.style import context
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
from dq_checks.transaction_suite import run_transaction_suite
from dq_checks.customer_suite import run_customer_suite

# ________GIVEN steps : load data __________________________

@given('the transactions table is loaded')
def step_load_transactions(conntext):
    context.transactions_df = load_table("transactions")
    assert len(context.transactions_df) > 0, "Transactions table is empty"

@given('the customers table is loaded')
def step_load_customers(context):
    context.customers_df = load_table("customers")
    assert len(context.customers_df) > 0, "Customers table is empty"

# ________WHEN steps : run checks __________________________

@when('Icheck the transaction_id column for nulls')
def step_check_txn_null(context):
    context.result = check_no_nulls(context.transactions_df, "transaction_id")

@when('I check the transaction_id for duplicates')
def step_check_txn_dupes(context):
    context.result = check_unique(context.transactions_df, "transaction_id")

@when('I check thew amount column for valid range between 0.01 ad 1000000')
def step_check_amount_range(context):
    context.result = check_value_range(context.transactions_df, "amount",
                                      min_value=0.01, max_value=1000000)
    
@when('I check referential integrity between transactions and customers')
def step_check_ref_integrity(context):
    context.result = check_referential_integrity(
        df_child=context.transactions_df,
        df_parent=context.customers_df,
        child_key="customer_id",
        parent_key="customer_id"
    )   

@when('I check transaction_type for accepted values')
def step_check_txn_type(context):
    context.result = check_accepted_values(
        context.transactions_df, "transaction_type", ["DEBIT", "CREDIT"]
    )

@when('I check currency for accepted values')
def step_check_currency(context):
    context.result = check_accepted_values(
        context.transactions_df, "currency", ["GBP"]
    )
@when('I run the full transaction quality suite')
def step_run_full_txn_suite(context):
    context.suite_results = run_transaction_suite(
        context.transactions_df, context.customers_df
    )

@when('I check the customer_id column for nulls')
def step_check_cust_null(context):
    context.result = check_no_nulls(context.customers_df, "customer_id")

@when('I check customer_id for duplicates')
def step_check_cust_dupes(context):
    context.result = check_unique(context.customers_df, "customer_id")

@when('I check credit_score for valid range between 500 and 999')
def step_check_credit_score(context):
    context.result = check_value_range(
        context.customers_df, "credit_score",
        min_value=500, max_value=999
    )

@when('I check account_type for accepted values')
def step_check_account_type(context):
    context.result = check_accepted_values(
        context.customers_df,
        "account_type",
        ["CURRENT", "SAVINGS"]
    )

@when('I run the full customer quality suite')
def step_run_full_cust_suite(context):
    context.suite_results = run_customer_suite(context.customers_df)

# ── THEN steps — assert outcomes ────────────────────────────────────

@then('the null check should pass')
def step_null_should_pass(context):
    assert context.result["passed"], \
        f"Expected null check to pass but got: {context.result['details']}"
    print(f"PASSED: {context.result['details']}")

@then('the duplicate check should fail because T001 appears twice')
def step_dupe_should_fail(context):
    assert not context.result["passed"], \
        "Expected duplicate check to fail — T001 should appear twice"
    print(f"CORRECTLY DETECTED: {context.result['details']}")

@then('the range check should fail because T007 has a negative amount')
def step_range_should_fail(context):
    assert not context.result["passed"], \
        "Expected range check to fail — T007 has amount -50.00"
    print(f"CORRECTLY DETECTED: {context.result['details']}")

@then('the referential integrity check should fail because C999 does not exist')
def step_ref_should_fail(context):
    assert not context.result["passed"], \
        "Expected referential integrity check to fail — C999 has no matching customer"
    print(f"CORRECTLY DETECTED: {context.result['details']}")

@then('the accepted values check should pass')
def step_accepted_should_pass(context):
    assert context.result["passed"], \
        f"Expected accepted values check to pass but got: {context.result['details']}"
    print(f"PASSED: {context.result['details']}")

@then('the currency check should pass')
def step_currency_should_pass(context):
    assert context.result["passed"], \
        f"Expected currency check to pass but got: {context.result['details']}"
    print(f"PASSED: {context.result['details']}")

@then('the suite should identify all data quality issues')
def step_suite_identifies_issues(context):
    failed = [r for r in context.suite_results if not r["passed"]]
    passed = [r for r in context.suite_results if r["passed"]]
    print(f"\n{'='*50}")
    print(f"TRANSACTION SUITE RESULTS")
    print(f"{'='*50}")
    print(f"Total checks: {len(context.suite_results)}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    print(f"\nFailed checks:")
    for r in failed:
        print(f"  FAIL: {r['check']} — {r['details']}")
    print(f"\nPassed checks:")
    for r in passed:
        print(f"  PASS: {r['check']} — {r['details']}")
    assert len(failed) > 0, \
        "Expected some checks to fail — bad data should be detected"

@then('the customer null check should pass')
def step_cust_null_pass(context):
    assert context.result["passed"], \
        f"Expected customer null check to pass: {context.result['details']}"
    print(f"PASSED: {context.result['details']}")

@then('the customer duplicate check should pass')
def step_cust_dupe_pass(context):
    assert context.result["passed"], \
        f"Expected customer duplicate check to pass: {context.result['details']}"
    print(f"PASSED: {context.result['details']}")

@then('the credit score check should fail because C005 has a score of 455')
def step_credit_score_fail(context):
    assert not context.result["passed"], \
        "Expected credit score check to fail — C005 has score 455"
    print(f"CORRECTLY DETECTED: {context.result['details']}")

@then('the account type check should pass')
def step_account_type_pass(context):
    assert context.result["passed"], \
        f"Expected account type check to pass: {context.result['details']}"
    print(f"PASSED: {context.result['details']}")

@then('the suite should identify all customer data quality issues')
def step_cust_suite_issues(context):
    failed = [r for r in context.suite_results if not r["passed"]]
    passed = [r for r in context.suite_results if r["passed"]]
    print(f"\n{'='*50}")
    print(f"CUSTOMER SUITE RESULTS")
    print(f"{'='*50}")
    print(f"Total checks: {len(context.suite_results)}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    print(f"\nFailed checks:")
    for r in failed:
        print(f"  FAIL: {r['check']} — {r['details']}")
    print(f"\nPassed checks:")
    for r in passed:
        print(f"  PASS: {r['check']} — {r['details']}")
    assert len(failed) > 0, \
        "Expected some checks to fail — bad data should be detected"