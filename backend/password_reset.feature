Feature: Password Reset API

Background:
  * url baseUrl
  * path '/api/auth/password-reset'

Scenario: Request a password reset
  Given request { email: 'demo@example.test' }
  When method post
  Then status 202

Scenario: Passwords reset rejects an invalid email format
  Given request { email: 'not-an-email' }
  When method post
  Then status 400
