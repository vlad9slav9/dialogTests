import configparser

from playwright.sync_api import Page
from playwright.sync_api import expect

from pages.event_page import EventPage


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self._username_input = self.page.locator("#login")
        self._password_input = self.page.locator("#password")
        self._login_button = self.page.locator("#login_enter_button")
        self._login_error_message = self.page.get_by_text("Введены неверные данные")
        self.config = configparser.ConfigParser()
        self.config.read("auth.ini")

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
        username = self.get_responsible_username()
        password = self.get_responsible_password()
        self.do_login(username, password)
        return EventPage(self.page)

    def assert_login_error_visible(self):
        expect(self._login_error_message).to_be_visible()