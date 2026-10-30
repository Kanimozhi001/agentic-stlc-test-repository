Feature: User Registration API

Background:
  * url baseUrl
  * path '/api/auth/register'

Scenario: Register a new user
  Given request { username: 'new_demo_user', email: 'new@example.test', password: 'DemoPass123!' }
  When method post
  Then status 201

Scenario: Registration rejects an existing email
  Given request { username: 'another_user', email: 'existing@example.test', password: 'DemoPass123!' }
  When method post
  Then status 409
