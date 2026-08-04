class AllButtonPayPage:
    def __init__(self, page):
        self.page = page
        self.vip_element = page.locator('#ServMine img[alt="vip status"]')
        self.admin_element = page.locator('#ServMine img[alt="admin"]')
        self.console_element = page.locator('#ServMine img[alt="console"]')

    def click_banner_vip(self):
        self.vip_element.click(force=True)

    def click_banner_admin(self):
        self.admin_element.click(force=True)

    def click_banner_console(self):
        self.console_element.click(force=True)