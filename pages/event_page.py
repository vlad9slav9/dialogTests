
from playwright.sync_api import Page
from playwright.sync_api import expect


class EventPage:
    def __init__(self, page: Page):
        self.page = page
        self._responsible_profile_button = self.page.get_by_role("button", name="Девятый Д.Д")

    def assert_responsible_profile_button_visible(self):
        expect(self._responsible_profile_button).to_be_visible()
