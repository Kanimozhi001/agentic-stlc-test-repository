Feature: User Profile API

Background:
  * url baseUrl
  * header Authorization = 'Bearer ' + authToken

Scenario: Retrieve the current user's profile
  Given path '/api/users/me'
  When method get
  Then status 200
  And match response.username == '#string'

Scenario: Update the current user's display name
  Given path '/api/users/me'
  And request { displayName: 'Demo User' }
  When method patch
  Then status 200
