```gherkin
Feature: Student Management System API Tests
  # -------------------------------------------------
  # Assumptions (placeholders):
  #   - BASE_URL: the base URL of the Student Management API
  #   - AUTH_TOKEN: a valid bearer token for authentication
  #   - The API follows typical REST conventions:
  #       POST   /api/students               -> 201 Created, returns { id: <number>, ... }
  #       PUT    /api/students/{id}          -> 200 OK, returns updated student
  #       PATCH  /api/students/{id}          -> 200 OK, returns updated student
  #       DELETE /api/students/{id}          -> 204 No Content
  #       GET    /api/students/search        -> 200 OK, returns list of students
  #   - Request/response payloads are JSON.
  # -------------------------------------------------

  Background:
    * url BASE_URL
    * header Authorization = 'Bearer ' + AUTH_TOKEN
    * configure headers = { 'Content-Type': 'application/json' }

  # -----------------------------------------------------------------
  # Positive Scenarios
  # -----------------------------------------------------------------

  Scenario: Add a new student (positive)
    Given path '/api/students'
    And request
    """
    {
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com",
      "age": 20
    }
    """
    When method post
    Then status 201
    And match response == { id: '#number', firstName: 'John', lastName: 'Doe', email: 'john.doe@example.com', age: 20 }
    # Store the created student id for later scenarios
    * def studentId = response.id

  Scenario: Update an existing student (positive - full replace)
    # Prerequisite: a student has been created in the previous scenario
    Given path '/api/students', studentId
    And request
    """
    {
      "firstName": "Jane",
      "lastName": "Doe",
      "email": "jane.doe@example.com",
      "age": 21
    }
    """
    When method put
    Then status 200
    And match response == { id: '#(studentId)', firstName: 'Jane', lastName: 'Doe', email: 'jane.doe@example.com', age: 21 }

  Scenario: Partially update an existing student (positive - PATCH)
    Given path '/api/students', studentId
    And request
    """
    {
      "age": 22
    }
    """
    When method patch
    Then status 200
    And match response.age == 22

  Scenario: Search for students by name (positive)
    Given path '/api/students/search'
    And param q = 'Doe'    # placeholder query parameter name/value
    When method get
    Then status 200
    And match response == '#[0]'   # at least one result
    And match each response contains { firstName: '#string', lastName: '#string', email: '#string', age: '#number' }

  Scenario: Delete an existing student (positive)
    Given path '/api/students', studentId
    When method delete
    Then status 204

  # -----------------------------------------------------------------
  # Negative / Edge Cases
  # -----------------------------------------------------------------

  Scenario: Add a student with missing required field (negative)
    Given path '/api/students'
    And request
    """
    {
      "firstName": "Alice",
      "lastName": "Smith",
      "age": 19
      // email is missing – assumed required
    }
    """
    When method post
    Then status 400
    And match response.error == '#string'

  Scenario: Add a duplicate student (negative)
    # First add a student
    * def duplicatePayload =
    """
    {
      "firstName": "Bob",
      "lastName": "Brown",
      "email": "bob.brown@example.com",
      "age": 23
    }
    """
    Given path '/api/students'
    And request duplicatePayload
    When method post
    Then status 201
    * def dupId = response.id

    # Attempt to add the same student again
    Given path '/api/students'
    And request duplicatePayload
    When method post
    Then status 409
    And match response.error == '#string'

    # Cleanup
    Given path '/api/students', dupId
    When method delete
    Then status 204

  Scenario: Update a non‑existent student (negative)
    Given path '/api/students', 999999   # assumed non‑existent id
    And request
    """
    {
      "firstName": "Ghost",
      "lastName": "User",
      "email": "ghost.user@example.com",
      "age": 30
    }
    """
    When method put
    Then status 404
    And match response.error == '#string'

  Scenario: Delete a non‑existent student (negative)
    Given path '/api/students', 999999   # assumed non‑existent id
    When method delete
    Then status 404
    And match response.error == '#string'

  Scenario: Search with invalid query parameter (negative)
    Given path '/api/students/search'
    And param q = ''   # empty query – assumed invalid
    When method get
    Then status 400
    And match response.error == '#string'
```
