import pytest

from pages.components.layout_component import LayoutComponent


def test_open_document_creation_window(responsible_user: LayoutComponent):
    responsible_user.click_quick_doc_create_button()
    responsible_user.assert_doc_create_window_visible()


def test_cancel_document_creation_window(responsible_user: LayoutComponent):
    responsible_user.click_quick_doc_create_button()
    responsible_user.click_cancel_doc_create_button()
    responsible_user.assert_doc_create_window_hidden()


def test_close_document_creation_window(responsible_user: LayoutComponent):
    responsible_user.click_quick_doc_create_button()
    responsible_user.click_close_doc_create_button()
    responsible_user.assert_doc_create_window_hidden()


def test_search_document_type_in_document_creation_window(
    responsible_user: LayoutComponent,
):
    responsible_user.click_quick_doc_create_button()
    responsible_user.click_doc_type_select_field()
    responsible_user.assert_dropdown_list_contain_options("Исходящий (Автотест)")
    responsible_user.assert_dropdown_list_contain_options("Исходящий МЭДО (Автотест)")
    responsible_user.assert_dropdown_list_contain_options("Входящий (Автотест)")
    responsible_user.assert_dropdown_list_contain_options(
        "Внутренний. Без Шаблона Печати (Автотест)"
    )
    responsible_user.fill_doc_type_search_field("исходящий")
    responsible_user.assert_dropdown_list_contain_options("Исходящий (Автотест)")
    responsible_user.assert_dropdown_list_contain_options("Исходящий МЭДО (Автотест)")
    responsible_user.assert_dropdown_list_not_contain_options("Входящий (Автотест)")
    responsible_user.assert_dropdown_list_not_contain_options(
        "Внутренний. Без Шаблона Печати (Автотест)"
    )


def test_search_nonexistent_document_type(responsible_user: LayoutComponent):
    responsible_user.click_quick_doc_create_button()
    responsible_user.click_doc_type_select_button()
    responsible_user.fill_doc_type_search_field("Негативный тест")
    responsible_user.assert_dropdown_list_without_options()


def test_reselect_document_type_in_document_creation_window(
    responsible_user: LayoutComponent,
):
    responsible_user.click_quick_doc_create_button()
    responsible_user.click_doc_type_select_button()
    responsible_user.select_doc_type("Исходящий (Автотест)")
    responsible_user.assert_doc_option_selected("Исходящий (Автотест)")
    responsible_user.click_doc_type_select_field()
    responsible_user.assert_dropdown_list_not_contain_options("Исходящий (Автотест)")
    responsible_user.assert_dropdown_list_contain_options("Входящий (Автотест)")
    responsible_user.assert_dropdown_list_contain_options("Исходящий МЭДО (Автотест)")
    responsible_user.assert_dropdown_list_contain_options(
        "Внутренний. Без Шаблона Печати (Автотест)"
    )
    responsible_user.select_doc_type("Входящий (Автотест)")
    responsible_user.assert_doc_option_selected("Входящий (Автотест)")


def test_create_document_button_disabled_after_clearing_field(
    responsible_user: LayoutComponent,
):
    responsible_user.click_quick_doc_create_button()
    responsible_user.assert_doc_type_search_field_is_empty()
    responsible_user.assert_create_doc_button_disabled()
    responsible_user.click_doc_type_select_field()
    responsible_user.select_doc_type("Входящий (Автотест)")
    responsible_user.assert_doc_option_selected("Входящий (Автотест)")
    responsible_user.assert_create_doc_button_enabled()
    responsible_user.click_doc_type_search_field_clear_button()
    responsible_user.assert_doc_type_search_field_is_empty()
    responsible_user.assert_create_doc_button_disabled()


def test_autofill_default_fields(responsible_user: LayoutComponent):
    user_information = responsible_user.get_basic_user_information()
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.assert_document_creation_tab_visible("Исходящий (Автотест)")
    doc_edit_page.assert_default_fields_are_filled(user_information)


def test_change_print_template(responsible_user: LayoutComponent):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.assert_field_is_filled(
        "Шаблон (для печати) *", "Первый автотестовый шаблон"
    )
    doc_edit_page.change_print_template("второй")
    doc_edit_page.assert_field_is_filled("Шаблон (для печати) *", "Второй для печати")


def test_search_nonexistent_print_template(
    responsible_user: LayoutComponent,
):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.assert_field_is_filled(
        "Шаблон (для печати) *", "Первый автотестовый шаблон"
    )
    doc_edit_page.clear_classifier_by_name("Шаблон (для печати) *")
    doc_edit_page.enter_text_in_the_classifier(
        "Шаблон (для печати) *", "второй несуществующий"
    )
    doc_edit_page.assert_dropdown_list_without_options()


def test_check_empty_print_template(responsible_user: LayoutComponent):
    doc_edit_page = responsible_user.open_doc_edit_page(
        "Внутренний. Без Шаблона Печати (Автотест)"
    )
    doc_edit_page.assert_field_is_empty_by_name("Шаблон (для печати)")
    doc_edit_page.click_classifier("Шаблон (для печати)")
    doc_edit_page.assert_dropdown_list_without_options()


def test_fill_content_editor_via_content_template(
    responsible_user: LayoutComponent,
):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.assert_content_editor_is_empty()
    doc_edit_page.select_content_template("Первый шаблон для Исходящего документа")
    doc_edit_page.assert_content_editor_has_text(
        "Автотест для проверки добавления первого шаблона содержимого!"
    )
    doc_edit_page.select_content_template("Второй свой шаблон для Исходящего документа")
    doc_edit_page.assert_content_editor_has_text(
        "Автотест для проверки добавления первого шаблона содержимого!"
        "Это второй шаблон для автотеста, который проверяет, что добавляется второй шаблон в дополнении к первому"
    )


def test_select_empty_content_template(responsible_user: LayoutComponent):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.select_content_template("Без шаблона")
    doc_edit_page.assert_content_editor_is_empty()


@pytest.mark.parametrize(
    "field_name",
    [
        "Вид документа",
        "Тематика",
        "Корреспондент",
        "Встреча с коллективами предприятий",
        "Выездные совещания",
        "Размер шрифта(при печати)",
    ],
)
def test_search_option_in_classifier(responsible_user: LayoutComponent, field_name):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.enter_text_in_the_classifier(field_name, "тест значение")
    doc_edit_page.assert_dropdown_list_contain_text("тест значение")
    doc_edit_page.assert_dropdown_list_not_contain_text("негативная проверка")


def test_fill_organization_classifier_via_group(
    responsible_user: LayoutComponent,
):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.fill_classifier_group(
        "Выберите группу", "Автотестовая группа из профиля"
    )
    doc_edit_page.assert_field_is_filled(
        "target_department_after_sign",
        doc_edit_page.group_with_organizations_from_profile,
        is_multiform=True,
    )
    doc_edit_page.clear_group_field_by_id("target_department_after_sign")
    doc_edit_page.assert_group_and_field_is_empty("target_department_after_sign")


def test_fill_user_classifier_via_grop(responsible_user: LayoutComponent):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.fill_classifier_group(
        "Добавить из группы", "Пользователи моей организации"
    )
    doc_edit_page.assert_field_is_filled(
        "send_forward_after_signature",
        doc_edit_page.department_users,
        is_multiform=True,
    )
    doc_edit_page.clear_group_field_by_id("send_forward_after_signature")
    doc_edit_page.assert_group_and_field_is_empty("send_forward_after_signature")


@pytest.mark.parametrize(
    "main_field, second_field",
    [("signature", "position"), ("coordinator_name", "coordinator_pos")],
)
def test_autofill_position_classifier(
    responsible_user: LayoutComponent, main_field, second_field
):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.fill_classifier_by_id(main_field, doc_edit_page.department_users[0])
    doc_edit_page.assert_field_is_filled(
        second_field,
        doc_edit_page.extract_user_parts(
            doc_edit_page.department_users[0], parts="position"
        ),
    )
    doc_edit_page.clear_classifier_by_id(main_field)
    doc_edit_page.assert_field_is_empty_by_id(main_field)
    doc_edit_page.assert_field_is_empty_by_id(second_field)
    doc_edit_page.fill_classifier_by_id(main_field, doc_edit_page.department_users[1])
    doc_edit_page.assert_field_is_filled(
        second_field,
        doc_edit_page.extract_user_parts(
            doc_edit_page.department_users[1], parts="position"
        ),
    )


def test_search_user_in_creation_document_fields(
    responsible_user: LayoutComponent,
):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.clear_multivalues_field("От кого")
    doc_edit_page.assert_picker_contain_users(
        "От кого", doc_edit_page.cross_department_users
    )
    doc_edit_page.assert_picker_contain_users(
        "Кому", doc_edit_page.cross_department_users
    )
    doc_edit_page.assert_picker_contain_users(
        "Подпись", doc_edit_page.users_with_mku_and_curators
    )
    doc_edit_page.assert_picker_not_contain_users(
        "Подпись", doc_edit_page.users_from_other_departments
    )
    doc_edit_page.assert_picker_contain_users(
        "Имя согласователя", doc_edit_page.users_with_mku_and_curators
    )
    doc_edit_page.assert_picker_not_contain_users(
        "Имя согласователя", doc_edit_page.users_from_other_departments
    )
    doc_edit_page.assert_picker_contain_users(
        "Ответственный исполнитель", doc_edit_page.cross_department_users
    )
    doc_edit_page.assert_picker_contain_users(
        "Получатели после подписания", doc_edit_page.users_with_mku_and_curators
    )
    doc_edit_page.assert_picker_not_contain_users(
        "Получатели после подписания", doc_edit_page.users_from_other_departments
    )
    doc_edit_page.assert_picker_contain_users(
        "Пользователи своей орги",
        doc_edit_page.users_with_mku_and_curators,
        fill_field=False,
    )
    doc_edit_page.assert_picker_not_contain_users(
        "Пользователи своей орги",
        doc_edit_page.users_from_other_departments,
        fill_field=False,
    )


def test_search_user_in_creation_document_medo_fields(
    responsible_user: LayoutComponent,
):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий МЭДО (Автотест)")
    doc_edit_page.clear_multivalues_field("От кого")
    doc_edit_page.assert_picker_contain_users(
        "От кого", doc_edit_page.users_without_curators
    )
    doc_edit_page.assert_picker_not_contain_users(
        "От кого", doc_edit_page.department_curators
    )
    doc_edit_page.assert_picker_contain_users(
        "Кому", doc_edit_page.cross_department_users, fill_field=False
    )
    doc_edit_page.assert_picker_contain_users(
        "Подпись", doc_edit_page.cross_department_users, fill_field=False
    )
    doc_edit_page.assert_picker_contain_users(
        "Имя согласователя", doc_edit_page.cross_department_users, fill_field=False
    )
    doc_edit_page.assert_picker_contain_users(
        "Ответственный исполнитель",
        doc_edit_page.cross_department_users,
        fill_field=False,
    )
    doc_edit_page.assert_picker_contain_users(
        "Получатели после подписания", doc_edit_page.users_with_mku
    )
    doc_edit_page.assert_picker_not_contain_users(
        "Получатели после подписания", doc_edit_page.curators_and_other_departments
    )
    doc_edit_page.assert_picker_contain_users(
        "Пользователи своей орги", doc_edit_page.users_with_mku_and_curators
    )
    doc_edit_page.assert_picker_not_contain_users(
        "Пользователи своей орги", doc_edit_page.users_from_other_departments
    )


def test_create_document_with_all_fields(responsible_user: LayoutComponent):
    user_information = responsible_user.get_basic_user_information()
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_view_page, fields_values = doc_edit_page.create_document(user_information)
    doc_edit_page.assert_snackbar_displayed("Документ создан")
    doc_view_page.assert_fields_have_values(fields_values)
    doc_view_page.assert_system_fields_have_values(user_information)


def test_create_document_with_only_required_fields(
    responsible_user: LayoutComponent,
):
    user_information = responsible_user.get_basic_user_information()
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_view_page, fields_values = doc_edit_page.create_document(
        user_information, only_required_fields=True
    )
    doc_edit_page.assert_snackbar_displayed("Документ создан")
    doc_view_page.assert_fields_have_values(fields_values)
    doc_view_page.assert_system_fields_have_values(user_information)


@pytest.mark.parametrize(
    "save_action",
    [
        "click_upper_save_button",
        "click_upper_edit_button",
        "click_bottom_save_button",
        "click_bottom_edit_button",
    ],
)
def test_create_document(responsible_user: LayoutComponent, save_action):
    doc_edit_page = responsible_user.open_doc_edit_page(
        "Внутренний. Без Шаблона Печати (Автотест)"
    )
    doc_edit_page.fill_short_description()
    getattr(doc_edit_page, save_action)()
    doc_edit_page.assert_document_tab_visible("Редактирование документа №")
    doc_edit_page.assert_snackbar_displayed("Документ создан")


@pytest.mark.parametrize(
    "save_action",
    [
        "click_upper_save_button",
        "click_upper_edit_button",
        "click_bottom_save_button",
        "click_bottom_edit_button",
    ],
)
def test_save_document_without_filling_required_fields(
    responsible_user: LayoutComponent, save_action
):
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_edit_page.clear_property("Срок исполнения *")
    doc_edit_page.clear_property("Дата документа *")
    doc_edit_page.clear_print_template()
    getattr(doc_edit_page, save_action)()
    doc_edit_page.assert_document_creation_tab_visible("Исходящий (Автотест)")
    doc_edit_page.assert_required_field_error_displayed(
        "Срок исполнения должен быть датой"
    )
    doc_edit_page.assert_required_field_error_displayed(
        'Значение поля "Дата документа" должно быть датой'
    )
    doc_edit_page.assert_required_field_error_displayed(
        'Значение поля "Тип документа" не может быть пустым.'
    )
    doc_edit_page.assert_required_field_error_displayed(
        'Значение поля "№ документа" не может быть пустым.'
    )
    doc_edit_page.assert_required_field_error_displayed(
        'Значение поля "Вид документа" не может быть пустым.'
    )
    doc_edit_page.assert_required_field_error_displayed(
        'Значение поля "Краткое описание" не может быть пустым.'
    )
    doc_edit_page.assert_required_field_error_displayed(
        'Значение поля "Шаблон (для печати)" не может быть пустым.'
    )
    doc_edit_page.assert_snackbar_displayed("Не все поля заполнены корректно.")


def test_edit_document(responsible_user: LayoutComponent):
    user_information = responsible_user.get_basic_user_information()
    doc_edit_page = responsible_user.open_doc_edit_page("Исходящий (Автотест)")
    doc_view_page, fields_values = doc_edit_page.create_document(user_information)
    doc_view_page.click_edit_button()
    doc_edit_page.assert_document_tab_visible("Редактирование документа  № АвтоИсход")
    doc_edit_page.clear_editable_fields()
    doc_edit_page.fill_empty_fields()


def test_retest(responsible_user: LayoutComponent):
    user_information = responsible_user.get_basic_user_information()
    doc_edit_page = responsible_user.open_doc_edit_page(
        "Исходящий (Автотест)", user_information
    )
    doc_edit_page.create_document()
