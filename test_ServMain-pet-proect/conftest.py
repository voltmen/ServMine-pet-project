import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()

TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


@pytest.fixture(autouse=True)
def set_viewport(page: Page):
    page.set_viewport_size({"width": 1920, "height": 1080})


@pytest.fixture(scope="function")
def login_in_page(page: Page):
    """Register a fresh user and log them in before handing the page to the test."""
    assert TEST_EMAIL and TEST_USERNAME and TEST_PASSWORD, (
        "TEST_EMAIL, TEST_USERNAME and TEST_PASSWORD must be set "
        "(check your .env file or CI secrets)"
    )

    page.goto("http://localhost:3000", timeout=30000)

    # 1. Open the auth modal
    page.click("ul.nav li:nth-child(3)")

    # 2. Switch to registration mode
    page.click("p.toggle-auth")

    # 3. Fill and submit registration form
    page.fill("input[name='email']", TEST_EMAIL)
    page.fill("input[name='username']", TEST_USERNAME)
    page.fill("input[name='password']", TEST_PASSWORD)
    page.locator("button.auth-btn:visible").click()

    # 4. Handle transition back to login mode
    try:
        # Чекаємо, поки зникне поле email або перемикаємо вручну
        page.locator("input[name='email']").wait_for(state="hidden", timeout=3000)
    except Exception:
        page.click("p.toggle-auth")

    # 5. Perform login
    page.fill("input[name='username']", TEST_USERNAME)
    page.fill("input[name='password']", TEST_PASSWORD)
    page.locator("button.auth-btn:visible").click()

    # 6. Ensure modal is fully closed
    page.locator(".modal-overlay").wait_for(state="hidden", timeout=10000)

    return page