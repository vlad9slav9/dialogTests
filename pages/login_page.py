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
        self._krtech_logo_link = self.page.locator(".SocialComponent-KrtechLogo a")
        self._telegram_button_link = self.page.locator(".SocialComponent-Telegram a")
        self._vkontakte_button_link = self.page.locator(".SocialComponent-Vkontakte a")

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

    def click_and_open_new_tab(self, button_link):
        context = self.page.context
        with context.expect_page() as new_page_info:
            button_link.click()
        new_page = new_page_info.value
        return new_page

    def click_krtech_logo(self):
        return self.click_and_open_new_tab(self._krtech_logo_link)

    def click_telegram_button(self):
        return self.click_and_open_new_tab(self._telegram_button_link)

    def click_vkontakte_button(self):
        return self.click_and_open_new_tab(self._vkontakte_button_link)

    def assert_login_error_visible(self):
        expect(self._login_error_message).to_be_visible()

    def assert_login_page_logo_visible(self):
        expect(self._login_page_logo).to_be_visible()

    def assert_login_button_disabled(self):
        expect(self._login_button).to_be_disabled()

    def assert_krtech_website_opened(self, new_page):
        expect(new_page).to_have_url("https://krtech.ru/")

    def assert_telegram_website_opened(self, new_page):
        expect(new_page).to_have_url("https://t.me/krtech")

    def assert_vkontakte_website_opened(self, new_page):
        expect(new_page).to_have_url("https://vk.com/krtech_crimea")