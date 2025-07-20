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
        locator = self.page.locator(f".MuiFormControl-root:has(label:text-is('{field_name}'))").locator("input, textarea, span.MuiChip-label, div.PropsViewWorkerPickerSelect-UserList")
        first_element = locator.first
        tag_name = first_element.evaluate("el => el.tagName.toLowerCase()")
        if tag_name in ['input', 'textarea']:
            expect(first_element).to_have_value(expected_value)
        else:
            for value in expected_value:
                expect(locator.filter(has_text=value)).to_be_visible()

    def assert_field_has_value_test(self, field_name, expected_value):
        base_locator = self.page.locator(f".MuiFormControl-root:has(label:text-is('{field_name}'))")
        locator = base_locator.locator("input, textarea, span.MuiChip-label, div.PropsViewWorkerPickerSelect-UserList")

        # Определяем, какой именно элемент перед нами (input или span и т.п.)
        first_element = locator.first
        tag_name = first_element.evaluate("el => el.tagName.toLowerCase()")

        if isinstance(expected_value, str):
            expected_value = [expected_value]

        if tag_name in ['input', 'textarea']:
            # Строковое значение - ожидаем одиночное поле
            for value in expected_value:
                expect(first_element).to_have_value(value)
        else:
            # Ожидаем список span’ов или div’ов — проверяем по одному
            chips = base_locator.locator("span.MuiChip-label, div.PropsViewWorkerPickerSelect-UserList")
            for value in expected_value:
                expect(chips.filter(has_text=value)).to_be_visible()

    def assert_fields_have_values(self, fields_values):
        for field_name, expected_value in fields_values.items():
            self.assert_field_has_value(field_name, expected_value)

    #def example_method(self, expected_data):
