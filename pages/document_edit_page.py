import random
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta
from mimesis import Generic
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.document_view_page import DocumentViewPage

generic_ru = Generic("ru")

TARGET_CLASSIFIER_FRONTEND_INPUTS = {
    "workerPicker",
    "classifierSelect",
    "targetDepartmentPicker",
    "signature",
    "onlyMyDepWorkerPicker",
    "targetDepartmentAfterSignPicker",
}

TARGET_PROPERTY_INPUTS = {"date", "dateYear", "date_empty", "text", "text_area"}


class DocumentEditPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # self.page = page

        self._outgoing_document_creation_tab = self.page.get_by_role(
            "tab", name="Создание документа (Исходящий (Автотест))", exact=True
        )
        self._end_date_field = self.page.locator("#endDate")
        self._short_description_field = self.page.locator(
            "textarea[name='description']"
        )
        # self._print_template_field = self.page.get_by_role('textbox', name='Шаблон (для печати)')
        self._print_template_field = self.page.locator("#templateId")
        self._content_editor = self.page.get_by_role(
            "textbox", name="Область редактирования редактора: main"
        )
        self._upper_edit_button = self.page.get_by_role("button").and_(
            page.get_by_title("Сохранить + редактирование (Ctrl+Alt+S)")
        )
        self._upper_save_button = self.page.get_by_role("button").and_(
            page.get_by_title("Сохранить + просмотр (Ctrl+Alt+S)")
        )
        self._bottom_edit_button = self.page.get_by_role(
            "button", name="Сохранить + редактировать", exact=True
        )
        self._bottom_save_button = self.page.get_by_role(
            "button", name="Сохранить + просмотр", exact=True
        )
        self._error_snackbar = self.page.locator("#notistack-snackbar")
        self._short_description = self.page.locator("textarea[name='description']")
        self.clear_print_template_button = self.page.locator(
            "//label[text() = 'Шаблон (для печати)']//following::button[@title='Clear']"
        )
        self._content_template_field = self.page.locator(".Document-Select").filter(
            has_text="Добавить содержимое из шаблона"
        )

        self._calendar_year_button = self.page.locator(
            "button:has(h6.MuiPickersToolbarText-toolbarTxt)"
        )

        self._prev_month_button = self.page.locator(
            ".MuiPickersCalendarHeader-switchHeader button"
        ).nth(0)
        self._next_month_button = self.page.locator(
            ".MuiPickersCalendarHeader-switchHeader button"
        ).nth(1)

        self.classifiers_ids = [
            "office_class_view_docs",
            "whom",
            "target_department",
            "responsible_performer",
            "users_my_org_test",
            "office_class_topics",
            "office_class_corrs",
            "print_font_size_pt",
        ]

    def select_option(self, value=None):
        options_locator = self.page.get_by_role("option")
        expect(options_locator).not_to_have_count(0)
        options = options_locator.all()
        if value:
            selected_option = next(
                (option for option in options if value in option.inner_text()), None
            )
        else:
            selected_option = random.choice(options)
        option_text = selected_option.inner_text()
        selected_option.click()
        return option_text

    def fill_classifier_group(self, classifier_label, value):
        group_locator = self.page.get_by_label(f"{classifier_label}")
        group_locator.click()
        self.select_option(value)

    def clear_group_field_by_id(self, field_id):
        clear_locator = self.page.locator(
            f'#{field_id} [class*="GroupsPicker"] button[aria-label="Clear"]'
        )
        clear_locator.click()

    def fill_date_property(self, date_property_name, input_date=None):
        date_property_locator = self.page.get_by_label(date_property_name, exact=True)
        if input_date:
            date_property_locator.press_sequentially(input_date)
        else:
            input_date = self.generate_date_offset_days(0)
            date_property_locator.press_sequentially(input_date)

        return input_date

    def change_date_in_property(self, prop_name, date_offset):
        self.clear_property(prop_name)
        new_date = self.generate_date_offset_days(date_offset)
        self.fill_date_property(prop_name, new_date)
        self.assert_property_has_value(prop_name, new_date)

    def click_field_calendar(self, property_name):
        button = self.page.locator(
            f"//label[text() = '{property_name}']/following::button[1]"
        )
        button.click()

    def change_date_via_calendar(self, property_name, future_date=True, is_year=False):
        delta = relativedelta(days=1, months=1, years=1)
        new_date = datetime.today() + delta if future_date else datetime.today() - delta
        self.click_field_calendar(property_name)
        if is_year:
            self.page.locator(".MuiPickersYear-root").get_by_text(
                new_date.strftime("%Y")
            ).click()
            return new_date.strftime("%Y")
        self._calendar_year_button.click()
        self.page.locator(".MuiPickersYear-root").get_by_text(
            new_date.strftime("%Y")
        ).click()
        self._next_month_button.click() if future_date else self._prev_month_button.click()
        self.page.locator(".MuiPickersDay-day").get_by_text(
            new_date.strftime("%d")
        ).first.click()
        return new_date.strftime("%d.%m.%Y")

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
        self._content_editor.click()
        self._content_editor.press("Control+A")
        self._content_editor.press("Backspace")

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
        self._print_template_field.press_sequentially(f"{entered_text}")
        self.assert_dropdown_list_contain_text(f"{entered_text}")
        options_locator = self.page.get_by_role("option", name=f"{entered_text}")
        options_locator.click()

    def assert_checkbox_checked(self, checkbox_id):
        expect(
            self.page.locator(f'#{checkbox_id} input[type="checkbox"]')
        ).to_be_checked()

    def assert_checkbox_not_checked(self, checkbox_id):
        expect(
            self.page.locator(f'#{checkbox_id} input[type="checkbox"]')
        ).not_to_be_checked()

    def assert_field_is_empty(self, field_label):
        container = self.get_field_container(field_label)

        # Классификаторы / Мультиселекты
        if container.locator(".MuiChip-root, .MuiAutocomplete-tag").count() > 0:
            return False

        # Чекбоксы и переключатели
        checkbox = container.locator('input[type="checkbox"]')
        if checkbox.count() > 0 and checkbox.first.is_checked():
            return False

        # Текстовые инпуты, даты, числа
        input_elem = container.locator(
            "input:not([type='hidden']):not([type='checkbox'])"
        )
        if input_elem.count() > 0 and input_elem.first.input_value().strip():
            return False

        # 4. Многострочные Textarea
        textarea_elem = container.locator("textarea:visible")
        return not (
            textarea_elem.count() > 0 and textarea_elem.first.input_value().strip()
        )

    def fill_empty_fields(self, only_required_fields=False):
        template_data = getattr(self, "template_data", None)
        if not template_data:
            raise ValueError("Данные шаблона не были перехвачены!")

        filled_fields = {}

        for block in template_data.get("template", []):
            for item in block.get("items", []):
                if only_required_fields and not item.get("required"):
                    continue

                frontend_input = item.get("frontendInput")
                is_multiple = item.get("multiple", False)
                field_label = item.get("label")

                if not self.assert_field_is_empty(field_label):
                    continue

                if frontend_input in TARGET_CLASSIFIER_FRONTEND_INPUTS:
                    selected_value = self.fill_classifier_by_label(
                        field_label=field_label,
                        is_multiple=is_multiple,
                        search_prefix="тес",
                    )
                    expected_value = selected_value
                    if frontend_input == "signature":
                        expected_value = self.get_shortened_name(selected_value)

                    self.assert_field_has_value_by_label(field_label, expected_value)
                    filled_fields[field_label] = selected_value

                elif frontend_input in TARGET_PROPERTY_INPUTS:
                    if frontend_input in ["date", "date_empty"]:
                        value = self.generate_date_offset_days(0)
                    elif frontend_input == "dateYear":
                        value = self.generate_date_offset_days(0, year=True)
                    elif frontend_input in ["text", "text_area"]:
                        value = self.generate_random_input()
                    else:
                        raise ValueError(
                            f"Неподдерживаемый тип свойства: {frontend_input}"
                        )

                    self.fill_field_by_label(field_label, value)
                    self.assert_field_has_value_by_label(field_label, value)
                    filled_fields[field_label] = value

                elif frontend_input == "checkbox":
                    self.set_switch_by_label(field_label, True)
                    self.assert_field_has_value_by_label(field_label, True)
                    filled_fields[field_label] = True

        short_desc = self.fill_short_description()
        filled_fields["Краткое описание"] = short_desc

        content_text = self.fill_content_editor()
        filled_fields["Содержимое"] = content_text

        return filled_fields

    def click_upper_edit_button(self):
        self._upper_edit_button.click()

    def click_upper_save_button(self):
        self._upper_save_button.click()

    def click_bottom_edit_button(self):
        self._bottom_edit_button.click()

    def click_bottom_save_button(self):
        self._bottom_save_button.click()

    def assert_document_creation_tab_visible(self, document_name):
        locator = self.page.get_by_role(
            "tab", name=f"Создание документа ({document_name})", exact=True
        )
        expect(locator).to_be_visible()

    def assert_default_fields_are_filled(self, user_information, return_values=False):
        end_date = self.generate_date_offset_days(14)
        self.assert_field_has_value_by_label("Срок исполнения", end_date)
        # expect(self._end_date_field).to_have_value(end_date)

        current_date = self.generate_date_offset_days()
        self.assert_field_has_value_by_label("Дата документа", current_date)

        self.assert_field_has_value_by_label("Дата от", current_date)

        current_year = self.generate_date_offset_days(0, year=True)
        self.assert_field_has_value_by_label("Год", current_year)

        self.assert_field_has_value_by_label("От кого", user_information)

        self.assert_field_has_value_by_label("Отображать ЭП при печати", True)
        self.assert_field_has_value_by_label(
            "Отображать автора и номер телефона на последней странице", True
        )

        expect(self._print_template_field).to_have_value("Первый автотестовый шаблон")

        if return_values:
            return {
                "Срок исполнения": end_date,
                "Дата документа": current_date,
                "Дата от": current_date,
                "От кого": user_information.rsplit(" | ", 1)[0],
                "Год": current_year,
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

    def assert_picker_contain_users(
        self, classifier_name, users_values, fill_field=True
    ):
        self.assert_dropdown_list_contain_options(
            classifier_name, users_values, fill_field=fill_field
        )

    def assert_picker_not_contain_users(
        self, classifier_name, users_values, fill_field=True
    ):
        self.assert_dropdown_list_not_contain_options(
            classifier_name, users_values, fill_field=fill_field
        )

    def assert_document_tab_visible(self, tab_name):
        expect(self.page.get_by_role("tab").filter(has_text=tab_name)).to_be_visible()

    def create_document(self, user_information, only_required_fields=False):
        if only_required_fields:
            filled_fields = {
                **self.assert_default_fields_are_filled(
                    user_information, return_values=True
                ),
                **self.fill_empty_fields(only_required_fields=True),
            }
            self.click_bottom_save_button()
            self.assert_document_tab_visible("Документ №")
            return DocumentViewPage(self.page), filled_fields
        else:
            filled_fields = {
                **self.assert_default_fields_are_filled(
                    user_information, return_values=True
                ),
                **self.fill_empty_fields(),
            }
            self.click_upper_save_button()
            self.assert_document_tab_visible("Документ №")
            return DocumentViewPage(self.page), filled_fields

    def clear_editable_fields(self):
        template_data = getattr(self, "template_data", None)
        if not template_data:
            raise ValueError("Данные шаблона не были перехвачены!")
        for block in template_data.get("template", []):
            for item in block.get("items", []):
                # Проверяем, что поле доступно для редактирования
                if not item.get("editable", False):
                    continue
                field_label = item.get("label")
                self.clear_field_by_label(field_label)
        self._short_description.clear()
        self._content_editor.clear()

    def get_field_container(self, field_name: str):
        pattern = re.compile(rf"^\s*{re.escape(field_name)}[\s\*\u2009]*$")
        return self.page.locator(
            ".MuiFormControl-root, fieldset, .Document-TextArea, .PropsTextArea"
        ).filter(
            has=self.page.locator(
                "label, legend, .MuiFormControlLabel-label", has_text=pattern
            )
        )

    # Заполнение текстовых полей, дат, чисел и многострочных Textarea
    def fill_field_by_label(self, field_label, value):
        container = self.get_field_container(field_label)
        field_input = container.locator(
            "input:not([type='hidden']), textarea:visible"
        ).first
        field_input.click()
        field_input.press("Control+A")
        field_input.press("Backspace")
        field_input.press_sequentially(str(value))
        return value

    # Очистка любого поля по названию
    def clear_field_by_label(self, field_label):
        container = self.get_field_container(field_label)

        # Если есть кнопка очистки Autocomplete
        clear_btn = container.locator(
            "button[title='Clear'], button[aria-label='Clear']"
        )
        if clear_btn.is_visible():
            clear_btn.click()
            return

        # Если есть чипы
        delete_icons = container.locator(".MuiChip-deleteIcon")
        if delete_icons.count() > 0:
            for icon in delete_icons.all()[::-1]:
                icon.click()
            return

        # Для обычных input и textarea
        field_input = container.locator(
            "input:not([type='hidden']), textarea:visible"
        ).first
        field_input.click()
        field_input.press("Control+A")
        field_input.press("Backspace")

    # Заполнение классификаторов / справочников / Autocomplete по названию
    def fill_classifier_by_label(
        self,
        field_label,
        value=None,
        search_prefix=None,
        is_multiple=False,
    ):
        container = self.get_field_container(field_label)
        input_locator = container.locator("input:not([type='hidden'])")

        if is_multiple:
            selected_values = []
            for _ in range(2):
                input_locator.click(force=True)
                if search_prefix:
                    input_locator.press_sequentially(search_prefix)
                selected_values.append(self.select_option(value))
            return selected_values
        else:
            input_locator.click(force=True)
            if search_prefix:
                input_locator.press_sequentially(search_prefix)
            return self.select_option(value)

    # Переключение чекбоксов
    def set_switch_by_label(self, field_label, state=True):
        container = self.get_field_container(field_label)
        checkbox = container.locator("input[type='checkbox']")
        is_checked = checkbox.is_checked()
        if is_checked != state:
            checkbox.click(force=True)

    # Проверка значения в поле по его названию
    def assert_field_has_value_by_label(self, field_label, expected_value):
        container = self.get_field_container(field_label)

        # Если это чипы
        chips = container.locator(".MuiChip-label")
        if chips.count() > 0:
            if isinstance(expected_value, list):
                expect(chips).to_have_text(expected_value)
            else:
                expect(chips).to_have_text(str(expected_value))
            return

        # Если это чекбокс
        checkbox = container.locator("input[type='checkbox']")
        if checkbox.count() > 0:
            if expected_value is True:
                expect(checkbox).to_be_checked()
            elif expected_value is False:
                expect(checkbox).not_to_be_checked()
            return

        # Для обычных input и textarea
        target = container.locator("input:not([type='hidden']), textarea:visible").first
        expect(target).to_have_value(str(expected_value))
