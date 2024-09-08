import configparser

from playwright.async_api import Page
from playwright.sync_api import expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self._username_input = self.page.locator("#login")
        self._password_input = self.page.locator("password")
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