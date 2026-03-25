Feature: Customer data quality
    As a data quality engineer on the PEC platform
    I want to ensure all customer data meets quality standards
    So that personalised communications reach the right customers

    Background:
        Given the customers table is loaded

    Scenario: Customer IDs must not be null
        When I check the customer_id column for nulls
        Then the customer null check should pass

    Scenario: Customer IDs must be unique
        When I check customer_id for duplicates
        Then the customer duplicate check should pass

    Scenario: Account type must be CURRENT or SAVINGS
        When I check account_type for accepted values
        Then the account type check should pass

    Scenario: Full customer suite runs all checxks and reports results
        When I run the full customer quality suite
        Then the suite should identify all customer data quality issues