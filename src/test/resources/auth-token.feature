Feature: Create a demo authentication token for backend tests

Scenario:
  * def baseUrl = __arg.baseUrl
  Given url baseUrl
  And path '/api/auth/login'
  And request { username: 'demo_user', password: 'DemoPass123!' }
  When method post
  Then status 200
  And def token = response.token
