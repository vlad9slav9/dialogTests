from pages.main_page import MainPage
import pytest

def test_open_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_doc_create_button()
    main_page_with_responsible.assert_doc_create_window_visible()


def test_cancel_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_doc_create_button()
    main_page_with_responsible.click_cancel_doc_create_button()
    main_page_with_responsible.assert_doc_create_window_hidden()


def test_close_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_doc_create_button()
    main_page_with_responsible.click_close_doc_create_button()
    main_page_with_responsible.assert_doc_create_window_hidden()


def test_search_document_type_in_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_doc_create_button()
    main_page_with_responsible.click_doc_type_select_field()
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Входящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Внутренний. Без Шаблона Печати (Автотест)')
    main_page_with_responsible.fill_doc_type_search_field('исходящий')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_dropdown_list_not_contain_options('Входящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_not_contain_options('Внутренний. Без Шаблона Печати (Автотест)')


def test_search_nonexistent_document_type(main_page_with_responsible):
    main_page_with_responsible.click_quick_doc_create_button()
    main_page_with_responsible.click_doc_type_select_button()
    main_page_with_responsible.fill_doc_type_search_field('Негативный тест')
    main_page_with_responsible.assert_dropdown_list_without_options()


def test_reselect_document_type_in_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_doc_create_button()
    main_page_with_responsible.click_doc_type_select_button()
    main_page_with_responsible.select_doc_type('Исходящий (Автотест)')
    main_page_with_responsible.assert_doc_option_selected('Исходящий (Автотест)')
    main_page_with_responsible.click_doc_type_select_field()
    main_page_with_responsible.assert_dropdown_list_not_contain_options('Исходящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Входящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Внутренний. Без Шаблона Печати (Автотест)')
    main_page_with_responsible.select_doc_type('Входящий (Автотест)')
    main_page_with_responsible.assert_doc_option_selected('Входящий (Автотест)')


def test_create_document_button_disabled_after_clearing_field(main_page_with_responsible):
    main_page_with_responsible.click_quick_doc_create_button()
    main_page_with_responsible.assert_doc_type_search_field_is_empty()
    main_page_with_responsible.assert_create_doc_button_disabled()
    main_page_with_responsible.click_doc_type_select_field()
    main_page_with_responsible.select_doc_type('Входящий (Автотест)')
    main_page_with_responsible.assert_doc_option_selected('Входящий (Автотест)')
    main_page_with_responsible.assert_create_doc_button_enabled()
    main_page_with_responsible.click_doc_type_search_field_clear_button()
    main_page_with_responsible.assert_doc_type_search_field_is_empty()
    main_page_with_responsible.assert_create_doc_button_disabled()

def test_autofill_default_fields(main_page_with_responsible):
    user_information = main_page_with_responsible.get_basic_user_information()
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.assert_document_creation_tab_visible('Исходящий (Автотест)')
    doc_edit_page.assert_default_fields_are_filled(user_information)

def test_change_print_template(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.assert_field_is_filled('Шаблон (для печати) *', 'Первый автотестовый шаблон')
    doc_edit_page.change_print_template('второй')
    doc_edit_page.assert_field_is_filled('Шаблон (для печати) *', 'Второй для печати')
def test_search_nonexistent_print_template(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.assert_field_is_filled('Шаблон (для печати) *', 'Первый автотестовый шаблон')
    doc_edit_page.clear_classifier('Шаблон (для печати) *')
    doc_edit_page.enter_text_in_the_classifier('Шаблон (для печати) *', 'второй несуществующий')
    doc_edit_page.assert_dropdown_list_without_options()
def test_check_empty_print_template(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Внутренний. Без Шаблона Печати (Автотест)')
    doc_edit_page.assert_field_is_empty('Шаблон (для печати)')
    doc_edit_page.click_classifier('Шаблон (для печати)')
    doc_edit_page.assert_dropdown_list_without_options()

def test_fill_content_editor_via_content_template(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.assert_content_editor_is_empty()
    doc_edit_page.select_content_template('Первый шаблон для Исходящего документа')
    doc_edit_page.assert_content_editor_has_text('Автотест для проверки добавления первого шаблона содержимого!')
    doc_edit_page.select_content_template('Второй свой шаблон для Исходящего документа')
    doc_edit_page.assert_content_editor_has_text("Автотест для проверки добавления первого шаблона содержимого!"
                                                  "Это второй шаблон для автотеста, который проверяет, что добавляется второй шаблон в дополнении к первому")

def test_select_empty_content_template(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.select_content_template('Без шаблона')
    doc_edit_page.assert_content_editor_is_empty()

def test_search_option_in_classifier(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.enter_text_in_the_classifier('Вид документа *','9')
    doc_edit_page.assert_dropdown_list_contain_text('9')
    doc_edit_page.enter_text_in_the_classifier('Тематика', 'Тест')
    doc_edit_page.assert_dropdown_list_contain_text('Тест')
    doc_edit_page.enter_text_in_the_classifier('Корреспондент', '9999 | Тест значение')
    doc_edit_page.assert_dropdown_list_contain_text('9999 | Тест значение')
    doc_edit_page.enter_text_in_the_classifier('Размер шрифта(при печати)', '13')
    doc_edit_page.assert_dropdown_list_contain_text('13')

def test_search_user_in_creation_document_fields(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.clear_multivalues_field('От кого')
    doc_edit_page.assert_picker_contain_users('От кого', doc_edit_page.cross_department_users)
    doc_edit_page.assert_picker_contain_users('Кому', doc_edit_page.cross_department_users)
    doc_edit_page.assert_picker_contain_users('Подпись', doc_edit_page.users_with_mku_and_curators)
    doc_edit_page.assert_picker_not_contain_users('Подпись', doc_edit_page.users_from_other_departments)
    doc_edit_page.assert_picker_contain_users('Имя согласователя', doc_edit_page.users_with_mku_and_curators)
    doc_edit_page.assert_picker_not_contain_users('Имя согласователя', doc_edit_page.users_from_other_departments)
    doc_edit_page.assert_picker_contain_users('Ответственный исполнитель', doc_edit_page.cross_department_users)
    doc_edit_page.assert_picker_contain_users('Получатели после подписания', doc_edit_page.users_with_mku_and_curators)
    doc_edit_page.assert_picker_not_contain_users('Получатели после подписания', doc_edit_page.users_from_other_departments)
    doc_edit_page.assert_picker_contain_users('Пользователи своей орги', doc_edit_page.users_with_mku_and_curators, fill_field=False)
    doc_edit_page.assert_picker_not_contain_users('Пользователи своей орги', doc_edit_page.users_from_other_departments, fill_field=False)

def test_search_user_in_creation_document_medo_fields(main_page_with_responsible):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий МЭДО (Автотест)')
    doc_edit_page.clear_multivalues_field('От кого')
    doc_edit_page.assert_picker_contain_users('От кого', doc_edit_page.users_without_curators)
    doc_edit_page.assert_picker_not_contain_users('От кого', doc_edit_page.department_curators)
    doc_edit_page.assert_picker_contain_users('Кому', doc_edit_page.cross_department_users, fill_field=False)
    doc_edit_page.assert_picker_contain_users('Подпись', doc_edit_page.cross_department_users, fill_field=False)
    doc_edit_page.assert_picker_contain_users('Имя согласователя', doc_edit_page.cross_department_users, fill_field=False)
    doc_edit_page.assert_picker_contain_users('Ответственный исполнитель', doc_edit_page.cross_department_users, fill_field=False)
    doc_edit_page.assert_picker_contain_users('Получатели после подписания', doc_edit_page.users_with_mku)
    doc_edit_page.assert_picker_not_contain_users('Получатели после подписания', doc_edit_page.curators_and_other_departments)
    doc_edit_page.assert_picker_contain_users('Пользователи своей орги', doc_edit_page.users_with_mku_and_curators)
    doc_edit_page.assert_picker_not_contain_users('Пользователи своей орги', doc_edit_page.users_from_other_departments)

def test_create_document_with_all_fields(main_page_with_responsible):
    user_information = main_page_with_responsible.get_basic_user_information()
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_view_page, fields_values = doc_edit_page.create_regular_document(user_information, all_fields=True)
    doc_edit_page.assert_snackbar_displayed('Документ создан')
    doc_view_page.assert_fields_have_values(fields_values)
    doc_view_page.assert_system_fields_have_values(user_information)

def test_create_document_with_only_required_fields(main_page_with_responsible):
    user_information = main_page_with_responsible.get_basic_user_information()
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_view_page, fields_values = doc_edit_page.create_regular_document(user_information, all_fields=False)
    doc_edit_page.assert_snackbar_displayed('Документ создан')
    doc_view_page.assert_fields_have_values(fields_values)
    doc_view_page.assert_system_fields_have_values(user_information)

@pytest.mark.parametrize(
    "save_action",
    [
        "click_upper_edit_button",
        "click_bottom_edit_button",
    ]
)
def test_create_document_via_edit_button(main_page_with_responsible, save_action):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Внутренний. Без Шаблона Печати (Автотест)')
    doc_edit_page.fill_short_description()
    getattr(doc_edit_page, save_action)()
    doc_edit_page.assert_document_tab_visible('Редактирование документа №')
    doc_edit_page.assert_snackbar_displayed('Документ создан')

@pytest.mark.parametrize(
    "save_action",
    [
        "click_upper_save_button",
        "click_upper_edit_button",
        "click_bottom_save_button",
        "click_bottom_edit_button",
    ]
)
def test_save_document_without_filling_required_fields(main_page_with_responsible, save_action):
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_edit_page.clear_property('Срок исполнения *')
    doc_edit_page.clear_property('Дата документа *')
    doc_edit_page.clear_print_template()
    getattr(doc_edit_page, save_action)()
    doc_edit_page.assert_document_creation_tab_visible('Исходящий (Автотест)')
    doc_edit_page.assert_required_field_error_displayed('Срок исполнения должен быть датой')
    doc_edit_page.assert_required_field_error_displayed('Значение поля "Дата документа" должно быть датой')
    doc_edit_page.assert_required_field_error_displayed('Значение поля "Тип документа" не может быть пустым.')
    doc_edit_page.assert_required_field_error_displayed('Значение поля "№ документа" не может быть пустым.')
    doc_edit_page.assert_required_field_error_displayed('Значение поля "Вид документа" не может быть пустым.')
    doc_edit_page.assert_required_field_error_displayed('Значение поля "Краткое описание" не может быть пустым.')
    doc_edit_page.assert_required_field_error_displayed('Значение поля "Шаблон (для печати)" не может быть пустым.')
    doc_edit_page.assert_snackbar_displayed('Не все поля заполнены корректно.')

def test_edit_document(main_page_with_responsible):
    user_information = main_page_with_responsible.get_basic_user_information()
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_view_page, fields_values = doc_edit_page.create_regular_document(user_information, all_fields=True)
    doc_view_page.click_edit_button()
    doc_edit_page.assert_document_tab_visible('Редактирование документа  № АвтоИсход')


# Сделать с редактируемыми полями во время создания / редактирования + дата документа на который ссылаемся для печати
# def test_change_default_date_fields(main_page_with_responsible):
#     doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
#     future_date = doc_create_page.change_date_via_calendar('Срок исполнения')
#     doc_create_page.assert_field_is_filled('Срок исполнения *', future_date)
#     doc_create_page.change_date_in_property('Дата документа *', -15)
#     new_year = doc_create_page.change_date_via_calendar('Год', is_year=True)
#     doc_create_page.assert_field_is_filled('Год', new_year)
#     past_date = doc_create_page.change_date_via_calendar('Дата от', future_date=False)
#     doc_create_page.assert_field_is_filled('Дата от', past_date)

def test_retest(main_page_with_responsible):
    user_information = main_page_with_responsible.get_basic_user_information()
    doc_edit_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_view_page, fields_values = doc_edit_page.create_regular_document(user_information, all_fields=True)
    doc_view_page.assert_fields_have_values(fields_values)
    doc_view_page.assert_system_fields_have_values(user_information)








