import pytest

@pytest.mark.login
def test_user_can_login_with_valid_credentials(page):
    page.goto("http://localhost:3000/login")
    page.fill("[name='username']", "demo_user")
    page.fill("[name='password']", "DemoPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("**/home")
    assert page.url.endswith("/home")

@pytest.mark.login
def test_invalid_password_shows_error(page):
    page.goto("http://localhost:3000/login")
    page.fill("[name='username']", "demo_user")
    page.fill("[name='password']", "wrong-password")
    page.click("button[type='submit']")
    assert page.locator("[role='alert']").is_visible()
