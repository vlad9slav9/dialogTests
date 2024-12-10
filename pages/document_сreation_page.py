from playwright.sync_api import Page
from playwright.sync_api import expect
import datetime
import random

from mimesis import Generic

from pages.base_page import BasePage

generic = Generic('ru')


class DocumentCreationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self._outgoing_document_creation_tab = self.page.get_by_role("tab",
                                                                     name="Создание документа (Исходящий (Автотест))")
        self._end_date_field = self.page.locator("#endDate")
        self._document_date_field = self.page.get_by_label("Дата документа *", exact=True)
        self._document_type_field = self.page.get_by_label("Тип документа *", exact=True)
        self._from_whom_field = self.page.locator("#from")
        self._to_medo_checkbox = self.page.get_by_label("Для МЭДО", exact=True)
        self._link_to_number_field = self.page.get_by_label("Ссылается на № (для печати)", exact=True)
        self._document_number_field = self.page.get_by_label("№ документа", exact=True)
        self._document_referenced_date_field = self.page.get_by_label(
            "Дата документа на который ссылаемся (для печати)", exact=True)
        self._whom_field = self.page.get_by_label("Кому")
        self._control_uk_checkbox = self.page.get_by_label("Контроль УК", exact=True)
        self._control_uk_fcp_checkbox = self.page.get_by_label("Контроль УК ФЦП", exact=True)
        self._year_field = self.page.get_by_label("Год", exact=True)
        self._urgent_checkbox = self.page.get_by_label("Срочный", exact=True)
        self._organization_group_after_signing_field = self.page.get_by_role("textbox", name="Выберите группу")
        self._organization_after_signing_field = self.page.get_by_role("textbox",
                                                                       name="Адресат-организация после подписания (не более 10)")
        self._signature_field = self.page.get_by_label("Подпись", exact=True)
        self._signatory_position_field = self.page.locator("#position")
        self._show_signature_checkbox = self.page.get_by_label("Отображать ЭП при печати", exact=True)
        self._show_author_checkbox = self.page.get_by_label("Отображать автора и номер телефона на последней странице",
                                                            exact=True)
        self._document_information_field = self.page.locator("#props_0_17")
        self._coordinator_name_field = self.page.get_by_label("Имя согласователя", exact=True)
        self._coordinator_position_field = self.page.locator("#coordinator_pos")
        self._date_from_field = self.page.get_by_label("Дата от", exact=True)
        self._responsible_performer_field = self.page.get_by_label("Ответственный исполнитель", exact=True)
        self._users_group_after_signing_field = self.page.get_by_role("textbox", name="Добавить из группы")
        self._users_after_signing_field = self.page.get_by_role("textbox", name="Получатели после подписания")
        self._addressee_field = self.page.get_by_label("Адресат", exact=True)
        self._my_organisation_users_field = self.page.get_by_label("Пользователи своей орги", exact=True)
        self._test_number_field = self.page.get_by_label("Число", exact=True)
        self._document_view_field = self.page.get_by_label("Вид документа *", exact=True)
        self._topic_field = self.page.get_by_label("Тематика", exact=True)
        self._correspondent_field = self.page.get_by_label("Корреспондент", exact=True)

        self._meeting_place_field = self.page.get_by_label("Выездные совещания", exact=True)
        self._meeting_company_field = self.page.get_by_label("Встреча с коллективами предприятий", exact=True)

        self._print_font_size_field = self.page.get_by_label("Размер шрифта(при печати)", exact=True)
        self._short_description_field = self.page.locator("textarea[name='description']")
        self._print_template_field = self.page.get_by_role("textbox", name="Шаблон (для печати)")
        self._content_editor = self.page.get_by_role("textbox", name="Область редактирования редактора: main")
        self._upper_edit_button = self.page.get_by_role("button").and_(
            page.get_by_title("Сохранить + редактирование (Ctrl+Alt+S)"))
        self._upper_save_button = self.page.get_by_role("button").and_(
            page.get_by_title("Сохранить + просмотр (Ctrl+Alt+S)"))
        self._bottom_edit_button = self.page.get_by_role("button", name="Сохранить + редактировать")
        self._bottom_save_button = self.page.get_by_role("button", name="Сохранить + просмотр")

        self._responsible_in_from_field = self.page.get_by_role("button", name="Первый Ответственный Пользователь")

        self._first_responsible_user = self.page.get_by_role("option", name="Ответственный Первый Пользователь")
        self._first_regular_user = self.page.get_by_role("option", name="Обычный Первый Пользователь")

        self._meeting_place_multivalue = self.page.locator("#document_type_field_meeting")
        self._meeting_company_multivalue = self.page.locator("#document_type_field_meeting_region")

        self.group_with_organizations = ["ФУЛ МКУ 9", "Тестовая 9919", "РЕадмин", "Министерство сэд 2.0"]
        self.group_with_users = ["Ответственный Первый Пользователь | Автотестовая Родительская организация | Первая автотестовая должность", 'Обычный Первый Пользователь | Автотестовая Родительская организация | Вторая автотестовая должность']


    def assert_outgoing_document_creation_tab_visible(self):
        expect(self._outgoing_document_creation_tab).to_be_visible()

    def assert_end_date_filled_plus_nine_days(self):
        expected_date = self.generate_date_offset_days(9)
        expect(self._end_date_field).to_have_value(expected_date)

    def assert_document_date_filled_current_date(self):
        expected_date = datetime.datetime.now().strftime("%d.%m.%Y")
        expect(self._document_date_field).to_have_value(expected_date)

    def assert_date_from_filled_current_date(self):
        expected_date = datetime.datetime.now().strftime("%d.%m.%Y")
        expect(self._date_from_field).to_have_value(expected_date)


    def assert_show_signature_checkbox_checked(self):
        expect(self._show_signature_checkbox).to_be_checked()

    def assert_show_author_checkbox_checked(self):
        expect(self._show_author_checkbox).to_be_checked()

    def assert_year_filled_current_year(self):
        expected_year = datetime.datetime.now().strftime("%Y")
        expect(self._year_field).to_have_value(expected_year)

    def assert_print_template_filled_first_template(self):
        expect(self._print_template_field).to_have_value("Первый исходящий автотестовый шаблон")

    def fill_all_fields_randomly(self):
        document_type = self.fill_property('Тип документа *')
        self.assert_field_has_value('Тип документа *', document_type)

        link_to_number = self.fill_property('Ссылается на № (для печати)')
        self.assert_field_has_value('Ссылается на № (для печати)', link_to_number)

        document_number = self.fill_property('№ документа')
        self.assert_field_has_value('№ документа', document_number)

        reference_date = self.fill_date_property('Дата документа на который ссылаемся (для печати)')
        self.assert_field_has_value('Дата документа на который ссылаемся (для печати)', reference_date)

        whom_value = self.fill_classifier('Кому')
        self.assert_field_has_value('Кому', whom_value)

        self.check_control_uk()
        self._control_uk_checkbox.is_checked()

        self.check_control_uk_fcp()
        self._control_uk_fcp_checkbox.is_checked()

        self.check_urgent()
        self._urgent_checkbox.is_checked()

        organizations_group = self.fill_classifier("Выберите группу", option_value="ТК9 группа")
        self.assert_field_has_value("Выберите группу", organizations_group)
        self.assert_multivalues_field_has_value('Адресат-организация после подписания (не более 10)',
                                                self.group_with_organizations)

        signature_name = self.fill_classifier('Подпись')
        self.assert_field_has_short_name('Подпись', signature_name)

        document_information = self.fill_textarea('Информация о документе')
        self.assert_textarea_has_value('Информация о документе', document_information)

        coordinator_name = self.fill_classifier('Имя согласователя')
        self.assert_field_has_short_name('Имя согласователя', coordinator_name)

        responsible_performer = self.fill_classifier('Ответственный исполнитель')
        self.assert_field_has_value('Ответственный исполнитель', responsible_performer)

        users_group = self.fill_classifier("Добавить из группы", option_value="Пользователи моей организации")
        self.assert_field_has_value("Добавить из группы", users_group)
        self.assert_multivalues_field_has_value('Получатели после подписания', self.group_with_users)

        addressee = self.fill_classifier('Адресат')
        self.assert_field_has_value('Адресат', addressee)

        my_organization_users = self.fill_classifier('Пользователи своей орги')
        self.assert_field_has_value('Пользователи своей орги', my_organization_users)

        test_number = self.fill_property('Число', '1234567890')
        self.assert_field_has_value('Число', test_number)

        document_view = self.fill_classifier('Вид документа *')
        self.assert_field_has_value('Вид документа *', document_view)

        topic = self.fill_classifier('Тематика')
        self.assert_field_has_value('Тематика', topic)

        correspondent = self.fill_classifier('Корреспондент')
        self.assert_field_has_value('Корреспондент', correspondent)

        meeting_place = self.fill_classifier('Выездные совещания', multiform=True)
        self.assert_multivalues_field_has_value('Выездные совещания', meeting_place)

        meeting_company = self.fill_classifier('Встреча с коллективами предприятий', multiform=True)
        self.assert_multivalues_field_has_value('Встреча с коллективами предприятий', meeting_company)

        print_font_size = self.fill_classifier('Размер шрифта(при печати)')
        self.assert_field_has_value('Размер шрифта(при печати)', print_font_size)

        short_description = self.fill_short_description()
        self.assert_short_description_has_value(short_description)

        content = self.fill_content_editor()
        self.assert_content_editor_has_value(content)

    def shorten_name(self, option_text):
        parts = option_text.split()
        first_name_initial = parts[1][0]
        last_name = parts[0]
        short_name = f"{first_name_initial}. {last_name}"
        return short_name

    def fill_classifier(self, classifier_name, multiform=False, option_value=None):
        classifier = self.page.get_by_label(classifier_name, exact=True)
        options_locator = self.page.locator("role=option")

        def select_option(value=None):
            classifier.click()
            expect(options_locator).not_to_have_count(0)
            options = options_locator.all()
            if value:
                selected_option = next((opt for opt in options if value in opt.inner_text()), None)
            else:
                selected_option = random.choice(options)
            option_text = selected_option.inner_text()
            selected_option.click()
            return option_text
        if multiform:
            selected_texts = []
            for _ in range(3):
                selected_texts.append(select_option())
            return selected_texts
        else:
            return select_option(option_value)

    def fill_property(self, property_name, input_text=None):
        if input_text:
            self.page.get_by_label(property_name, exact=True).fill(input_text)
        else:
            input_text = self.generate_random_string_with_all_symbols()
            self.page.get_by_label(property_name, exact=True).fill(input_text)

        return input_text

    def fill_textarea(self, area_name, input_text=None):
        if input_text:
            self.page.locator(f"legend:has-text('{area_name}')").locator("..").locator(
                "textarea.PropsTextArea-Autosize:first-of-type").fill(input_text)
        else:
            input_text = generic.text.text()
            self.page.locator(f"legend:has-text('{area_name}')").locator("..").locator(
                "textarea.PropsTextArea-Autosize:first-of-type").fill(input_text)

        return input_text

    def fill_date_property(self, date_property_name, input_date=None):
        if input_date:
            self.page.get_by_label(date_property_name, exact=True).fill(input_date)
        else:
            input_date = self.generate_date_offset_days(0)
            self.page.get_by_label(date_property_name, exact=True).fill(input_date)

        return input_date

    def fill_content_editor(self, text=None):
        if text:
            self.page.get_by_role("textbox", name='Область редактирования редактора: main').fill(text)
        else:
            text = generic.text.text()
            self.page.get_by_role("textbox", name='Область редактирования редактора: main').fill(text)

        return text

    def fill_short_description(self, value=None):
        if value:
            self.page.locator("textarea[name='description']").fill(value)
        else:
            value = generic.text.text()
            self.page.locator("textarea[name='description']").fill(value)
        return value

    def assert_short_description_has_value(self, value):
        expect(self.page.locator("textarea[name='description']")).to_have_value(value)

    def assert_content_editor_has_value(self, value):
        expect(self.page.get_by_role("textbox", name='Область редактирования редактора: main')).to_have_text(value)

    def assert_field_has_short_name(self, classifier_name, option_text):
        short_name = self.shorten_name(option_text)
        expect(self.page.get_by_label(classifier_name, exact=True)).to_have_value(short_name)

    def assert_field_has_value(self, field_name, value):
        expect(self.page.get_by_label(field_name, exact=True)).to_have_value(value.strip())

    def assert_multivalues_field_has_value(self, field_name, values):
        field_container = self.page.locator(f"label:has-text('{field_name}')").locator("..").locator(
            ".MuiInputBase-root")

        for text in values:
            button = field_container.locator(f"[role='button'] >> text='{text}'")
            expect(button).to_be_visible()

    def assert_textarea_has_value(self, area_name, value_text):
        textarea = self.page.locator(f"legend:has-text('{area_name}')").locator("..").locator(
            "textarea.PropsTextArea-Autosize:first-of-type")
        expect(textarea).to_have_value(value_text)

    def example_method(self):
        short_description = self.fill_short_description()
        self.assert_short_description_has_value(short_description)
