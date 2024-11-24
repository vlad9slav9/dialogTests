from playwright.sync_api import Page
from playwright.sync_api import expect

class CreateDocumentPage():
    def __init__(self, page: Page):
        self.page = page

        self._outgoing_document_creation_tab = self.page.get_by_role("tab", name="Создание документа (Исходящий (Автотест))")
        self._end_date_field = self.page.locator("#endDate")
        self._document_date_field = self.page.locator("#date_doc")
        self._document_type_field = self.page.locator("#doc_type")
        self._from_field = self.page.locator("#from")
        self._to_medo_checkbox = self.page.locator("#to_medo")
        self._link_to_number_field = self.page.locator("#link_to_num")
        self._document_number_field = self.page.locator("#doc_num")
        self._document_referenced_date_field = self.page.locator("#data_experiment")
        self._whom_field = self.page.locator("#whom")
        self._control_uk_checkbox = self.page.locator("#control_uk")
        self._control_uk_fcp_checkbox = self.page.locator("#control_uk_fcp")
        self._year_field = self.page.locator("#date_year")
        self._urgent_checkbox = self.page.locator("#urgent")
        self._organisation_group_after_signing_field = self.page.get_by_role("textbox", name="Выберите группу")
        self._organisation_after_signing_field = self.page.get_by_role("textbox", name="Адресат-организация после подписания (не более 10)")
        self._signature_field = self.page.locator("#signature")
        self._signatory_position_field = self.page.locator("#position")
        self._show_signature_checkbox = self.page.locator("#show_signature")
        self._show_author_checkbox = self.page.locator("#show_author")
        self._document_information_field = self.page.locator("#smrkdocinfo")
        self._coordinator_name_field = self.page.locator("#coordinator_name")
        self._coordinator_position_field = self.page.locator("#coordinator_pos")
        self._date_from_field = self.page.locator("#date_from")
        self._responsible_performer_field = self.page.locator("#responsible_performer")
        self._users_group_after_signing_field = self.page.get_by_role("textbox", name="Добавить из группы")
        self._users_after_signing_field = self.page.get_by_role("textbox", name="Получатели после подписания")
        self._addressee_field = self.page.locator("#target_department")
        self._my_organisation_users_field = self.page.locator("#users_my_org_test")
        self._test_number_field = self.page.locator("#number_64_test")
        self._document_view_field = self.page.locator("#office_class_view_docs")
        self._topic_field = self.page.locator("#office_class_topics")
        self._correspondent_field = self.page.locator("#office_class_corrs")
        self._meeting_place_field = self.page.locator("#document_type_field_meeting")
        self._meeting_company_field = self.page.locator("#document_type_field_meeting_region")
        self._print_font_size_field = self.page.locator("#print_font_size_pt")
        self._description_field = self.page.locator("textarea[name='description']")
        self._print_template_field = self.page.get_by_role("textbox", name="Шаблон (для печати)")
        self._content_editor = self.page.get_by_role("textbox", name="Область редактирования редактора: main")
        self._upper_edit_button = self.page.get_by_role("button").and_(page.get_by_title("Сохранить + редактирование (Ctrl+Alt+S)"))
        self._upper_save_button = self.page.get_by_role("button").and_(page.get_by_title("Сохранить + просмотр (Ctrl+Alt+S)"))
        self._bottom_edit_button = self.page.get_by_role("button", name="Сохранить + редактировать")
        self._bottom_save_button = self.page.get_by_role("button", name="Сохранить + просмотр")








    def assert_outgoing_document_creation_tab_visible(self):
        expect(self._outgoing_document_creation_tab).to_be_visible()
