import logging

from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.base_page import BasePage
from datetime import datetime
import locale


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._responsible_profile_button = self.page.get_by_role("button", name="Девятый Д.Д")
        self._logout_button = self.page.locator('[title = "Выход"]')
        self._confirm_logout_button = self.page.get_by_role("button", name="Выйти")
        self._cancel_logout_button = self.page.get_by_role("button", name="Отмена")
        self._sidebar = self.page.locator(".PageSidebar")
        self._hide_sidebar_button = self.page.get_by_role("button", name="Скрыть меню")
        self._open_sidebar_button = self.page.get_by_role("button", name="Открыть меню")
        self._home_button = self.page.get_by_role("button", name="На главную")
        self._event_container = self.page.locator(".EventContainer")
        self._quick_create_document_button = self.page.locator(".DocumentCreateModal")
        self._add_animal_card_button = self.page.get_by_role("button", name="Добавить карточку животного")
        self._quick_search_button = self.page.locator(".DocumentQuickSearchAutocomplete-SearchButton")
        self._support_service_button = self.page.get_by_role("button", name="Служба поддержки (Ctrl+Alt+2)")
        self._reference_materials_button = self.page.get_by_role("button", name="Справочные материалы")
        self._displayed_date = self.page.locator(".style_date__TlIM3")
        self._displayed_time = self.page.locator(".style_time__RaPtf")
        self._document_type_search_field = self.page.get_by_label("Выберите тип документа")
        self._document_type_select_button = self.page.get_by_role("button", name="Open")
        self._clear_document_type_search_field_button = self.page.get_by_role("button", name="Clear")
        self._incoming_document_option = self.page.get_by_role("option", name="Входящий (Автотест)")
        self._outgoing_document_option = self.page.get_by_role("option", name="Исходящий (Автотест)")
        self._outgoing_MEDO_document_option = self.page.get_by_role("option", name="Исходящий МЭДО (Автотест)")
        self._internal_document_option = self.page.get_by_role("option", name="Внутренний (Без Шаблона Печати) Автотест")
        self._create_document_button = self.page.get_by_role("button", name="Создать")
        self._cancel_create_document_window_button = self.page.get_by_role("button", name="Отмена")
        self._close_create_document_window_button = self.page.get_by_label("close")
        self._quick_create_document_window = self.page.get_by_label("Быстрое создание документа")

    def click_responsible_profile_button(self):
        self._responsible_profile_button.click()

    def click_logout_button(self):
        self._logout_button.click()

    def click_confirm_logout_button(self):
        self._confirm_logout_button.click()

    def click_cancel_logout_button(self):
        self._cancel_logout_button.click()

    def click_hide_sidebar_button(self):
        self._hide_sidebar_button.click()

    def click_open_sidebar_button(self):
        self._open_sidebar_button.click()

    def click_home_button(self):
        self._home_button.click()

    def click_quick_create_document_button(self):
        self._quick_create_document_button.click()

    def click_cancel_create_document_button(self):
        self._cancel_create_document_window_button.click()

    def click_close_create_document_button(self):
        self._close_create_document_window_button.click()

    def click_clear_document_type_search_field_button(self):
        self._clear_document_type_search_field_button.click()

    def select_outgoing_document_type(self):
        self._document_type_select_button.click()
        self._outgoing_document_option.click()

    def select_incoming_document_type(self):
        self._document_type_select_button.click()
        self._incoming_document_option.click()

    def select_outgoing_MEDO_document_type(self):
        self._document_type_search_field.fill("исходящий мэдо")
        self._outgoing_MEDO_document_option.click()

    def select_internal_document_type(self):
        self._document_type_search_field.fill("внутренний")
        self._internal_document_option.click()

    def enter_document_type_in_field(self, document_type):
        self._document_type_search_field.fill(document_type)







    def assert_responsible_profile_button_visible(self):
        expect(self._responsible_profile_button).to_be_visible()

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

    def assert_create_document_window_opened(self):
        expect(self._quick_create_document_window).to_be_visible()

    def assert_create_document_window_hidden(self):
        expect(self._quick_create_document_window).to_be_hidden()

    def assert_create_document_button_disabled(self):
        expect(self._create_document_button).to_be_disabled()

    def assert_create_document_button_enabled(self):
        expect(self._create_document_button).to_be_enabled()




    def assert_outgoing_document_visible(self):
        expect(self._outgoing_document_option).to_be_visible()

    def assert_outgoing_document_hidden(self):
        expect(self._outgoing_document_option).to_be_hidden()

    def assert_outgoing_MEDO_document_visible(self):
        expect(self._outgoing_MEDO_document_option).to_be_visible()

    def assert_outgoing_MEDO_document_hidden(self):
        expect(self._outgoing_MEDO_document_option).to_be_hidden()

    def assert_incoming_document_visible(self):
        expect(self._incoming_document_option).to_be_visible()

    def assert_incoming_document_hidden(self):
        expect(self._incoming_document_option).to_be_hidden()

    def assert_internal_document_visible(self):
        expect(self._internal_document_option).to_be_visible()

    def assert_internal_document_hidden(self):
        expect(self._internal_document_option).to_be_hidden()