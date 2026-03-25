import sqlite3
import pandas as pd

def load_table(table_name:str, db_path: str = "data/banking.db") -> pd.DataFrame:
    """Load a table from SQLite into a pandas dataframe."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    print(f"Loaded {len(df)} rows from {table_name}")
    return df

def check_no_nulls(df:pd.DataFrame, column: str) -> dict:
    """Check that a column has no (null values."""
    null_count = df[column].isnull().sum()
    passed = null_count == 0
    return {
        "check": f"no_nulls_{column}",
        "passed": passed,
        "details": f"{null_count} null values found in {column}"
    }

def check_unique(df: pd.DataFrame, column: str) -> dict:
    """Check that a column has no duploicate values."""
    duplicate_count = df[column].duplicated().sum()
    passed = duplicate_count == 0
    return {
        "check": f"unique_{column}",
        "passed": passed,
        "details": f"{duplicate_count} duplicate values found in {column}"
    }

def check_value_range(df: pd.DataFrame, column: str,
                      min_value: float, max_value: float) -> dict:
    """Check that all values in a column fall within a valid range."""
    invalid = df[(df[column] < min_value) | (df[column] > max_value)]
    passed = len(invalid) == 0
    return {
        "check": f"range_{column}",
        "passed": passed,
        "details": f"{len(invalid)} values outside range [{min_value}, {max_value}]"
    }

def check_referential_integrity(df_child: pd.DataFrame,
                                df_parent: pd.DataFrame,
                                child_key: str,
                                parent_key: str) -> dict:
    """Check every key in child table exists in parent table."""
    valid_keys = set(df_parent[parent_key])
    orphaned = df_child[~df_child[child_key].isin(valid_keys)]
    passed = len(orphaned) == 0
    return {
        "check": f"referential_integrity_{child_key}",
        "passed": passed,
        "details": f"{len(orphaned)} orphaned records - {child_key} not found in parent"
    }

def check_accepted_values(df: pd.DataFrame,
                          column: str, accepted: list) -> dict:
    """Check that all values in a column are from an accepted list."""
    invalid = df[~df[column].isin(accepted)]
    passed = len(invalid) == 0
    return {
        "check": f"accepted_values_{column}",
        "passed": passed,
        "details": f"{len(invalid)} values not in accepted list {accepted}"
    }

def assert_check(result:dict) -> None:
    """Assert a check passed - raises AssertionError with details if not."""
    if not result["passed"]:
        raise AssertionError(
            f"FAILED: {result['check']} - {result['details']}"
        )
    print(f"PASSED: {result['check']} - {result['details']}")