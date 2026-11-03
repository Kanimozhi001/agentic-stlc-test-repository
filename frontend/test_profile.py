import pytest
from playwright.sync_api import expect

@pytest.mark.profile
def test_user_can_view_profile(page):
    page.goto("http://localhost:3000/profile")
    expect(page.get_by_role("heading", name="My Profile")).to_be_visible()

@pytest.mark.profile
def test_user_can_update_display_name(page):
    page.goto("http://localhost:3000/profile")
    page.fill("[name='displayName']", "Demo User")
    page.click("button:has-text('Save')")
    expect(page.get_by_text("Profile updated")).to_be_visible()
