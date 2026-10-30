import pytest

@pytest.mark.logout
def test_user_can_logout(page):
    page.goto("http://localhost:3000/home")
    page.click("button:has-text('Logout')")
    page.wait_for_url("**/login")
    assert page.url.endswith("/login")
