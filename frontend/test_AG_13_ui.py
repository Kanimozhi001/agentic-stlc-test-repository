import pytest
from playwright.sync_api import Playwright, sync_playwright, expect

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    """Start Playwright for the test session."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright):
    """Launch a browser instance (headless by default)."""
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def page(browser):
    """Create a new browser context and page for each test."""
    context = browser.new_context()
    page = context.new_page()
    # Placeholder: replace with the actual base URL of the Student Management System
    page.goto("{{BASE_URL}}/students")
    yield page
    context.close()


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def add_student_via_ui(page, name, email, age):
    """
    Helper to add a student using the UI.
    Returns when the student row appears in the list.
    """
    # Click the "Add Student" button
    page.click("{{ADD_STUDENT_BUTTON_SELECTOR}}")  # e.g., "#add-student-button"

    # Fill the form fields
    page.fill("{{STUDENT_NAME_INPUT_SELECTOR}}", name)      # e.g., "#student-name-input"
    page.fill("{{STUDENT_EMAIL_INPUT_SELECTOR}}", email)    # e.g., "#student-email-input"
    page.fill("{{STUDENT_AGE_INPUT_SELECTOR}}", str(age))   # e.g., "#student-age-input"

    # Submit the form
    page.click("{{SAVE_STUDENT_BUTTON_SELECTOR}}")  # e.g., "#save-student-button"

    # Wait for success toast or the new row to appear
    expect(page.locator("{{SUCCESS_TOAST_SELECTOR}}")).to_be_visible()  # e.g., ".toast-success"
    # Verify the new row appears in the table/list
    new_row = page.locator("{{STUDENT_ROW_SELECTOR}}", has_text=name)
    expect(new_row).to_be_visible()
    return new_row


def search_student(page, query):
    """Perform a search for a student."""
    page.fill("{{SEARCH_INPUT_SELECTOR}}", query)   # e.g., "#search-input"
    page.click("{{SEARCH_BUTTON_SELECTOR}}")       # e.g., "#search-button"


# ----------------------------------------------------------------------
# Test cases
# ----------------------------------------------------------------------
def test_add_student_success(page):
    """Positive scenario: add a student with valid data."""
    name = "John Doe"
    email = "john.doe@example.com"
    age = 21

    new_row = add_student_via_ui(page, name, email, age)

    # Additional assertions on the row content
    expect(new_row.locator("{{STUDENT_EMAIL_CELL_SELECTOR}}")).to_have_text(email)
    expect(new_row.locator("{{STUDENT_AGE_CELL_SELECTOR}}")).to_have_text(str(age))


def test_add_student_missing_required_fields(page):
    """Negative scenario: attempt to add a student without required fields."""
    page.click("{{ADD_STUDENT_BUTTON_SELECTOR}}")
    # Intentionally leave the name empty, fill other fields
    page.fill("{{STUDENT_EMAIL_INPUT_SELECTOR}}", "missing.name@example.com")
    page.fill("{{STUDENT_AGE_INPUT_SELECTOR}}", "19")
    page.click("{{SAVE_STUDENT_BUTTON_SELECTOR}}")

    # Expect validation error for the missing name
    expect(page.locator("{{NAME_FIELD_ERROR_SELECTOR}}")).to_be_visible()  # e.g., "#student-name-error"


def test_search_student_found(page):
    """Positive scenario: search for an existing student."""
    # Ensure a known student exists
    name = "Alice Smith"
    add_student_via_ui(page, name, "alice.smith@example.com", 22)

    # Perform search
    search_student(page, name)

    # Expect the result row to be visible
    result_row = page.locator("{{STUDENT_ROW_SELECTOR}}", has_text=name)
    expect(result_row).to_be_visible()


def test_search_student_not_found(page):
    """Negative scenario: search for a non‑existent student."""
    search_student(page, "NonExistentStudent123")

    # Expect a 'no results' indicator
    expect(page.locator("{{NO_RESULTS_SELECTOR}}")).to_be_visible()  # e.g., ".no-results"


def test_update_student_success(page):
    """Positive scenario: update an existing student's details."""
    # Create a student to update
    original_name = "Bob Johnson"
    row = add_student_via_ui(page, original_name, "bob.j@example.com", 20)

    # Click the edit button for that row
    row.locator("{{EDIT_BUTTON_SELECTOR}}").click()  # e.g., ".edit-button"

    # Change the email and age
    new_email = "bob.johnson@newmail.com"
    new_age = 21
    page.fill("{{STUDENT_EMAIL_INPUT_SELECTOR}}", new_email)
    page.fill("{{STUDENT_AGE_INPUT_SELECTOR}}", str(new_age))
    page.click("{{SAVE_STUDENT_BUTTON_SELECTOR}}")

    # Verify success toast
    expect(page.locator("{{SUCCESS_TOAST_SELECTOR}}")).to_be_visible()
    # Verify updated values in the row
    expect(row.locator("{{STUDENT_EMAIL_CELL_SELECTOR}}")).to_have_text(new_email)
    expect(row.locator("{{STUDENT_AGE_CELL_SELECTOR}}")).to_have_text(str(new_age))


def test_update_student_invalid_email(page):
    """Negative scenario: attempt to update a student with an invalid email."""
    name = "Carol White"
    row = add_student_via_ui(page, name, "carol.w@example.com", 23)

    # Open edit dialog
    row.locator("{{EDIT_BUTTON_SELECTOR}}").click()
    # Enter invalid email
    page.fill("{{STUDENT_EMAIL_INPUT_SELECTOR}}", "invalid-email")
    page.click("{{SAVE_STUDENT_BUTTON_SELECTOR}}")

    # Expect validation error for email field
    expect(page.locator("{{EMAIL_FIELD_ERROR_SELECTOR}}")).to_be_visible()


def test_delete_student_success(page):
    """Positive scenario: delete an existing student."""
    name = "David Green"
    row = add_student_via_ui(page, name, "david.g@example.com", 24)

    # Click the delete button for that row
    row.locator("{{DELETE_BUTTON_SELECTOR}}").click()  # e.g., ".delete-button"

    # Confirm deletion in the modal/dialog
    page.click("{{CONFIRM_DELETE_BUTTON_SELECTOR}}")  # e.g., "#confirm-delete"

    # Expect success toast
    expect(page.locator("{{SUCCESS_TOAST_SELECTOR}}")).to_be_visible()
    # Verify the row is no longer present
    expect(page.locator("{{STUDENT_ROW_SELECTOR}}", has_text=name)).to_have_count(0)


def test_delete_student_cancel(page):
    """Negative scenario: cancel deletion and ensure the student remains."""
    name = "Eve Black"
    row = add_student_via_ui(page, name, "eve.b@example.com", 25)

    # Initiate delete
    row.locator("{{DELETE_BUTTON_SELECTOR}}").click()
    # Cancel the deletion
    page.click("{{CANCEL_DELETE_BUTTON_SELECTOR}}")  # e.g., "#cancel-delete"

    # Verify the row is still present
    expect(page.locator("{{STUDENT_ROW_SELECTOR}}", has_text=name)).to_be_visible()


# ----------------------------------------------------------------------
# Notes
# ----------------------------------------------------------------------
# - All selectors wrapped in double curly braces (e.g., {{SELECTOR}}) are
#   placeholders. Replace them with the actual CSS/XPath selectors used by
#   the application under test.
# - {{BASE_URL}} should be set to the root URL of the Student Management System.
# - The helper `add_student_via_ui` is used to keep tests independent and
#   readable; it can be expanded with additional steps (e.g., waiting for
#   network responses) if needed.
# - The tests rely on Playwright's built‑in `expect` for reliable waiting
#   and assertions on UI state changes.
