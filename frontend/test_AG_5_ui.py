import pytest
from playwright.sync_api import sync_playwright, Page, expect

# ==============================
# PLACEHOLDER CONFIGURATION
# ==============================
BASE_URL = "https://<YOUR_APPLICATION_URL>"  # TODO: replace with actual application URL
SEARCH_INPUT_SELECTOR = "css=input[name='search']"  # TODO: replace with actual selector for the search box
SEARCH_BUTTON_SELECTOR = "css=button[id='searchBtn']"  # TODO: replace with actual selector for the search button (if any)
RESULT_ITEMS_SELECTOR = "css=.search-results .product-item"  # TODO: replace with selector that matches each product in the result list
NO_RESULTS_MESSAGE_SELECTOR = "css=.no-results"  # TODO: replace with selector that displays the 'No products found' message
NO_RESULTS_TEXT = "No products found"  # TODO: verify exact text shown by the application
EMPTY_INPUT_VALIDATION_SELECTOR = "css=.search-validation"  # TODO: replace with selector for empty‑input validation message
EMPTY_INPUT_VALIDATION_TEXT = "Please enter a product name"  # TODO: verify exact validation message


# ==============================
# Pytest fixtures
# ==============================
@pytest.fixture(scope="session")
def playwright_context():
    """Start Playwright and create a browser context for the whole test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=False for debugging
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(playwright_context) -> Page:
    """Create a new page for each test."""
    page = playwright_context.new_page()
    yield page
    page.close()


# ==============================
# Helper functions
# ==============================
def perform_search(page: Page, query: str):
    """Enter a query into the search box and trigger the search."""
    page.goto(BASE_URL)
    # Ensure the search input is ready
    page.wait_for_selector(SEARCH_INPUT_SELECTOR)
    page.fill(SEARCH_INPUT_SELECTOR, query)

    # If the UI requires clicking a button, use it; otherwise press Enter.
    try:
        page.click(SEARCH_BUTTON_SELECTOR)
    except Exception:
        # Fallback to pressing Enter if button is not present or fails
        page.press(SEARCH_INPUT_SELECTOR, "Enter")

    # Wait for either results or a no‑results message to appear
    page.wait_for_load_state("networkidle")


def assert_results_contain(page: Page, expected_substring: str):
    """Assert that at least one result item contains the expected substring."""
    results = page.locator(RESULT_ITEMS_SELECTOR)
    expect(results).to_have_count_greater_than(0)
    # Verify that at least one result includes the expected text (case‑insensitive)
    matching = results.filter(has_text=expected_substring, ignore_case=True)
    expect(matching).to_have_count_greater_than(0)


def assert_no_results_message(page: Page):
    """Assert that the 'no results' message is displayed."""
    no_results = page.locator(NO_RESULTS_MESSAGE_SELECTOR)
    expect(no_results).to_be_visible()
    expect(no_results).to_have_text(NO_RESULTS_TEXT)


def assert_empty_input_validation(page: Page):
    """Assert that the validation message for an empty search is displayed."""
    validation = page.locator(EMPTY_INPUT_VALIDATION_SELECTOR)
    expect(validation).to_be_visible()
    expect(validation).to_have_text(EMPTY_INPUT_VALIDATION_TEXT)


# ==============================
# Test cases
# ==============================
def test_search_laptop_returns_matching_products(page: Page):
    """
    Scenario: Search "Laptop"
    Expected result: Matching laptops displayed
    """
    perform_search(page, "Laptop")
    assert_results_contain(page, "Laptop")


def test_search_phone_returns_matching_products(page: Page):
    """
    Scenario: Search "Phone"
    Expected result: Matching phones displayed
    """
    perform_search(page, "Phone")
    assert_results_contain(page, "Phone")


def test_search_nonexistent_product_shows_no_results(page: Page):
    """
    Scenario: Search "xyz123"
    Expected result: No products found
    """
    perform_search(page, "xyz123")
    assert_no_results_message(page)


def test_search_partial_name_returns_matching_products(page: Page):
    """
    Scenario: Search partial name "Lap"
    Expected result: Matching products displayed
    """
    perform_search(page, "Lap")
    # Assuming that a partial match still contains the full term in the result text
    assert_results_contain(page, "Lap")


def test_search_with_empty_input_shows_validation_message(page: Page):
    """
    Scenario: Search with empty input
    Expected result: Validation message displayed
    """
    perform_search(page, "")
    assert_empty_input_validation(page)
