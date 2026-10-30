import pytest

@pytest.mark.password_reset
def test_user_can_request_password_reset(page):
    page.goto("http://localhost:3000/forgot-password")
    page.fill("[name='email']", "demo@example.test")
    page.click("button[type='submit']")
    assert page.get_by_text("If the account exists, reset instructions will be sent").is_visible()

@pytest.mark.password_reset
def test_password_reset_rejects_invalid_email(page):
    page.goto("http://localhost:3000/forgot-password")
    page.fill("[name='email']", "not-an-email")
    page.click("button[type='submit']")
    assert page.locator("[role='alert']").is_visible()
