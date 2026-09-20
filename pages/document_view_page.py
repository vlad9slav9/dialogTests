from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class DocumentViewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self._doc_number_tab = self.page.locator(".DocNumber-Text")
        self._doc_history_tab = self.page.get_by_role(
            "tab", name="История документа", exact=True
        )
        self._edit_button = self.page.locator("#edit_document")

    def click_edit_button(self):
        self._edit_button.click()

    def assert_field_has_value(self, field_name, expected_value):
        locator = self.page.locator(
            f".MuiFormControl-root:has(label:text-is('{field_name}'))"
        ).locator(
            "input, textarea, span.MuiChip-label, div.PropsViewWorkerPickerSelect-UserList, div.MuiSelect-root"
        )
        current_locator = locator.first
        tag_name = current_locator.evaluate("el => el.tagName.toLowerCase()")
        if tag_name in ["input", "textarea"]:
            expect(current_locator).to_have_value(expected_value)
        elif "MuiSelect-root" in current_locator.evaluate("el => el.className"):
            expect(current_locator).to_have_text(expected_value)
        else:
            if isinstance(expected_value, str):
                expected_value = [expected_value]
            for value in expected_value:
                expect(locator.filter(has_text=value)).to_be_visible()

    def assert_test_field_has_value(self, field_id):
        new_locator = self.page.locator(f"#{field_id}").locator(
            "input, textarea:visible, .MuiChip-label, .ViewSwitch-Switch, .PropsViewWorkerPickerSelect-UserList"
        )

        expect(
            self.page.locator("#target_department_after_sign .MuiChip-label")
        ).to_have_text(
            [
                "Министерство внутренней политики, информации и связи Республики Крым",
                "Министерство сэд 2.0",
                "Тестовая Орга 999",
            ]
        )
        expect(
            self.page.locator("#document_type_field_meeting_region .MuiChip-label")
        ).to_have_text(
            [
                '40 | ГБУ РК "Крымский академический театр кукол"',
                '42 | ГБУ РК "Крымский киномедиацентр"',
            ]
        )
        expect(
            self.page.locator("#document_type_field_meeting .MuiChip-label")
        ).to_have_text(["21 | Первомайский р-н", "17 | Красногвардейский р-н"])
        expect(self.page.locator("#show_signature .ViewSwitch-Switch")).to_have_text(
            "Да"
        )
        expect(self.page.locator("#urgent .ViewSwitch-Switch")).to_have_text("Heт")
        expect(self.page.locator("#date_doc input")).to_have_value("12.04.2026")
        expect(self.page.locator("#date_from input")).to_have_value("12.04.2026")
        expect(self.page.locator("#date_year input")).to_have_value("2026")
        expect(self.page.locator("#from .MuiChip-label")).to_have_text(
            "Ответственный Первый Пользователь | Автотестовая Родительская организация"
        )
        expect(self.page.locator("#doc_type textarea:visible")).to_have_value(
            "Тест типа"
        )
        expect(
            self.page.locator("#office_class_view_docs .MuiChip-label")
        ).to_have_text("126 | Распоряжение Правительства Российской Федерации")
        expect(self.page.locator("#doc_num textarea:visible")).to_have_value(
            "тест номера"
        )
        expect(self.page.locator("#link_to_num textarea:visible")).to_have_value(
            "Тест ссылки"
        )
        expect(self.page.locator("#data_experiment input")).to_have_value("12.04.2026")
        expect(self.page.locator("#whom .MuiChip-label")).to_have_text(
            "Обычный Первый Пользователь | Автотестовая Родительская организация"
        )
        expect(self.page.locator("#target_department .MuiChip-label")).to_have_text(
            "Министерство внутренней политики, информации и связи Республики Крым"
        )
        expect(self.page.locator("#responsible_performer .MuiChip-label")).to_have_text(
            "Ответственный Первый Пользователь | Автотестовая Родительская организация"
        )
        expect(self.page.locator("#signature input")).to_have_value("П. Обычный")
        expect(self.page.locator("#position textarea:visible")).to_have_value(
            "Вторая автотестовая должность"
        )
        expect(self.page.locator("#coordinator_name input")).to_have_value(
            "П. Ответственный"
        )
        expect(self.page.locator("#number_64_test textarea:visible")).to_have_value(
            "1234567890"
        )
        expect(self.page.locator("#coordinator_pos textarea:visible")).to_have_value(
            "Первая автотестовая должность"
        )
        expect(
            self.page.locator(
                "#send_forward_after_signature .PropsViewWorkerPickerSelect-UserList"
            )
        ).to_have_text("Обычный П.П.")
        expect(
            self.page.locator(
                "#users_my_org_test .PropsViewWorkerPickerSelect-UserList"
            )
        ).to_have_text("Ответственный П.П.")
        expect(self.page.locator("#by_attorney textarea:visible")).to_have_value(
            "Тест доверенности"
        )
        expect(self.page.locator("#office_class_topics .MuiChip-label")).to_have_text(
            "115 | Работа РГА, исполкомов горсоветов, сельских и поселковых советов"
        )
        expect(self.page.locator("#office_class_corrs .MuiChip-label")).to_have_text(
            "123 | Управление делами Президента Российской Федерации"
        )
        expect(self.page.locator("#print_font_size_pt .MuiChip-label")).to_have_text(
            "14 шрифт"
        )
        expect(self.page.locator("#smrkdocinfo textarea:visible")).to_have_value(
            "Тест информации"
        )

    def assert_description_contain_text(self, field_name, expected_text):
        locator = self.page.locator(
            f"div.CustomSpoiler:has(.CustomSpoiler-Title:text-is('{field_name}')) div.Document-ContentView"
        )
        expect(locator).to_contain_text(expected_text)

    def assert_fields_have_values(self, fields_values):
        for field_name, expected_value in fields_values.items():
            if field_name in ("Краткое описание:", "Содержимое:"):
                self.assert_description_contain_text(field_name, expected_value)
            else:
                self.assert_field_has_value(field_name, expected_value)

    def assert_system_fields_have_values(self, user_information):
        current_date = self.generate_date_offset_days()
        self.assert_field_has_value("Дата создания в системе", current_date)

        document_author = user_information.split(" | ", 1)[0]
        self.assert_field_has_value("Автор документа", document_author)

        self.assert_field_has_value("Статус Документа", "Открыт")

    # def example_method(self, expected_data):

    def assert_field_has_value_by_id(self, field_id: str, expected_val):

        container = self.page.locator(f"#{field_id}")
        expect(container).to_be_visible()
        # 1. Поля ввода (input или textarea) -> значение лежит в атрибуте value

        input_elem = container.locator("input:not([type='hidden']), textarea").first
        if input_elem.count() > 0:
            if isinstance(expected_val, list):
                expected_val = expected_val[0]
            expect(input_elem).to_have_value(str(expected_val))
            return

        # 2. Множественные чипы / теги (.MuiChip-label)
        chips = container.locator(".MuiChip-label")
        if chips.count() > 0:
            if isinstance(expected_val, list):
                for val in expected_val:
                    expect(chips.filter(has_text=val)).to_be_visible()
            else:
                expect(chips.filter(has_text=expected_val)).to_be_visible()
            return

        # 3. Переключатели (Да / Нет)
        switch = container.locator(".ViewSwitch-Switch")
        if switch.count() > 0:
            expect(switch).to_have_text(str(expected_val))
            return

        # 4. Fallback: поиск по тексту внутри всего контейнера поля
        # (подходит для списков пользователей вида PropsViewWorkerPickerSelect-UserList)
        if isinstance(expected_val, list):
            for val in expected_val:
                expect(container).to_contain_text(val)
        else:
            expect(container).to_contain_text(str(expected_val))

    def assert_fields_have_values_by_id(self, fields_dict: dict):
        for field_id, expected_value in fields_dict.items():
            self.assert_field_has_value_by_id(field_id, expected_value)
