import pytest
from playwright.sync_api import expect

@pytest.mark.login
def test_user_can_login_with_valid_credentials(page):
    page.goto("http://localhost:3000/login")
    page.fill("[name='username']", "demo_user")
    page.fill("[name='password']", "DemoPass123!")
    page.click("button[type='submit']")
    page.wait_for_url("**/home")
    expect(page).to_have_url("http://localhost:3000/home")

@pytest.mark.login
def test_invalid_password_shows_error(page):
    page.goto("http://localhost:3000/login")
    page.fill("[name='username']", "demo_user")
    page.fill("[name='password']", "wrong-password")
    page.click("button[type='submit']")
    expect(page.locator("[role='alert']")).to_be_visible()
