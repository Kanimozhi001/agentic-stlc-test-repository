import pytest

@pytest.mark.registration
def test_user_can_register(page):
    page.goto("http://localhost:3000/register")
    page.fill("[name='username']", "new_demo_user")
    page.fill("[name='email']", "new@example.test")
    page.fill("[name='password']", "DemoPass123!")
    page.click("button[type='submit']")
    assert page.get_by_text("Registration successful").is_visible()

@pytest.mark.registration
def test_registration_requires_email(page):
    page.goto("http://localhost:3000/register")
    page.fill("[name='username']", "new_demo_user")
    page.fill("[name='password']", "DemoPass123!")
    page.click("button[type='submit']")
    assert page.locator("[name='email']").get_attribute("required") is not None
