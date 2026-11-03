import pytest
from playwright.sync_api import expect

@pytest.mark.registration
def test_user_can_register(page):
    page.goto("http://localhost:3000/register")
    page.fill("[name='username']", "new_demo_user")
    page.fill("[name='email']", "new@example.test")
    page.fill("[name='password']", "DemoPass123!")
    page.click("button[type='submit']")
    expect(page.get_by_text("Registration successful")).to_be_visible()

@pytest.mark.registration
def test_registration_requires_email(page):
    page.goto("http://localhost:3000/register")
    page.fill("[name='username']", "new_demo_user")
    page.fill("[name='password']", "DemoPass123!")
    page.click("button[type='submit']")
    expect(page.locator("[name='email']")).to_have_attribute("required", "")
