Feature: Transaction data quality
  As a data quality engineer on the PEC platform
  I want to ensure all transaction data meets quality standards
  So that customer personalisation is based on accurate data

  Scenario: Transaction IDs must not be null
    Given the transactions table is loaded
    And the customers table is loaded
    When I check the transaction_id column for nulls
    Then the null check should pass

  Scenario: Transaction IDs must be unique
    Given the transactions table is loaded
    And the customers table is loaded
    When I check transaction_id for duplicates
    Then the duplicate check should fail because T001 appears twice

  Scenario: Transaction amounts must be within valid range
    Given the transactions table is loaded
    And the customers table is loaded
    When I check the amount column for valid range between 0.01 and 1000000
    Then the range check should fail because T007 has a negative amount

  Scenario: Every transaction must link to a valid customer
    Given the transactions table is loaded
    And the customers table is loaded
    When I check referential integrity between transactions and customers
    Then the referential integrity check should fail because C999 does not exist

  Scenario: Transaction type must be DEBIT or CREDIT
    Given the transactions table is loaded
    And the customers table is loaded
    When I check transaction_type for accepted values
    Then the accepted values check should pass

  Scenario: Currency must be GBP or EUR
    Given the transactions table is loaded
    And the customers table is loaded
    When I check currency for accepted values
    Then the currency check should pass

  Scenario: Full transaction suite runs all checks and reports results
    Given the transactions table is loaded
    And the customers table is loaded
    When I run the full transaction quality suite
    Then the suite should identify all data quality issues
