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

        self.group_with_organizations = ['ФУЛ МКУ 9', 'Тестовая 9919', "РЕадмин", "Министерство сэд 2.0"]
        self.department_users = [
            'Ответственный Первый Пользователь | Автотестовая Родительская организация | Первая автотестовая должность',
            'Обычный Первый Пользователь | Автотестовая Родительская организация | Вторая автотестовая должность']
        self.department_curators = [
            'Волохов Алексей Николаевич | Аппарат Совета министров Республики Крым | Глава Республики Крым',
            'Косторнова Елена Борисовна | Аппарат Совета министров Республики Крым | Начальник управления']
        self.mku_users = [
            'Второй Юзер Мкушнович | МКУ Автотестовое | Второго уровня должность',
            'Мкушный Пользователь Ответственный | МКУ Автотестовое | Должность первого уровня']
        self.users_from_other_departments = [
            'Андрошин Андрей Владимирович | Министерство Тестирования РК | Генеральный директор	',
            'Сидоров Артем Сергеевич | Министерство сэд 2.0 | Руководитель']
        self.users_with_mku = self.department_users + self.mku_users
        self.users_with_mku_and_curators = self.users_with_mku + self.department_curators
        self.cross_department_users = self.users_with_mku_and_curators + self.users_from_other_departments
        self.users_without_curators = self.department_users + self.mku_users + self.users_from_other_departments
        self.curators_and_other_departments = self.department_curators + self.users_from_other_departments

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

    def get_shortened_name(self, option_text):
        parts = option_text.split()
        first_name_initial = parts[1][0]
        last_name = parts[0]
        short_name = f"{first_name_initial}. {last_name}"
        return short_name

    def get_user_position(self, option_text):
        parts = option_text.split('|')
        position = parts[2].strip()
        return position

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

    def click_checkbox(self, checkbox_name):
        self.page.get_by_label(checkbox_name, exact=True).click()

    def click_classifier(self, classifier_name):
        self.page.get_by_role('textbox', name=classifier_name, exact=True).click()

    def assert_krtech_website_opened(self, new_page):
        expect(new_page).to_have_url('https://krtech.ru/')

    def assert_telegram_website_opened(self, new_page):
        expect(new_page).to_have_url('https://t.me/krtech')

    def assert_vkontakte_website_opened(self, new_page):
        expect(new_page).to_have_url('https://vk.com/krtech_crimea')


    def assert_dropdown_list_contain_text(self, search_text):
        options_locator = self.page.locator('role=option')
        expect(options_locator).not_to_have_count(0)
        all_options = options_locator.all()
        for option in all_options:
            expect(option).to_contain_text(search_text, ignore_case=True)

    def assert_dropdown_list_contain_options(self, classifier_name, users_options, fill_field=False):
        if isinstance(users_options, str):
            users_options = [users_options]
        self.click_classifier(classifier_name)
        for user_option in users_options:
            if fill_field:
                search_prefix = user_option[:3]
                self.enter_text_in_the_classifier(classifier_name, search_prefix)
                expect(self.page.get_by_role('option', name=user_option, exact=True)).to_be_visible()
                self.clear_classifier(classifier_name)
            else:
                expect(self.page.get_by_role('option', name=user_option, exact=True)).to_be_visible()

    def assert_dropdown_list_not_contain_options(self, classifier_name, users_options, fill_field=True):
        if isinstance(users_options, str):
            users_options = [users_options]
        self.click_classifier(classifier_name)
        for user_option in users_options:
            if fill_field:
                search_prefix = user_option[:3]
                self.enter_text_in_the_classifier(classifier_name, search_prefix)
                expect(self.page.get_by_role('option', name=user_option, exact=True)).to_be_hidden()
                self.clear_classifier(classifier_name)
            else:
                expect(self.page.get_by_role('option', name=user_option, exact=True)).to_be_hidden()




    def assert_dropdown_list_without_options(self, wait_time=3000):
        options_locator = self.page.locator("role=option")
        self.page.wait_for_timeout(wait_time)
        expect(options_locator).to_have_count(0)
        expect(self._dropdown_list_without_options).to_be_visible()


    def enter_text_in_the_classifier(self, classifier_name, text):
        classifier = self.page.get_by_role('textbox', name=classifier_name)
        classifier.press_sequentially(text, delay=100)

    def clear_classifier(self, classifier_name):
        classifier = self.page.get_by_role('textbox', name=classifier_name, exact=True)
        classifier.clear()