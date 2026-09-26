from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class EventPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Элементы дашборда главной страницы
        self._event_container = self.page.locator(".EventContainer")

    # Проверки дашборда
    def assert_event_container_visible(self):
        expect(self._event_container).to_be_visible()
