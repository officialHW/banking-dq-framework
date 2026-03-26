import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dq_checks.transaction_suite import run_transaction_suite
from dq_checks.customer_suite import run_customer_suite
from dq_checks.base_expectations import load_table


def run_all_checkpoints():
    """
    Run all data quality checkpoints across all tables.
    Prints a full summary of passed and failed checks.
    Returns True if all checks passed, False if any failed.
    """
    print("\n" + "="*60)
    print("RUNNING ALL DATA QUALITY CHECKPOINTS")
    print("="*60)

    all_passed = True

    # --- Transactions checkpoint ---
    print("\n[1/2] Running transactions checkpoint...")
    transactions_df = load_table("transactions")
    customers_df = load_table("customers")
    txn_results = run_transaction_suite(transactions_df, customers_df)

    txn_failed = [r for r in txn_results if not r["passed"]]
    txn_passed = [r for r in txn_results if r["passed"]]

    print(f"Transactions: {len(txn_passed)} passed, {len(txn_failed)} failed")
    for r in txn_failed:
        print(f"  FAIL: {r['check']} — {r['details']}")
    for r in txn_passed:
        print(f"  PASS: {r['check']} — {r['details']}")

    if txn_failed:
        all_passed = False

    # --- Customers checkpoint ---
    print("\n[2/2] Running customers checkpoint...")
    customers_df = load_table("customers")
    cust_results = run_customer_suite(customers_df)

    cust_failed = [r for r in cust_results if not r["passed"]]
    cust_passed = [r for r in cust_results if r["passed"]]

    print(f"Customers: {len(cust_passed)} passed, {len(cust_failed)} failed")
    for r in cust_failed:
        print(f"  FAIL: {r['check']} — {r['details']}")
    for r in cust_passed:
        print(f"  PASS: {r['check']} — {r['details']}")

    if cust_failed:
        all_passed = False

    # --- Summary ---
    print("\n" + "="*60)
    print("CHECKPOINT SUMMARY")
    print("="*60)
    total_checks = len(txn_results) + len(cust_results)
    total_failed = len(txn_failed) + len(cust_failed)
    total_passed = len(txn_passed) + len(cust_passed)
    print(f"Total checks run: {total_checks}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")

    if all_passed:
        print("\nSTATUS: ALL CHECKS PASSED")
    else:
        print(f"\nSTATUS: {total_failed} CHECKS FAILED — review details above")

    return all_passed


if __name__ == "__main__":
    success = run_all_checkpoints()
    sys.exit(0 if success else 1)