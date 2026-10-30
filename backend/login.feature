Feature: User Login API

Background:
  * url baseUrl
  * path '/api/auth/login'

Scenario: Login succeeds with valid credentials
  Given request { username: 'demo_user', password: 'DemoPass123!' }
  When method post
  Then status 200
  And match response contains { token: '#string' }

Scenario: Login fails with an incorrect password
  Given request { username: 'demo_user', password: 'wrong-password' }
  When method post
  Then status 401
