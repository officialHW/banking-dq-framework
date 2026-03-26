Feature: Customer data quality
  As a data quality engineer on the PEC platform
  I want to ensure all customer data meets quality standards
  So that personalised communications reach the right customers

  Scenario: Customer IDs must not be null
    Given the customers table is loaded
    When I check the customer_id column for nulls
    Then the customer null check should pass

  Scenario: Customer IDs must be unique
    Given the customers table is loaded
    When I check customer_id for duplicates
    Then the customer duplicate check should pass

  Scenario: Credit scores must be within valid range
    Given the customers table is loaded
    When I check credit_score for valid range between 500 and 999
    Then the credit score check should fail because C005 has a score of 455

  Scenario: Account type must be CURRENT or SAVINGS
    Given the customers table is loaded
    When I check account_type for accepted values
    Then the account type check should pass

  Scenario: Full customer suite runs all checks and reports results
    Given the customers table is loaded
    When I run the full customer quality suite
    Then the suite should identify all customer data quality issues