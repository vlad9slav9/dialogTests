from playwright.sync_api import Page
from playwright.sync_api import expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

        self._krtech_logo_link = self.page.locator(".SocialComponent-KrtechLogo a")
        self._telegram_button_link = self.page.locator(".SocialComponent-Telegram a")
        self._vkontakte_button_link = self.page.locator(".SocialComponent-Vkontakte a")

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

    def assert_krtech_website_opened(self, new_page):
        expect(new_page).to_have_url("https://krtech.ru/")

    def assert_telegram_website_opened(self, new_page):
        expect(new_page).to_have_url("https://t.me/krtech")

    def assert_vkontakte_website_opened(self, new_page):
        expect(new_page).to_have_url("https://vk.com/krtech_crimea")