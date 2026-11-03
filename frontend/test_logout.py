import pytest
from playwright.sync_api import expect

@pytest.mark.logout
def test_user_can_logout(page):
    page.goto("http://localhost:3000/home")
    page.click("button:has-text('Logout')")
    page.wait_for_url("**/login")
    expect(page).to_have_url("http://localhost:3000/login")
