import locale
from datetime import datetime

from playwright.sync_api import Page, expect


class LayoutComponent:
    def __init__(self, page: Page):
        self.page = page

        # Профиль и авторизация
        self._profile_button = self.page.locator('button[title="Профиль"]')
        self._logout_button = self.page.locator('button[title="Выход"]')
        self._logout_confirm_button = self.page.get_by_role("button", name="Выйти")
        self._cancel_logout_button = self.page.get_by_role("button", name="Отмена")

        # Сайдбар и навигация
        self._sidebar = self.page.locator(".PageSidebar")
        self._hide_sidebar_button = self.page.get_by_role("button", name="Скрыть меню")
        self._open_sidebar_button = self.page.get_by_role("button", name="Открыть меню")
        self._home_button = self.page.get_by_role("button", name="На главную")

        # Отображение даты и времени в каркасе
        self._displayed_date = self.page.locator(".style_date__TlIM3")
        self._displayed_time = self.page.locator(".style_time__RaPtf")

        # Сервисные кнопки каркаса
        self._quick_search_button = self.page.locator(
            ".DocumentQuickSearchAutocomplete-SearchButton"
        )
        self._support_service_button = self.page.get_by_role(
            "button", name="Служба поддержки (Ctrl+Alt+2)"
        )
        self._reference_materials_button = self.page.get_by_role(
            "button", name="Справочные материалы"
        )

        # Модальное окно быстрого создания документа
        self._quick_doc_create_button = self.page.locator(
            ".DocumentCreateModal > .MuiButtonBase-root"
        )
        self._doc_create_window = self.page.get_by_role(
            "dialog", name="Быстрое создание документа"
        )
        self._doc_type_search_field = self.page.get_by_role(
            "textbox", name="Выберите тип документа"
        )
        self._doc_type_select_button = self.page.get_by_role("button", name="Open")
        self._doc_type_search_field_clear_button = self.page.get_by_role(
            "button", name="Clear"
        )
        self._create_doc_button = self.page.get_by_role("button", name="Создать")
        self._cancel_doc_create_window_button = self.page.get_by_role(
            "button", name="Отмена"
        )
        self._close_doc_create_window_button = self.page.get_by_role(
            "button", name="close"
        )

    # Действия с профилем и выходом
    def click_profile_button(self):
        self._profile_button.click()

    def click_logout_button(self):
        self._logout_button.click()

    def click_logout_confirm_button(self):
        self._logout_confirm_button.click()

    def click_cancel_logout_button(self):
        self._cancel_logout_button.click()

    def get_user_data(self, data_name: str) -> str:
        user_data_locator = self.page.locator(
            f'p.MuiTypography-root.MuiTypography-body1:has(strong:text("{data_name}"))'
        )
        return user_data_locator.inner_text().split(":")[-1].strip()

    def get_basic_user_information(self) -> str:
        self.click_profile_button()
        user_fio = self.get_user_data("Ф.И.О.")
        user_organization = self.get_user_data("Организация")
        user_position = self.get_user_data("Должность")
        return f"{user_fio} | {user_organization} | {user_position}"

    # Действия с сайдбаром и меню
    def click_hide_sidebar_button(self):
        self._hide_sidebar_button.click()

    def click_open_sidebar_button(self):
        self._open_sidebar_button.click()

    def click_home_button(self):
        from pages.event_page import EventPage

        self._home_button.click()
        return EventPage(self.page)

    # Действия с модальным окном создания документа
    def click_quick_doc_create_button(self):
        self._quick_doc_create_button.click()

    def click_cancel_doc_create_button(self):
        self._cancel_doc_create_window_button.click()

    def click_close_doc_create_button(self):
        self._close_doc_create_window_button.click()

    def click_doc_type_search_field_clear_button(self):
        self._doc_type_search_field_clear_button.click()

    def click_doc_type_select_button(self):
        self._doc_type_select_button.click()

    def click_doc_type_select_field(self):
        self._doc_type_search_field.click()

    def click_doc_option(self, doc_option: str):
        self.page.get_by_role("option", name=doc_option, exact=True).click()

    def fill_doc_type_search_field(self, doc_type: str):
        self._doc_type_search_field.fill(doc_type)

    def select_doc_type(self, doc_option: str):
        self.click_doc_option(doc_option)

    def open_doc_edit_page(self, doc_type: str):
        from pages.document_edit_page import DocumentEditPage

        self._quick_doc_create_button.click()
        self.click_doc_type_select_field()
        self.select_doc_type(doc_type)
        with self.page.expect_response(
            lambda res: "/template" in res.url and res.status == 200
        ) as response_info:
            self._create_doc_button.click()
        doc_edit_page = DocumentEditPage(self.page)
        doc_edit_page.template_data = response_info.value.json()
        return doc_edit_page

    # def create_and_open_document(
    #     self, doc_type: str = "Исходящий (Автотест)", user_info: str = None
    # ):
    #     """Хелпер-фасад: открывает страницу создания и сразу создает документ."""
    #     if not user_info:
    #         user_info = self.get_basic_user_information()
    #     doc_edit_page = self.open_doc_create_page(doc_type)
    #     return doc_edit_page.create_document(user_info)

    # Проверки (Assertions)
    def assert_profile_button_visible(self):
        expect(self._profile_button).to_be_visible()

    def assert_sidebar_visible(self):
        expect(self._sidebar).to_be_visible()

    def assert_sidebar_hidden(self):
        expect(self._sidebar).to_be_hidden()

    def assert_displayed_date(self):
        locale.setlocale(locale.LC_TIME, "ru_RU")
        expected_date = datetime.now().strftime("%A, %d.%m.%Y").capitalize()
        expect(self._displayed_date).to_have_text(expected_date)

    def assert_displayed_time(self):
        expected_time = datetime.now().strftime("%H:%M")
        expect(self._displayed_time).to_contain_text(expected_time)

    def assert_doc_create_window_visible(self):
        expect(self._doc_create_window).to_be_visible()

    def assert_doc_create_window_hidden(self):
        expect(self._doc_create_window).to_be_hidden()

    def assert_create_doc_button_disabled(self):
        expect(self._create_doc_button).to_be_disabled()

    def assert_create_doc_button_enabled(self):
        expect(self._create_doc_button).to_be_enabled()

    def assert_doc_option_selected(self, doc_type_text: str):
        expect(self._doc_type_search_field).to_have_value(doc_type_text)

    def assert_doc_type_search_field_is_empty(self):
        expect(self._doc_type_search_field).to_be_empty()
