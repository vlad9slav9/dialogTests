import time

from pages.base_page import BasePage
from playwright.sync_api import Page
from playwright.sync_api import expect


class DocumentViewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self._doc_number_tab = self.page.locator('.DocNumber-Text')
        self._doc_history_tab = self.page.get_by_role('tab', name='История документа', exact=True)

    def assert_field_has_value(self, field_name, expected_value):
        locator = (self.page.locator(f".MuiFormControl-root:has(label:text-is('{field_name}'))")
                   .locator("input, textarea, span.MuiChip-label, div.PropsViewWorkerPickerSelect-UserList, div.MuiSelect-root"))
        current_locator = locator.first
        tag_name = current_locator.evaluate("el => el.tagName.toLowerCase()")
        if tag_name in ['input', 'textarea']:
            expect(current_locator).to_have_value(expected_value)
        elif 'MuiSelect-root' in current_locator.evaluate("el => el.className"):
            expect(current_locator).to_have_text(expected_value)
        else:
            if isinstance(expected_value, str):
                expected_value = [expected_value]
            for value in expected_value:
                expect(locator.filter(has_text=value)).to_be_visible()

    def assert_description_contain_text(self, field_name, expected_text):
        locator = self.page.locator(f"div.CustomSpoiler:has(.CustomSpoiler-Title:text-is('{field_name}')) div.Document-ContentView")
        expect(locator).to_contain_text(expected_text)

    def assert_fields_have_values(self, fields_values):
        for field_name, expected_value in fields_values.items():
            if field_name in ("Краткое описание:", "Содержимое:"):
                self.assert_description_contain_text(field_name, expected_value)
            else:
                self.assert_field_has_value(field_name, expected_value)

    def assert_system_fields_have_values(self, user_information):
        current_date = self.generate_date_offset_days()
        self.assert_field_has_value('Дата создания в системе', current_date)

        document_author = user_information.split(' | ', 1)[0]
        self.assert_field_has_value('Автор документа', document_author)

        self.assert_field_has_value('Статус Документа', 'Открыт')


    #def example_method(self, expected_data):
