
from playwright.async_api import Page

class EventPage:
    def __init__(self, page: Page):
        self.page = page
        self._user_profile_button = self.page.get_by_role("button", name="Девятый Д.Д")
