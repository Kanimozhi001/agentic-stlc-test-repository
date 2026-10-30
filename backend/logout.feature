Feature: User Logout API

Scenario: Logout an authenticated user
  Given url baseUrl
  And path '/api/auth/logout'
  And header Authorization = 'Bearer ' + authToken
  When method post
  Then status 200
