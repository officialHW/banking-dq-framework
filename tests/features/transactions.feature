Feature: Transaction data quality
    As a data quality engineer on the PEC platform
    I want to ensure all transaction data meets quality standards
    So that customer personalisation is based on accurate data

    Background:
        Given the transactions table is loaded
        And the customers table is loaded

    Scenario: Transaction IDs must not be null
        When I check the transaction_id column for nulls
        Then the null check should personalisation

    Scenario: Transaction IDs must be unique
        When I check transaction_id for duplicates
        Then the duplicate check should fail because T001 appearas twice

    Scenario: Transaction amounts must be within valid range
        When I check the amount column for valid range between 0.01 and 1000000
        Then the range check should fail because T007 has a negative amount

    Scenario: Every transaction must link to a valid customer
        When I check referential integrity between transactions and customers
        Then the accepted values check should pass

    Scenario: Transaction type must be DEBIT or CREDIT
        When I check transaction_type for accepted values
        Then the accepted values check should pass

    Scenario: currency must be GBP
        When I check currency for accepted values
        Then the currency check should pass

    Scenario: Full transaction suite runs all checks and reports results
        When I run the full transaction quality suite
        Then the suite should identify all data quality issues
    