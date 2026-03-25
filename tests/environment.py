import sys
import os

# Make sure Python can find our dq_checks module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def before_all(context):
    """Runs once before all tests."""
    print("\n" + "="*60)
    print("BANKING DATA QUALITY FRAMEWORK")
    print("PEC Platform - Lloyds Banking Group")
    print("="*60)
    context.db_path = "data/banking.db"

def before_scenario(context, scenario):
    """Runs before each scxenario."""
    print(f"\n--- Running: {scenario.name} ---")

def after_scenario(context, scenario):
    """Runs after each scenario."""
    if scenario.status == "failed":
        print(f"FAILED: {scenario.name}")
    else:
        print(f"PASSED: {scenario.name}")

def after_all(context):
    """Runs once after all tests."""
    print("\n" + "="*60)
    print("ALL SCENARIOS COMPLETE")
    print("="*60)