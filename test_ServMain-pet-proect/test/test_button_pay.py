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

    # Чекаємо появи елемента в основному DOM або всередині iframe LiqPay
    for _ in range(30):
        try:
            # Шукаємо в iframe
            if page.locator("iframe[src*='liqpay.ua']").count() > 0:
                frame_el = page.frame_locator("iframe[src*='liqpay.ua']").locator(selector).first
                if frame_el.is_visible():
                    return frame_el.screenshot()
            
            # Шукаємо в основному DOM
            dom_el = page.locator(selector).first
            if dom_el.is_visible():
                return dom_el.screenshot()
        except Exception:
            pass
        page.wait_for_timeout(1000)

    # Фінальна спроба з явним очікуванням
    element = page.locator(selector).first
    element.wait_for(state="visible", timeout=10000)
    return element.screenshot()


@pytest.mark.parametrize("banner_method, snapshot_name", BUTTON_CASES)
def test_button_pay(login_in_page, snapshot, banner_method, snapshot_name):
    """Click a payment banner and verify the payment info snapshot."""
    button_pay_page = AllButtonPayPage(login_in_page)

    with allure.step(f"Click {banner_method} and check payment element snapshot"):
        getattr(button_pay_page, banner_method)()

        login_in_page.wait_for_url(re.compile(r"liqpay\.ua"), wait_until="domcontentloaded", timeout=45000)

        snapshot.assert_match(
            capture_element_screenshot(login_in_page, PAYMENT_INFO_LOCATOR),
            snapshot_name,
        )