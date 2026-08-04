class AboutPage:

    def __init__(self, page):
        self.page = page
        self.about_nav_link = page.locator("ul.nav li").nth(1)

        self.news_items = page.locator("div.news-item")
        self.news_links = page.locator("a.news-link")

        self.reviews_section = page.locator("aside.reviews-side")
        self.review_input = self.reviews_section.locator("input")
        self.send_button = self.reviews_section.locator("button")

    def open_from_header(self):
        self.page.locator(".modal-overlay").wait_for(state="hidden", timeout=10000)
        self.about_nav_link.click(force=True)
        self.news_links.first.wait_for(state="visible", timeout=10000)

    def get_news_count(self) -> int:
        """Get total count of news items."""
        return self.news_items.count()

    def get_first_news_link(self) -> str:
        """Get href attribute from the first news item."""
        return self.news_links.first.get_attribute("href") or ""

    def submit_review(self, text: str):
        """Fill and submit review form."""
        self.review_input.fill(text)
        self.send_button.click()

    def get_review_input_value(self) -> str:
        """Get current value of the review input field."""
        return self.review_input.input_value()