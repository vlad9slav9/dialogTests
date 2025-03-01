from playwright.sync_api import Page
from playwright.sync_api import expect
import random
import datetime


class BasePage:
    def __init__(self, page: Page):
        self.page = page

        self._krtech_logo_link = self.page.locator('.SocialComponent-KrtechLogo a')
        self._telegram_button_link = self.page.locator('.SocialComponent-Telegram a')
        self._vkontakte_button_link = self.page.locator('.SocialComponent-Vkontakte a')
        self._dropdown_list_without_options = self.page.get_by_text('No options')

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
        expect(new_page).to_have_url('https://krtech.ru/')

    def assert_telegram_website_opened(self, new_page):
        expect(new_page).to_have_url('https://t.me/krtech')

    def assert_vkontakte_website_opened(self, new_page):
        expect(new_page).to_have_url('https://vk.com/krtech_crimea')


    def generate_random_string_with_all_symbols(self):
        digits = '0123456789'
        lowercase = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        uppercase = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        special_chars = '!@#$%^&*()_+-=[]{}|;:\'",.<>?/`~'

        random_digit = random.choice(digits)
        random_lowercase = random.choice(lowercase)
        random_uppercase = random.choice(uppercase)

        random_string = random_digit + random_lowercase + random_uppercase + special_chars

        random_string = ''.join(random.sample(random_string, len(random_string)))

        return random_string

    def generate_date_offset_days(self, days=0, year=False):
        if year:
            date_offset = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y')
        else:
            date_offset = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%d.%m.%Y')
        return date_offset

    def get_user_data(self, data_name):
        user_data_locator = self.page.locator(f'p.MuiTypography-root.MuiTypography-body1:has(strong:text("{data_name}"))')
        user_data = user_data_locator.inner_text().split(':')[-1].strip()
        return user_data

    def assert_dropdown_list_contain_text(self, search_text):
        document_type_options = self.page.locator("role=option")
        expect(document_type_options).not_to_have_count(0)
        all_options = document_type_options.all()
        for option in all_options:
            expect(option).to_contain_text(search_text, ignore_case=True)

    def assert_dropdown_list_without_options_visible(self, wait_time=3000):
        options_locator = self.page.locator("role=option")
        self.page.wait_for_timeout(wait_time)
        expect(options_locator).to_have_count(0)
        expect(self._dropdown_list_without_options).to_be_visible()
