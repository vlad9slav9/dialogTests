from playwright.sync_api import Page
from playwright.sync_api import expect
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

from mimesis import Generic

from pages.base_page import BasePage
from pages.document_view_page import DocumentViewPage

generic = Generic('ru')


class DocumentCreationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self._outgoing_document_creation_tab = self.page.get_by_role('tab',
                                                                     name='Создание документа (Исходящий (Автотест))',
                                                                     exact=True)
        self._end_date_field = self.page.locator('#endDate')
        self._short_description_field = self.page.locator("textarea[name='description']")
        self._print_template_field = self.page.get_by_role('textbox', name='Шаблон (для печати)')
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

        self.group_with_organizations_from_admin = ["Министерство сэд 2.0", 'Аппарат Совета министров Республики Крым',
                                                    'Министерство Тестирования РК']
        self.group_with_organizations_from_profile = ['Тестовая Организация 999', 'МКУ Автотестовое']


        self._calendar_year_button = self.page.locator('button:has(h6.MuiPickersToolbarText-toolbarTxt)')

        self._prev_month_button = self.page.locator(".MuiPickersCalendarHeader-switchHeader button").nth(0)
        self._next_month_button = self.page.locator(".MuiPickersCalendarHeader-switchHeader button").nth(1)

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
        return self.normalize_spaces(option_text)


    def fill_classifier(self, classifier_name, is_multiform=False, option_value=None):
        classifier = self.page.get_by_label(classifier_name, exact=True)
        if is_multiform:
            selected_values = []
            for _ in range(2):
                classifier.click()
                selected_values.append(self.select_option(option_value))
            return selected_values
        else:
            classifier.click()
            return self.select_option(option_value)

    def fill_textarea(self, area_name, input_text=None):
        textarea_locator = self.page.locator(f"fieldset:has(legend:has-text('{area_name}')) textarea.PropsTextArea-Autosize").first
        if input_text:
            textarea_locator.fill(input_text)
        else:
            input_text = generic.text.text()
            textarea_locator.fill(input_text)

        return input_text

    def fill_property(self, property_name, input_text=None):
        property_locator = self.page.get_by_label(property_name, exact=True)
        if input_text:
            property_locator.fill(input_text)
        else:
            input_text = generic.text.word()
            #input_text = self.generate_random_string_with_all_symbols()
            property_locator.fill(input_text)

        return input_text

    def clear_multivalues_field(self, field_name):
        delete_icons = self.page.locator(f'label:has-text("{field_name}") ~ div .MuiChip-deleteIcon')
        for icon in delete_icons.all()[::-1]:
            icon.click()

    def assert_field_is_filled(self, field_name, value, is_multivalues=False):
        value = self.normalize_spaces(value)
        if is_multivalues:
            if isinstance(value, str):
                value = [value]
            field_container = self.page.locator(f"label:has-text('{field_name}') ~ .MuiInputBase-root")

            for text in value:
                button = field_container.get_by_role("button", name=self.normalize_spaces(text))
                expect(button).to_be_visible()
        else:
            expect(self.page.get_by_label(field_name, exact=True)).to_have_value(self.normalize_spaces(value))

    def assert_field_is_empty(self, field_name):
        expect(self.page.get_by_label(field_name, exact=True)).to_be_empty()

    def assert_textarea_has_value(self, area_name, value_text):
        textarea_locator = self.page.locator(f"fieldset:has(legend:has-text('{area_name}')) textarea.PropsTextArea-Autosize").first
        expect(textarea_locator).to_have_value(value_text)

    #def assert_multivalues_field_has_value(self, field_name, buttons_name):
    #    if isinstance(buttons_name, str):
    #        buttons_name = [buttons_name]

    #    field_container = self.page.locator(f"label:has-text('{field_name}') ~ .MuiInputBase-root")

    #    for text in buttons_name:
    #        button = field_container.get_by_role("button", name=text)
    #        expect(button).to_be_visible()

    def assert_field_has_short_name(self, classifier_name, full_name, all_initial=True):
        short_name = self.get_shortened_name(full_name, all_initial)
        expect(self.page.get_by_label(classifier_name, exact=True)).to_have_value(short_name)

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
            value = generic.text.text()
            self._short_description.fill(value)
        return value

    def assert_short_description_has_value(self, value):
        expect(self._short_description_field).to_have_value(value)

    def fill_content_editor(self, text=None):
        if text:
            self._content_editor.fill(text)
        else:
            text = generic.text.text()
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
        self._print_template_field.press_sequentially(f'{entered_text}', delay=100)
        self.assert_dropdown_list_contain_text(f'{entered_text}')
        options_locator = self.page.get_by_role('option', name=f'{entered_text}')
        options_locator.click()

    def assert_checkbox_checked(self, checkbox_name):
        expect(self.page.get_by_label(checkbox_name, exact=True)).to_be_checked()

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

    def fill_required_fields(self, return_content=True):

        document_type = self.fill_property('Тип документа *')
        self.assert_field_is_filled('Тип документа *', document_type)

        document_view = self.fill_classifier('Вид документа *')
        self.assert_field_is_filled('Вид документа *', document_view)

        short_description = self.fill_short_description()
        self.assert_short_description_has_value(short_description)

        if return_content:
            return {
                'Тип документа': document_type,
                'Вид документа': document_view,
                'Краткое описание:': short_description
            }

    def fill_all_not_default_fields(self, return_values=False):
        document_type = self.fill_property('Тип документа *')
        self.assert_field_is_filled('Тип документа *', document_type)

        document_view = self.fill_classifier('Вид документа *')
        self.assert_field_is_filled('Вид документа *', document_view)

        document_number = self.fill_property('№ документа')
        self.assert_field_is_filled('№ документа', document_number)

        link_to_number = self.fill_property('Ссылается на № (для печати)')
        self.assert_field_is_filled('Ссылается на № (для печати)', link_to_number)

        reference_date = self.fill_date_property('Дата документа на который ссылаемся (для печати)')
        self.assert_field_is_filled('Дата документа на который ссылаемся (для печати)', reference_date)

        whom = self.fill_classifier('Кому')
        self.assert_field_is_filled('Кому', whom)

        addressee = self.fill_classifier('Адресат')
        self.assert_field_is_filled('Адресат', addressee)

        responsible_performer = self.fill_classifier('Ответственный исполнитель')
        self.assert_field_is_filled('Ответственный исполнитель', responsible_performer)

        organizations_group = self.fill_classifier("Выберите группу", option_value="Группа из профиля")
        self.assert_field_is_filled("Выберите группу", organizations_group)
        self.assert_field_is_filled('Адресат-организация после подписания (не более 10)',
                                    self.group_with_organizations_from_profile, is_multivalues=True)

        signatory_name = self.fill_classifier('Подпись')
        signatory_position = self.extract_user_parts(signatory_name, parts='position')
        self.assert_field_has_short_name('Подпись', signatory_name, all_initial=False)
        self.assert_field_is_filled('Должность', signatory_position)

        coordinator_data = self.fill_classifier('Имя согласователя')
        coordinator_position = self.extract_user_parts(coordinator_data, parts='position')
        self.assert_field_has_short_name('Имя согласователя', coordinator_data, all_initial=False)
        self.assert_textarea_has_value('Должность согласователя', coordinator_position)

        test_number = self.fill_property('Число', '1234567890')
        self.assert_field_is_filled('Число', test_number)

        users_group = self.fill_classifier("Добавить из группы", option_value="Пользователи моей организации")
        self.assert_field_is_filled('Добавить из группы', users_group)
        self.assert_field_is_filled('Получатели после подписания', self.department_users, is_multivalues=True)

        my_organization_user = self.fill_classifier('Пользователи своей орги')
        self.assert_field_is_filled('Пользователи своей орги', my_organization_user)

        topic = self.fill_classifier('Тематика')
        self.assert_field_is_filled('Тематика', topic)

        correspondent = self.fill_classifier('Корреспондент')
        self.assert_field_is_filled('Корреспондент', correspondent)

        meeting_company = self.fill_classifier('Встреча с коллективами предприятий', is_multiform=True)
        self.assert_field_is_filled('Встреча с коллективами предприятий', meeting_company, is_multivalues=True)

        meeting_place = self.fill_classifier('Выездные совещания', is_multiform=True)
        self.assert_field_is_filled('Выездные совещания', meeting_place, is_multivalues=True)

        print_font_size = self.fill_classifier('Размер шрифта(при печати)')
        self.assert_field_is_filled('Размер шрифта(при печати)', print_font_size)

        document_information = self.fill_textarea('Информация о документе')
        self.assert_textarea_has_value('Информация о документе', document_information)

        short_description = self.fill_short_description()
        self.assert_short_description_has_value(short_description)

        content = self.fill_content_editor()
        self.assert_content_editor_has_value(content)

        if return_values:
            return {
                'Тип документа': document_type,
                'Вид документа': document_view,
                '№ документа': document_number,
                'Ссылается на № (для печати)': link_to_number,
                'Дата документа на который ссылаемся (для печати)': reference_date,
                'Кому': self.extract_user_parts(whom, parts=['fio', 'organization']),
                'Адресат': addressee,
                'Ответственный исполнитель': self.extract_user_parts(responsible_performer,
                                                                     parts=['fio', 'organization']),
                'Адресат-организация после подписания (не более 10)': self.group_with_organizations_from_profile,
                'Подпись': self.get_shortened_name(signatory_name, all_initials=False),
                'Должность': signatory_position,
                'Имя согласователя': self.get_shortened_name(coordinator_data, all_initials=False),
                'Должность согласователя': coordinator_position,
                'Число': test_number,
                'Получатели после подписания': self.get_shortened_name(self.department_users),
                'Пользователи своей орги': self.get_shortened_name(my_organization_user),
                'Тематика': topic,
                'Корреспондент': correspondent,
                'Встреча с коллективами предприятий': meeting_company,
                'Выездные совещания': meeting_place,
                'Размер шрифта(при печати)': print_font_size,
                'Информация о документе': document_information,
                'Краткое описание:': short_description,
                'Содержимое:': content
            }

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
        self.assert_field_is_filled('Срок исполнения *', end_date)

        current_date = self.generate_date_offset_days()
        self.assert_field_is_filled('Дата документа *', current_date)

        self.assert_field_is_filled('Дата от', current_date)

        current_year = self.generate_date_offset_days(0, year=True)
        self.assert_field_is_filled('Год', current_year)

        self.assert_field_is_filled('От кого', user_information, is_multivalues=True)

        self.assert_checkbox_checked('Отображать ЭП при печати')
        self.assert_checkbox_checked('Отображать автора и номер телефона на последней странице')

        self.assert_field_is_filled('Шаблон (для печати) *', 'Первый автотестовый шаблон')

        if return_values:
            return {
                'Срок исполнения': end_date,
                'Дата документа': current_date,
                'От кого': user_information.rsplit(' | ', 1)[0],
                'Год': current_year,
                'Дата от': current_date
            }

    def assert_snackbar_displayed(self, notification_text):
        expect(self._error_snackbar).to_have_text(notification_text)

    def assert_required_field_error_displayed(self, error_text):
        locator = self.page.locator("p.MuiFormHelperText-root", has_text=error_text)
        expect(locator).to_be_visible()

    def assert_content_editor_has_first_template(self):
        self.assert_content_editor_has_value('Автотест для проверки добавления первого шаблона содержимого!')

    def assert_content_editor_has_two_templates(self):
        expect(self._content_editor).to_have_text("Автотест для проверки добавления первого шаблона содержимого!"
                                                  "Это второй шаблон для автотеста, который проверяет, что добавляется второй шаблон в дополнении к первому")

    def assert_content_editor_is_empty(self):
        expect(self._content_editor).to_be_empty()

    def assert_picker_contain_users(self, classifier_name, users_type, fill_field=True):
        self.assert_dropdown_list_contain_options(classifier_name, users_type, fill_field=fill_field)

    def assert_picker_not_contain_users(self, classifier_name, users_type, fill_field=True):
        self.assert_dropdown_list_not_contain_options(classifier_name, users_type, fill_field=fill_field)

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
                             **self.fill_required_fields()}
            self.click_bottom_save_button()
            self.assert_document_tab_visible('Документ №')
            #expect(self.page.get_by_role('tab', name='Документ №')).to_be_visible()
            return DocumentViewPage(self.page), filled_fields



    def test_example(self):
        document_information = self.fill_textarea('Информация о документе')
        self.assert_textarea_has_value('Информация о документе', document_information)