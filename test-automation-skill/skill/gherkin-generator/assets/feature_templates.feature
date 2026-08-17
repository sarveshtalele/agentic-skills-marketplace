Feature: Example business workflow
  In order to verify the core business behavior
  As a tester or automated workflow
  I want to convert structured test cases into executable Gherkin.

  Background:
    Given the user has access to the application
    And the required configuration is available

  @positive @TC-001 @REQ-001
  Scenario: Submit a valid request successfully
    When the user submits a valid payload
    Then the system accepts the request
    And a success response is returned

  @negative @TC-002 @REQ-001
  Scenario: Reject invalid input
    Given the user submits an invalid payload
    When the request is processed
    Then the system rejects the request
    And an error message is displayed

  @boundary @TC-003 @REQ-001
  Scenario Outline: Handle boundary values
    Given the user submits a value of "<value>"
    When the validation rule is applied
    Then the result should be "<result>"

    Examples:
      | value | result |
      | 0     | invalid |
      | 1     | valid |
      | 999   | valid |

  @positive @TC-004
  Scenario: Process structured payload data
    When the user submits the following payload:
      | field   | value |
      | amount  | 25.00 |
      | currency | USD |
    Then the system stores the payload correctly

  @positive @TC-005
  Scenario: Return a detailed response body
    When the request completes successfully
    Then the API response should be:
      """
      {
        "status": "success",
        "message": "created"
      }
      """
