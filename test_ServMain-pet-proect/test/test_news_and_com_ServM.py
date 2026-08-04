import re
import pytest
import allure
from pages.button_pay_ServM import AllButtonPayPage


PAYMENT_INFO_LOCATOR = '[data-testid="sandbox_paper"]'

BUTTON_CASES = [
    pytest.param("click_banner_vip", "payment_info_vip.png", id="vip"),
    pytest.param("click_banner_admin", "payment_info_admin.png", id="admin"),
    pytest.param("click_banner_console", "payment_info_console.png", id="console"),
]


def capture_element_screenshot(page, selector):
    page.mouse.move(0, 0)

    page.add_style_tag(content="""
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
            caret-color: transparent !important;
        }
    """)
    page.wait_for_timeout(500)

    # Пробуємо дочекатися iframe LiqPay, а якщо його немає — шукаємо в основному DOM
    try:
        page.wait_for_selector("iframe[src*='liqpay.ua']", timeout=20000)
        iframe = page.frame_locator("iframe[src*='liqpay.ua']").locator(selector).first
        iframe.wait_for(state="visible", timeout=30000)
        page.wait_for_timeout(300)
        return iframe.screenshot()
    except Exception:
        element = page.locator(selector).first
        element.wait_for(state="visible", timeout=30000)
        page.wait_for_timeout(300)
        return element.screenshot()


@pytest.mark.parametrize("banner_method, snapshot_name", BUTTON_CASES)
def test_button_pay(login_in_page, snapshot, banner_method, snapshot_name):
    """Click a payment banner and verify the payment info snapshot.

    Parametrized over BUTTON_CASES; ids ("vip"/"admin"/"console")
    come from pytest.param(..., id=...) and show up in the test name
    and Allure report.
    """
    button_pay_page = AllButtonPayPage(login_in_page)

    with allure.step(f"Click {banner_method} and check payment element snapshot"):
        getattr(button_pay_page, banner_method)()

        login_in_page.wait_for_url(re.compile(r"liqpay\.ua"), wait_until="networkidle", timeout=60000)

        snapshot.assert_match(
            capture_element_screenshot(login_in_page, PAYMENT_INFO_LOCATOR),
            snapshot_name,
        )