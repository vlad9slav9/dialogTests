from playwright.sync_api import Page
from playwright.sync_api import expect
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
from fields_config import ALL_FIELDS, REQUIRED_FIELDS, FieldType, ClassifierMode, PropertyMode

from mimesis import Generic

from pages.base_page import BasePage
from pages.document_view_page import DocumentViewPage

generic_ru = Generic('ru')


class DocumentEditPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        #self.page = page

        self._outgoing_document_creation_tab = self.page.get_by_role('tab',
                                                                     name='Создание документа (Исходящий (Автотест))',
                                                                     exact=True)
        self._end_date_field = self.page.locator('#endDate')
        self._short_description_field = self.page.locator("textarea[name='description']")
        #self._print_template_field = self.page.get_by_role('textbox', name='Шаблон (для печати)')
        self._print_template_field = self.page.locator('#templateId')
        self._content_editor = self.page.get_by_role('textbox', name='Область редактирования редактора: main')
        self._upper_edit_button = self.page.get_by_role('button').and_(
            page.get_by_title('Сохранить + редактирование (Ctrl+Alt+S)'))
        self._upper_save_button = self.page.get_by_role('button').and_(
            page.get_by_title('Сохранить + просмотр (Ctrl+Alt+S)'))
        self._bottom_edit_button = self.page.get_by_role('button', name='Сохранить + редактировать', exact=True)
        self._bottom_save_button = self.page.get_by_role('button', name='Сохранить + просмотр', exact=True)
        self._error_snackbar = self.page.locator('#notistack-snackbar')
        self._short_description = self.page.locator("textarea[name='description']")
        self.clear_print_template_button = self.page.locator(
            "//label[text() = 'Шаблон (для печати)']//following::button[@title='Clear']")
        self._content_template_field = self.page.locator(".Document-Select").filter(
            has_text="Добавить содержимое из шаблона")

        self._calendar_year_button = self.page.locator('button:has(h6.MuiPickersToolbarText-toolbarTxt)')

        self._prev_month_button = self.page.locator(".MuiPickersCalendarHeader-switchHeader button").nth(0)
        self._next_month_button = self.page.locator(".MuiPickersCalendarHeader-switchHeader button").nth(1)

        self.classifiers_ids = ['office_class_view_docs', 'whom', 'target_department', 'responsible_performer',
                                'users_my_org_test', 'office_class_topics',
                                'office_class_corrs', 'print_font_size_pt']

    def select_option(self, value=None):
        options_locator = self.page.get_by_role('option')
        expect(options_locator).not_to_have_count(0)
        options = options_locator.all()
        if value:
            selected_option = next((option for option in options if value in option.inner_text()), None)
        else:
            selected_option = random.choice(options)
        option_text = selected_option.inner_text()
        selected_option.click()
        return option_text

    def fill_classifier_by_label(self, classifier_label, value):
        group_locator = self.page.get_by_label(f'{classifier_label}')
        group_locator.click()
        self.select_option(value)

    def fill_classifier_by_config(self, classifier_id, config):
        mode = config.get('mode')
        classifier_locator = self.page.locator(f'#{classifier_id} input')
        if mode == ClassifierMode.SINGLE:
            classifier_locator.click()
            selected_value = self.select_option()
            self.assert_field_is_filled(classifier_id, selected_value)
            return selected_value
        elif mode == ClassifierMode.ABBREVIATED:
            classifier_locator.click()
            full_data = self.select_option()
            short_name = self.get_shortened_name(full_data, all_initials=False)
            self.assert_field_is_filled(classifier_id, short_name)
            return short_name
        elif mode == ClassifierMode.MULTI:
            selected_values = []
            for _ in range(2):
                classifier_locator.click()
                selected_values.append(self.select_option())
            self.assert_field_is_filled(classifier_id, selected_values, is_multiform=True)
            return selected_values

    def fill_property_by_config(self, property_id, config):
        mode = config.get('mode')
        property_locator = self.page.locator(f'#{property_id}').locator('input, textarea:visible')
        if mode == PropertyMode.TEXT:
            input_text = generic_ru.text.text()
        elif mode == PropertyMode.NUMBER:
            input_text = self.generate_random_input()
        elif mode == PropertyMode.DATE:
            input_text = self.generate_date_offset_days(0)
        property_locator.fill(input_text)
        self.assert_field_is_filled(property_id, input_text)
        return input_text

    def clear_multivalues_field(self, field_name):
        delete_icons = self.page.locator(f'label:has-text("{field_name}") ~ div .MuiChip-deleteIcon')
        for icon in delete_icons.all()[::-1]:
            icon.click()

    def clear_group_field_by_id(self, field_id):
        clear_locator = self.page.locator(f'#{field_id} [class*="GroupsPicker"] button[aria-label="Clear"]')
        clear_locator.click()

    def assert_field_is_filled(self, field_id, value, is_multiform=False):
        if is_multiform:
            field_locator = self.page.locator(f'#{field_id} .MuiChip-label')
            expect(field_locator).to_have_text(value)
        else:
            field_locator = self.page.locator(f'#{field_id}').locator('input, textarea:visible')
            expect(field_locator).to_have_value(value)

    def assert_field_is_empty(self, field_name):
        expect(self.page.get_by_label(field_name, exact=True)).to_be_empty()

    def assert_group_and_field_is_empty(self, container_id):
        expect(self.page.locator(f'#{container_id} [class*="GroupsPicker"] input')).to_be_empty()
        expect(self.page.locator(f'#{container_id} .MuiChip-root')).to_have_count(0)

    def fill_date_property(self, date_property_name, input_date=None):
        date_property_locator = self.page.get_by_label(date_property_name, exact=True)
        if input_date:
            date_property_locator.fill(input_date)
        else:
            input_date = self.generate_date_offset_days(0)
            date_property_locator.fill(input_date)

        return input_date

    def clear_property(self, prop_name):
        prop_locator = self.page.get_by_label(prop_name, exact=True)
        prop_locator.clear()

    def change_date_in_property(self, prop_name, date_offset):
        self.clear_property(prop_name)
        new_date = self.generate_date_offset_days(date_offset)
        self.fill_date_property(prop_name, new_date)
        self.assert_field_is_filled(prop_name, new_date)

    def click_field_calendar(self, property_name):
        button = self.page.locator(f"//label[text() = '{property_name}']/following::button[1]")
        button.click()

    def change_date_via_calendar(self, property_name, future_date=True, is_year=False):
        delta = relativedelta(days=1, months=1, years=1)
        new_date = datetime.today() + delta if future_date else datetime.today() - delta
        self.click_field_calendar(property_name)
        if is_year:
            self.page.locator('.MuiPickersYear-root').get_by_text(new_date.strftime('%Y')).click()
            return new_date.strftime('%Y')
        self._calendar_year_button.click()
        self.page.locator('.MuiPickersYear-root').get_by_text(new_date.strftime('%Y')).click()
        self._next_month_button.click() if future_date else self._prev_month_button.click()
        self.page.locator('.MuiPickersDay-day').get_by_text(new_date.strftime('%d')).first.click()
        return new_date.strftime('%d.%m.%Y')

    def fill_short_description(self, value=None):
        if value:
            self._short_description.fill(value)
        else:
            value = generic_ru.text.text()
            self._short_description.fill(value)
        return value

    def assert_short_description_has_value(self, value):
        expect(self._short_description_field).to_have_value(value)

    def fill_content_editor(self, text=None):
        if text:
            self._content_editor.fill(text)
        else:
            text = generic_ru.text.text()
            self._content_editor.fill(text)

        return text

    def clear_content_editor(self):
        self._content_editor.clear()

    def assert_content_editor_has_value(self, value):
        expect(self._content_editor).to_have_text(value)

    def select_content_template(self, template_name):
        self._content_template_field.click()
        self.page.get_by_role("option", name=f"{template_name}").click()

    def clear_print_template(self):
        self._print_template_field.hover()
        self.clear_print_template_button.click()

    def change_print_template(self, entered_text):
        self.clear_print_template()
        self._print_template_field.click()
        self._print_template_field.press_sequentially(f'{entered_text}')
        self.assert_dropdown_list_contain_text(f'{entered_text}')
        options_locator = self.page.get_by_role('option', name=f'{entered_text}')
        options_locator.click()

    def assert_checkbox_checked(self, checkbox_id):
        expect(self.page.locator(f'#{checkbox_id} input[type="checkbox"]')).to_be_checked()

    def assert_checkbox_not_checked(self, checkbox_id):
        expect(self.page.locator(f'#{checkbox_id} input[type="checkbox"]')).not_to_be_checked()

    # def check_not_default_checkboxes(self):
    #     self.click_checkbox('Контроль УК')
    #     self.assert_checkbox_checked('Контроль УК')
    #
    #     self.click_checkbox('Контроль УК ФЦП')
    #     self.assert_checkbox_checked('Контроль УК ФЦП')
    #
    #     self.click_checkbox('Срочный')
    #     self.assert_checkbox_checked('Срочный')
    #
    #     self.click_checkbox('Для МЭДО')
    #     self.assert_checkbox_checked('Для МЭДО')

    def fill_all_not_default_fields(self):
        filled_fields = {}
        for field_id, config in ALL_FIELDS.items():
            field_type = config['type']
            if field_type == FieldType.CLASSIFIER:
                selected_value = self.fill_classifier_by_config(field_id, config)
            elif field_type == FieldType.PROPERTY:
                selected_value = self.fill_property_by_config(field_id, config)
            else:
                raise ValueError(f'Неизвестный тип поля: {field_type}')
            filled_fields[field_id] = selected_value

        self.fill_short_description()
        self.fill_content_editor()

    def click_upper_edit_button(self):
        self._upper_edit_button.click()

    def click_upper_save_button(self):
        self._upper_save_button.click()

    def click_bottom_edit_button(self):
        self._bottom_edit_button.click()

    def click_bottom_save_button(self):
        self._bottom_save_button.click()

    def assert_document_creation_tab_visible(self, document_name):
        locator = self.page.get_by_role('tab', name=f'Создание документа ({document_name})', exact=True)
        expect(locator).to_be_visible()

    def assert_default_fields_are_filled(self, user_information, return_values=False):
        end_date = self.generate_date_offset_days(14)
        expect(self._end_date_field).to_have_value(end_date)

        current_date = self.generate_date_offset_days()
        self.assert_field_is_filled('date_doc', current_date)

        self.assert_field_is_filled('date_from', current_date)

        current_year = self.generate_date_offset_days(0, year=True)
        self.assert_field_is_filled('date_year', current_year)

        self.assert_field_is_filled('from', user_information, is_multiform=True)

        self.assert_checkbox_checked('show_signature')
        self.assert_checkbox_checked('show_author')

        expect(self._print_template_field).to_have_value('Первый автотестовый шаблон')

        if return_values:
            return {
                'end_date': end_date,
                'date_doc': current_date,
                'date_from': current_date,
                'from': user_information.rsplit(' | ', 1)[0],
                'date_year': current_year
            }

    def assert_snackbar_displayed(self, notification_text):
        expect(self._error_snackbar).to_have_text(notification_text)

    def assert_required_field_error_displayed(self, error_text):
        locator = self.page.locator("p.MuiFormHelperText-root", has_text=error_text)
        expect(locator).to_be_visible()

    def assert_content_editor_has_text(self, text):
        self.assert_content_editor_has_value(text)

    def assert_content_editor_is_empty(self):
        expect(self._content_editor).to_be_empty()

    def assert_picker_contain_users(self, classifier_name, users_values, fill_field=True):
        self.assert_dropdown_list_contain_options(classifier_name, users_values, fill_field=fill_field)

    def assert_picker_not_contain_users(self, classifier_name, users_values, fill_field=True):
        self.assert_dropdown_list_not_contain_options(classifier_name, users_values, fill_field=fill_field)

    def assert_document_tab_visible(self, tab_name):
        expect(self.page.get_by_role('tab', name=tab_name)).to_be_visible()

    def create_regular_document(self, user_information, all_fields=False):
        if all_fields:
            filled_fields = {**self.assert_default_fields_are_filled(user_information, return_values=True),
                             **self.fill_all_not_default_fields(return_values=True)}
            self.click_upper_save_button()
            self.assert_document_tab_visible('Документ №')
            #expect(self.page.get_by_role('tab', name='Документ №')).to_be_visible()
            return DocumentViewPage(self.page), filled_fields
        else:
            filled_fields = {**self.assert_default_fields_are_filled(user_information, return_values=True),
                             **self.fill_all_not_default_fields()}
            self.click_bottom_save_button()
            self.assert_document_tab_visible('Документ №')
            #expect(self.page.get_by_role('tab', name='Документ №')).to_be_visible()
            return DocumentViewPage(self.page), filled_fields

    def test_example(self, user_information):

        self.fill_all_not_default_fields()
        #self.assert_default_fields_are_filled(user_information)

        # meeting = self.fill_multiform('document_type_field_meeting_region')
        # self.assert_multiform_is_filled('document_type_field_meeting_region', meeting)
        #
        #
        # tematics = self.fill_classifier('office_class_topics')
        # self.assert_property_filled('office_class_topics', tematics)
        #
        #
        # by_attorney = self.fill_property('by_attorney')
        # self.assert_property_filled('by_attorney', by_attorney)
        #
        #
        # document_type = self.fill_property('doc_type')
        # self.assert_property_filled('doc_type', document_type)
