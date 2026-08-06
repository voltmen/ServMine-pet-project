import allure
from pages.news_page_ServM import AboutPage


def test_about_page_news_and_review_submission(login_in_page):
    """Verify news collection loading and review form input/button state on About Us page.

    Intentionally does not click the send button: submitted reviews cannot
    be removed on this environment, so this only checks that the form
    accepts input and the send button becomes interactive.
    """
    about_page = AboutPage(login_in_page)

    with allure.step("Navigate to About Us page via header menu"):
        about_page.open_from_header()

    with allure.step("Validate news feed collection "):
        news_count = about_page.get_news_count()
        assert news_count > 0, f"Expected at least 1 news item, but found {news_count}"

    with allure.step("Validate news links"):
        first_link = about_page.get_first_news_link()
        assert first_link.startswith("http"), f"News link should be a valid URL, got '{first_link}'"

    with allure.step("Fill review form and verify send button becomes interactive"):
        test_comment = "Great Minecraft server! High stability."

        about_page.review_input.fill(test_comment)
        assert about_page.get_review_input_value() == test_comment, "Review input value does not match entered text"

        assert about_page.send_button.is_enabled(), "Send button should be enabled after filling the review form"