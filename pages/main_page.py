
from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.base_page import BasePage
from datetime import datetime
import locale

from pages.document_сreation_page import DocumentCreationPage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._profile_button = self.page.get_by_role("button").and_(page.get_by_title("Профиль"))
        self._logout_button = self.page.get_by_role("button").and_(page.get_by_title("Выход"))

        #self._profile_button = self.page.locator('button[title="Профиль"]')
        #self._logout_button = self.page.locator('button[title = "Выход"]')
        self._logout_confirmation_button = self.page.get_by_role("button", name="Выйти")
        self._cancel_logout_button = self.page.get_by_role("button", name="Отмена")
        self._sidebar = self.page.locator(".PageSidebar")
        self._hide_sidebar_button = self.page.get_by_role("button", name="Скрыть меню")
        self._open_sidebar_button = self.page.get_by_role("button", name="Открыть меню")
        self._home_button = self.page.get_by_role("button", name="На главную")
        self._event_container = self.page.locator(".EventContainer")
        self._quick_document_creation_button = self.page.locator(".DocumentCreateModal > .MuiButtonBase-root")
        self._add_animal_card_button = self.page.get_by_role("button", name="Добавить карточку животного")
        self._quick_search_button = self.page.locator(".DocumentQuickSearchAutocomplete-SearchButton")
        self._support_service_button = self.page.get_by_role("button", name="Служба поддержки (Ctrl+Alt+2)")
        self._reference_materials_button = self.page.get_by_role("button", name="Справочные материалы")
        self._displayed_date = self.page.locator(".style_date__TlIM3")
        self._displayed_time = self.page.locator(".style_time__RaPtf")
        self._document_type_search_field = self.page.get_by_role("textbox", name="Выберите тип документа")
        self._document_type_selection_button = self.page.get_by_role("button", name="Open")
        self._document_type_search_field_clear_button = self.page.get_by_role("button", name="Clear")
        self._incoming_document_option = self.page.get_by_role("option", name="Входящий (Автотест)")
        self._outgoing_document_option = self.page.get_by_role("option", name="Исходящий (Автотест)")
        self._outgoing_medo_document_option = self.page.get_by_role("option", name="Исходящий МЭДО (Автотест)")
        self._internal_document_option = self.page.get_by_role("option", name="Внутренний (Без Шаблона Печати) Автотест")
        self._create_document_button = self.page.get_by_role("button", name="Создать")
        self._cancel_document_creation_window_button = self.page.get_by_role("button", name="Отмена")
        self._close_document_creation_window_button = self.page.get_by_role("button", name="close")
        self._document_creation_window = self.page.get_by_role("dialog", name="Быстрое создание документа")



    def click_profile_button(self):
        self._profile_button.click()

    def click_logout_button(self):
        self._logout_button.click()

    def click_logout_confirmation_button(self):
        self._logout_confirmation_button.click()

    def click_cancel_logout_button(self):
        self._cancel_logout_button.click()

    def click_hide_sidebar_button(self):
        self._hide_sidebar_button.click()

    def click_open_sidebar_button(self):
        self._open_sidebar_button.click()

    def click_home_button(self):
        self._home_button.click()

    def click_quick_document_creation_button(self):
        self._quick_document_creation_button.click()

    def click_cancel_document_creation_button(self):
        self._cancel_document_creation_window_button.click()

    def click_close_document_creation_button(self):
        self._close_document_creation_window_button.click()

    def click_document_type_search_field_clear_button(self):
        self._document_type_search_field_clear_button.click()

    def click_document_type_selection_button(self):
        self._document_type_selection_button.click()

    def click_document_type_selection_field(self):
        self._document_type_search_field.click()

    def click_outgoing_document_option(self):
        self._outgoing_document_option.click()

    def click_incoming_document_option(self):
        self._incoming_document_option.click()

    def click_internal_document_option(self):
        self._internal_document_option.click()

    def click_outgoing_medo_document_option(self):
        self._outgoing_medo_document_option.click()

    def enter_document_type_in_field(self, document_type):
        self._document_type_search_field.fill(document_type)

    def select_outgoing_document_type(self):
        self.click_document_type_selection_button()
        self.click_outgoing_document_option()

    def select_incoming_document_type(self):
        self.click_document_type_selection_button()
        self.click_incoming_document_option()

    def select_outgoing_medo_document_type(self):
        self.enter_document_type_in_field("исходящий мэдо")
        self.click_outgoing_medo_document_option()

    def select_internal_document_type(self):
        self.enter_document_type_in_field("внутренний")
        self.click_internal_document_option()

    def open_outgoing_document_creation_page(self):
        self._quick_document_creation_button.click()
        self.select_outgoing_document_type()
        self._create_document_button.click()
        return DocumentCreationPage(self.page)

    '''def get_user_data(self, data_name):
        self.click_profile_button()
        user_data_locator = self.page.locator(f'p.MuiTypography-root.MuiTypography-body1:has(strong:text("{data_name}"))')
        user_data = user_data_locator.inner_text().split(':')[-1].strip()
        return user_data'''

    def get_basic_user_information(self):
        user_fio = self.get_user_data("Ф.И.О.")
        user_organization = self.get_user_data("Организация")
        user_position = self.get_user_data("Должность")

        return f"{user_fio} | {user_organization} | {user_position}"





    def assert_profile_button_visible(self):
        expect(self._profile_button).to_be_visible()

    def assert_sidebar_visible(self):
        expect(self._sidebar).to_be_visible()

    def assert_sidebar_hidden(self):
        expect(self._sidebar).to_be_hidden()

    def assert_event_container_visible(self):
        expect(self._event_container).to_be_visible()

    def assert_displayed_date(self):
        locale.setlocale(locale.LC_TIME, "ru_RU")
        expected_date = datetime.now().strftime("%A, %d.%m.%Y").capitalize()
        expect(self._displayed_date).to_have_text(expected_date)

    def assert_displayed_time(self):
        expected_time = datetime.now().strftime("%H:%M")
        expect(self._displayed_time).to_contain_text(expected_time)

    def assert_document_creation_window_visible(self):
        expect(self._document_creation_window).to_be_visible()

    def assert_document_creation_window_hidden(self):
        expect(self._document_creation_window).to_be_hidden()

    def assert_create_document_button_disabled(self):
        expect(self._create_document_button).to_be_disabled()

    def assert_create_document_button_enabled(self):
        expect(self._create_document_button).to_be_enabled()

    def assert_outgoing_document_option_visible(self):
        expect(self._outgoing_document_option).to_be_visible()

    def assert_outgoing_document_option_hidden(self):
        expect(self._outgoing_document_option).to_be_hidden()

    def assert_outgoing_medo_document_option_visible(self):
        expect(self._outgoing_medo_document_option).to_be_visible()

    def assert_outgoing_medo_document_option_hidden(self):
        expect(self._outgoing_medo_document_option).to_be_hidden()

    def assert_incoming_document_option_visible(self):
        expect(self._incoming_document_option).to_be_visible()

    def assert_incoming_document_option_hidden(self):
        expect(self._incoming_document_option).to_be_hidden()

    def assert_internal_document_option_visible(self):
        expect(self._internal_document_option).to_be_visible()

    def assert_internal_document_option_hidden(self):
        expect(self._internal_document_option).to_be_hidden()

    def assert_outgoing_document_option_selected(self):
        expect(self._document_type_search_field).to_have_value("Исходящий (Автотест)")

    def assert_incoming_document_option_selected(self):
        expect(self._document_type_search_field).to_have_value("Входящий (Автотест)")

    def assert_internal_document_option_selected(self):
        expect(self._document_type_search_field).to_have_value("Внутренний (Без Шаблона Печати) Автотест")

    def assert_outgoing_medo_document_option_selected(self):
        expect(self._document_type_search_field).to_have_value("Исходящий МЭДО (Автотест)")

    def assert_document_type_search_field_empty(self):
        expect(self._document_type_search_field).to_be_empty()