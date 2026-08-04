class ProfilePage:

    def __init__(self, page):
        self.page = page
        self.profile_card = page.locator("div.profile-card")
        self.profile_nav_link = page.locator("ul.nav li").nth(2)
        self.card_heading = self.profile_card.locator("h2")

    def open_from_header(self):
        self.page.locator(".modal-overlay").wait_for(state="hidden", timeout=10000)
        self.profile_nav_link.click(force=True)
        self.profile_card.wait_for(state="visible", timeout=10000)

    def is_card_visible(self) -> bool:
        return self.profile_card.is_visible()

    def get_heading_text(self) -> str:
        return self.card_heading.inner_text()

    def get_card_text(self) -> str:
        return self.profile_card.inner_text()