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
                   .locator("input, textarea, span.MuiChip-label, div.PropsViewWorkerPickerSelect-UserList").first)
        tag_name = locator.evaluate("el => el.tagName.toLowerCase()")
        if tag_name in ['input', 'textarea']:
            expect(locator).to_have_value(expected_value)
        else:
            expect(locator).to_contain_text(expected_value)

    def assert_fields_have_values(self, fields_values):
        for field_name, expected_value in fields_values.items():
            self.assert_field_has_value(field_name, expected_value)


    #def example_method(self, expected_data):



