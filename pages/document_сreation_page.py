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




    '''def fill_classifier_with_random_option(self, input_field, classifier_options):
        input_field.click()
        random_option = random.choice(classifier_options)
        option_text = random_option.inner_text()
        random_option.click()
        expect(input_field).to_have_value(option_text)
        return option_text'''

    '''def fill_classifier_with_short_random_option(self, input_field, classifier_options, short_names):
        input_field.click()
        random_option = random.choice(classifier_options)
        option_text = random_option.inner_text()
        random_option.click()
        expected_shortened_value = short_names.get(option_text)
        expect(input_field).to_have_value(expected_shortened_value)
        return expected_shortened_value'''



    def fill_end_date(self, date):
        self._end_date_field.fill(date)
        expect(self._end_date_field).to_have_value(date)

    def fill_document_date(self, date):
        self._document_date_field.fill(date)
        expect

    def fill_document_type(self, document_type):
        self._document_type_field.fill(document_type)

    def check_to_medo_checkbox(self):
        self._to_medo_checkbox.check()

    def fill_link_to_number(self, number):
        self._link_to_number_field.fill(number)

    def fill_document_number(self, number):
        self._document_number_field.fill(number)

    def fill_document_referenced_date(self, date):
        self._document_referenced_date_field.fill(date)

    def fill_whom(self, user_option):
        self._whom_field.click()
        user_option.click()

    def check_control_uk(self):
        self._control_uk_checkbox.check()

    def check_control_uk_fcp(self):
        self._control_uk_fcp_checkbox.check()

    def fill_year(self, year):
        self._year_field.fill(year)

    def check_urgent(self):
        self._urgent_checkbox.check()

    def fill_organisation_group_after_signing_field(self, group_option):
        self._organization_group_after_signing_field.click()
        group_option.click()

    def fill_organisation_after_signing_field(self, organization_name, organization_option):
        self._organization_after_signing_field.fill(organization_name)
        organization_option.click()

    def fill_signature(self, user_option):
        self._signature_field.click()
        user_option.click()

    def fill_signatory_position(self, position):
        self._signatory_position_field.fill(position)

    def fill_document_information(self, information):
        self._document_information_field.fill(information)

    def fill_coordinator_position(self, position):
        self._coordinator_position_field.fill(position)

    def fill_date_from(self, date):
        self._date_from_field.fill(date)

    def fill_test_number(self, number):
        self._test_number_field.fill(number)

    def fill_short_description(self, description):
        self._short_description_field.fill(description)

    def fill_content_editor(self, content):
        self._content_editor.fill(content)

    def clear_end_date(self):
        self._end_date_field.clear()

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

    def assert_from_whom_filled_with_responsible(self):
        expect(self._from_whom_field).to_contain_text(
            "Первый Ответственный Пользователь | Автотестовая Родительская организация | Первая автотестовая должность")

    def assert_show_signature_checkbox_checked(self):
        expect(self._show_signature_checkbox).to_be_checked()

    def assert_show_author_checkbox_checked(self):
        expect(self._show_author_checkbox).to_be_checked()

    def assert_year_filled_current_year(self):
        expected_year = datetime.datetime.now().strftime("%Y")
        expect(self._year_field).to_have_value(expected_year)

    def assert_print_template_filled_first_template(self):
        expect(self._print_template_field).to_have_value("Первый исходящий автотестовый шаблон")

    def fill_random_document_type(self):
        random_document_type = self.generate_random_string_with_all_symbols()
        self._document_type_field.fill(random_document_type)
        return random_document_type

    def fill_random_link_to_number(self):
        random_link_to_number = self.generate_random_string_with_all_symbols()
        self._link_to_number_field.fill(random_link_to_number)
        return random_link_to_number

    def fill_random_document_number(self):
        random_document_number = self.generate_random_string_with_all_symbols()
        self._document_number_field.fill(random_document_number)
        return random_document_number

    def fill_document_referenced_date_with_current(self):
        current_date = self.generate_date_offset_days(0)
        self.fill_document_referenced_date(current_date)
        return current_date

    def fill_random_whom(self):
        return self.select_random_option(self._whom_field)

    def fill_random_organization_group_after_signing(self):
        return self.select_random_option(self._organization_group_after_signing_field)

    def fill_random_signature(self):
        return self.select_random_option(self._signature_field)

    def fill_random_document_information(self):
        random_information = generic.text.text()
        self.fill_document_information(random_information)
        return random_information

    def fill_random_coordinator_name(self):
        return self.select_random_option(self._coordinator_name_field)

    def fill_random_responsible_performer(self):
        return self.select_random_option(self._responsible_performer_field)

    def fill_random_users_group_after_signing(self):
        return self.select_random_option(self._users_group_after_signing_field)

    def fill_random_addressee(self):
        return self.select_random_option(self._addressee_field)

    def fill_random_my_organization_users(self):
        return self.select_random_option(self._my_organisation_users_field)

    def fill_random_test_number(self):
        random_number = generic.random.randint(0, 99)
        self.fill_test_number(random_number)
        return random_number

    def fill_random_document_view(self):
        return self.select_random_option(self._document_view_field)

    def fill_random_topic(self):
        return self.select_random_option(self._topic_field)

    def fill_random_correspondent(self):
        return self.select_random_option(self._correspondent_field)

    def fill_random_meeting_place(self):
        return self.select_random_option(self._meeting_place_field)

    def fill_random_meeting_company(self):
        return self.select_random_option(self._meeting_company_field)

    def fill_random_print_font_size(self):
        return self.select_random_option(self._print_font_size_field)

    def fill_random_short_description(self):
        random_short_description = generic.text.text()
        self.fill_short_description(random_short_description)
        return random_short_description

    def fill_random_content(self):
        random_content = generic.text.text()
        self.fill_content_editor(random_content)
        return random_content

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

        #random_organizations_group = self.fill_random_organization_group_after_signing()
        #expect(self._organization_group_after_signing_field).to_have_value(random_organizations_group)

        #random_signature = self.fill_random_signature()
        #self.shorten_name(self._signature_field, random_signature)

        #random_document_information = self.fill_random_document_information()
        #expect(self._document_information_field).to_have_value(random_document_information)

        #random_coordinator_name = self.fill_random_coordinator_name()
        #self.shorten_name(self._coordinator_name_field, random_coordinator_name)

        #random_responsible_performer = self.fill_random_responsible_performer()
        #expect(self._responsible_performer_field).to_have_value(random_responsible_performer)

        #random_users_group = self.fill_random_users_group_after_signing()
        #expect(self._users_group_after_signing_field).to_have_value(random_users_group)

        #random_addressee = self.fill_random_addressee()
        #expect(self._addressee_field).to_have_value(random_addressee)

        #random_my_organization_users = self.fill_random_my_organization_users()
        #expect(self._my_organisation_users_field).to_have_value(random_my_organization_users)

        #random_test_number = self.fill_random_test_number()
        #self.assert_field_has_correct_value(self._test_number_field, random_test_number)

        #random_document_view = self.fill_random_document_view()
        #expect(self._document_view_field).to_have_value(random_document_view)

        #random_topic = self.fill_random_topic()
        #expect(self._topic_field).to_have_value(random_topic)

        #random_correspondent = self.fill_random_correspondent()
        #expect(self._correspondent_field).to_have_value(random_correspondent)

        #random_meeting_place = self.fill_random_meeting_place()
        #expect(self._meeting_place_multivalue).to_contain_text(random_meeting_place)

        #random_meeting_company = self.fill_random_meeting_company()
        #expect(self._meeting_company_multivalue).to_contain_text(random_meeting_company)

        #random_print_font_size = self.fill_random_print_font_size()
        #expect(self._print_font_size_field).to_have_value(random_print_font_size)

        #random_short_description = self.fill_random_short_description()
        #expect(self._short_description_field).to_have_value(random_short_description)

        #random_content = self.fill_random_content()
        #self.assert_field_has_correct_value(self._content_editor, random_content)

    '''def select_random_option(self, classifier):
        classifier.click()
        expect(self.page.locator("role=option")).not_to_have_count(0)
        options = self.page.locator("role=option").all()
        #expect(classifier.locator("role=option")).not_to_have_count(0)
        #options = classifier.locator("role=option").all()
        random_option = random.choice(options)
        option_text = random_option.inner_text()
        random_option.click()
        return option_text'''



    def shorten_name(self, option_text):
        parts = option_text.split()
        first_name_initial = parts[1][0]
        last_name = parts[0]
        short_name = f"{first_name_initial}. {last_name}"
        return short_name


    def fill_classifier(self, classifier_name, option_value=None):
        self.page.get_by_label(classifier_name, exact=True).click()
        expect(self.page.locator("role=option")).not_to_have_count(0)
        options = self.page.locator("role=option").all()
        if option_value:
            matching_option = next((option for option in options if option_value in option.inner_text()), None)
            selected_option = matching_option
        else:
            selected_option = random.choice(options)
        option_text = selected_option.inner_text()
        selected_option.click()

        return option_text

    def fill_property(self, property_name, input_text=None):
        if input_text:
            self.page.get_by_label(property_name, exact=True).fill(input_text)
        else:
            input_text = self.generate_random_string_with_all_symbols()
            self.page.get_by_label(property_name, exact=True).fill(input_text)

        return input_text

    def fill_textarea(self, area_name, input_text=None):
        if input_text:
            self.page.get_by_label(area_name, exact=True).fill(input_text)
        else:
            input_text = generic.text.text()
            self.page.get_by_label(area_name, exact=True).fill(input_text)

        return input_text

    def fill_date_property(self, date_property_name, input_date=None):
        if input_date:
            self.page.get_by_label(date_property_name, exact=True).fill(input_date)
        else:
            input_date = self.generate_date_offset_days(0)
            self.page.get_by_label(date_property_name, exact=True).fill(input_date)

        return input_date


    def assert_classifier_has_short_name(self, classifier_name, option_text):
        short_name = self.shorten_name(option_text)
        expect(self.page.get_by_label(classifier_name, exact=True)).to_have_value(short_name)


    def assert_field_has_value(self, field_name, value):
        expect(self.page.get_by_label(field_name, exact=True)).to_have_value(value)



    def example_method(self):

        doc_view = self.fill_classifier("Вид документа *")
        self.assert_field_has_value("Вид документа *", doc_view)



