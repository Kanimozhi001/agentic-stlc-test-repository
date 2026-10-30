import pytest

@pytest.mark.profile
def test_user_can_view_profile(page):
    page.goto("http://localhost:3000/profile")
    assert page.get_by_role("heading", name="My Profile").is_visible()

@pytest.mark.profile
def test_user_can_update_display_name(page):
    page.goto("http://localhost:3000/profile")
    page.fill("[name='displayName']", "Demo User")
    page.click("button:has-text('Save')")
    assert page.get_by_text("Profile updated").is_visible()
