import configparser

from playwright.sync_api import Page
from playwright.sync_api import expect

from pages.event_page import EventPage


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.config = configparser.ConfigParser()
        self.config.read("auth.ini")

        self._username_input = self.page.locator("#login")
        self._password_input = self.page.locator("#password")
        self._login_button = self.page.locator("#login_enter_button")
        self._login_error_message = self.page.get_by_text("Введены неверные данные")
        self._login_page_logo = self.page.get_by_text("Войти в систему электронного документооборота")
        self._krtech_logo_link = self.page.get_by_role("link").first

    def navigate(self):
        self.page.goto("/")

    def enter_username(self, username):
        self._username_input.fill(username)

    def enter_password(self, password):
        self._password_input.fill(password)

    def click_login(self):
        self._login_button.click()

    def do_login(self, username, password):
        self._username_input.fill(username)
        self._password_input.fill(password)
        self._login_button.click()

    def get_responsible_username(self):
        return self.config['responsible']['username']

    def get_responsible_password(self):
        return self.config['responsible']['password']

    def login_with_responsible(self):
        self.do_login(self.get_responsible_username(), self.get_responsible_password())
        return EventPage(self.page)

    def click_krtech_logo(self):
        context = self.page.context
        with context.expect_page() as krtech_website:
            self._krtech_logo_link.click()
        krtech_page = krtech_website.value
        krtech_page.wait_for_load_state()
        return krtech_page












    def assert_login_error_visible(self):
        expect(self._login_error_message).to_be_visible()

    def assert_login_page_logo_visible(self):
        expect(self._login_page_logo).to_be_visible()

    def assert_login_button_disabled(self):
        expect(self._login_button).to_be_disabled()

    def assert_krtech_website_opened(self, new_page):
        expect(new_page).to_have_url("https://krtech.ru/")
