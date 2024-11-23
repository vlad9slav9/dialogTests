import configparser

from playwright.sync_api import Page
from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.main_page import MainPage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.config = configparser.ConfigParser()
        self.config.read("auth.ini")
        self._username_input_field = self.page.locator("#login")
        self._password_input_field = self.page.locator("#password")
        self._login_button = self.page.locator("#login_enter_button")
        self._login_error_message = self.page.get_by_text("Введены неверные данные")
        self._login_page_logo = self.page.get_by_text("Войти в систему электронного документооборота")

    def navigate(self):
        self.page.goto("/")

    def enter_username(self, username):
        self._username_input_field.fill(username)

    def enter_password(self, password):
        self._password_input_field.fill(password)

    def click_login(self):
        self._login_button.click()

    def do_login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_responsible_username(self):
        return self.config['responsible']['username']

    def get_responsible_password(self):
        return self.config['responsible']['password']

    def login_with_responsible(self):
        self.do_login(self.get_responsible_username(), self.get_responsible_password())
        return MainPage(self.page)

    def assert_login_error_visible(self):
        expect(self._login_error_message).to_be_visible()

    def assert_login_page_logo_visible(self):
        expect(self._login_page_logo).to_be_visible()

    def assert_login_button_disabled(self):
        expect(self._login_button).to_be_disabled()