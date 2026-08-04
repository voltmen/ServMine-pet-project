import allure
from pages.ServM_profile import ProfilePage


def test_profile_card_display_and_data_structure(login_in_page):
    """Verify profile card visibility, header tag, and user data format."""
    profile_page = ProfilePage(login_in_page)

    with allure.step("Navigate to profile page via header menu"):
        profile_page.open_from_header()

    with allure.step("Verify profile card and heading visibility"):
        assert profile_page.is_card_visible(), "Profile card element 'div.profile-card' is missing or hidden"

        heading_text = profile_page.get_heading_text()
        assert len(heading_text) > 0, "Profile heading <h2> should not be empty"

    with allure.step("Validate dynamic user email and content format"):
        card_text = profile_page.get_card_text()

        email_match = "@" in card_text
        assert email_match, "Valid email address was not found in profile card"

        assert len(card_text.strip()) > 0, "Profile card content is empty"