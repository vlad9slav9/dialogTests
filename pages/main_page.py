from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._responsible_profile_button = self.page.get_by_role("button", name="Девятый Д.Д")
        self._logout_button = self.page.locator('[title = "Выход"]')
        self._confirm_logout_button = self.page.get_by_role("button", name="Выйти")
        self._cancel_logout_button = self.page.get_by_role("button", name="Отмена")

    def assert_responsible_profile_button_visible(self):
        expect(self._responsible_profile_button).to_be_visible()

    def click_logout_button(self):
        self._logout_button.click()

    def click_confirm_logout_button(self):
        self._confirm_logout_button.click()

    def click_cancel_logout_button(self):
        self._cancel_logout_button.click()
