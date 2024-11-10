from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.base_page import BasePage
from datetime import datetime
import locale


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._responsible_profile_button = self.page.get_by_role("button", name="Девятый Д.Д")
        self._logout_button = self.page.locator('[title = "Выход"]')
        self._confirm_logout_button = self.page.get_by_role("button", name="Выйти")
        self._cancel_logout_button = self.page.get_by_role("button", name="Отмена")
        self._sidebar = self.page.locator(".PageSidebar")
        self._hide_sidebar_button = self.page.get_by_role("button", name="Скрыть меню")
        self._open_sidebar_button = self.page.get_by_role("button", name="Открыть меню")
        self._home_button = self.page.get_by_role("button", name="На главную")
        self._event_container = self.page.locator(".EventContainer")
        self._create_document_button = self.page.locator(".DocumentCreateModal")
        self._add_animal_card_button = self.page.get_by_role("button", name="Добавить карточку животного")
        self._quick_search_button = self.page.locator(".DocumentQuickSearchAutocomplete-SearchButton")
        self._support_service_button = self.page.get_by_role("button", name="Служба поддержки (Ctrl+Alt+2)")
        self._reference_materials_button = self.page.get_by_role("button", name="Справочные материалы")
        self._displayed_date = self.page.locator(".style_date__TlIM3")

    def click_responsible_profile_button(self):
        self._responsible_profile_button.click()

    def click_logout_button(self):
        self._logout_button.click()

    def click_confirm_logout_button(self):
        self._confirm_logout_button.click()

    def click_cancel_logout_button(self):
        self._cancel_logout_button.click()

    def click_hide_sidebar_button(self):
        self._hide_sidebar_button.click()

    def click_open_sidebar_button(self):
        self._open_sidebar_button.click()

    def click_home_button(self):
        self._home_button.click()

    def assert_responsible_profile_button_visible(self):
        expect(self._responsible_profile_button).to_be_visible()

    def assert_sidebar_visible(self):
        expect(self._sidebar).to_be_visible()

    def assert_sidebar_hidden(self):
        expect(self._sidebar).to_be_hidden()

    def assert_event_container_visible(self):
        expect(self._event_container).to_be_visible()

    def assert_displayed_date(self):
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
        expected_date = datetime.now().strftime("%A, %d.%m.%Y").capitalize()
        expect(self._displayed_date).to_have_text(expected_date)