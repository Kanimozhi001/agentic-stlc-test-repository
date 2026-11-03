import pytest
from playwright.sync_api import expect

@pytest.mark.password_reset
def test_user_can_request_password_reset(page):
    page.goto("http://localhost:3000/forgot-password")
    page.fill("[name='email']", "demo@example.test")
    page.click("button[type='submit']")
    expect(page.get_by_text("If the account exists, reset instructions will be sent")).to_be_visible()

@pytest.mark.password_reset
def test_password_reset_rejects_invalid_email(page):
    page.goto("http://localhost:3000/forgot-password")
    page.fill("[name='email']", "not-an-email")
    page.click("button[type='submit']")
    expect(page.locator("[role='alert']")).to_be_visible()
