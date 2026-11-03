Feature: Search Products
  # ------------------------------------------------------------
  #  This feature validates the product search functionality.
  #  Assumptions (place‑holders):
  #   * Base URL is defined in a Karate config file as `baseUrl`.
  #   * Search endpoint: GET ${baseUrl}/api/products/search
  #   * Query parameter for the search term is `q`.
  #   * Successful search returns HTTP 200 with a JSON array of products.
  #   * When no product matches, the API returns HTTP 200 with a
  #     JSON object containing a message: "No products found".
  #   * Empty search term is considered a client error (HTTP 400) with
  #     a validation message.
  # ------------------------------------------------------------

  Background:
    * url baseUrl + '/api/products/search'

  # -----------------------------------------------------------------
  # Positive scenarios – matching products
  # -----------------------------------------------------------------
  Scenario: Search "Laptop" – matching laptops displayed
    Given param q = 'Laptop'
    When method get
    Then status 200
    And match each response[*].name contains 'Laptop'

  Scenario: Search "Phone" – matching phones displayed
    Given param q = 'Phone'
    When method get
    Then status 200
    And match each response[*].name contains 'Phone'

  # -----------------------------------------------------------------
  # Positive scenario – partial name match
  # -----------------------------------------------------------------
  Scenario: Search partial name "Lap" – matching products displayed
    Given param q = 'Lap'
    When method get
    Then status 200
    # All returned product names should contain the substring "Lap"
    And match each response[*].name contains 'Lap'

  # -----------------------------------------------------------------
  # Negative scenario – no matching product
  # -----------------------------------------------------------------
  Scenario: Search "xyz123" – no products found
    Given param q = 'xyz123'
    When method get
    Then status 200
    # The API returns a message when the result set is empty
    And match response == { message: 'No products found' }

  # -----------------------------------------------------------------
  # Negative scenario – empty search input
  # -----------------------------------------------------------------
  Scenario: Search with empty input – validation message displayed
    Given param q = ''
    When method get
    Then status 400
    # Validation error returned by the API
    And match response == { error: 'Search term is required' }
