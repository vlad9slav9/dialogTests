from pages.main_page import MainPage

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


def test_autofill_default_fields_when_creating_a_document(main_page_with_responsible):
    user_information = main_page_with_responsible.get_basic_user_information()
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.assert_outgoing_document_creation_tab_visible()
    doc_create_page.assert_default_field_are_filled(user_information)

def test_change_default_date_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    future_date = doc_create_page.change_date_via_calendar('Срок исполнения')
    doc_create_page.assert_field_has_value('Срок исполнения *', future_date)
    doc_create_page.change_date_in_property('Дата документа *', -15)
    new_year = doc_create_page.change_date_via_calendar('Год', is_year=True)
    doc_create_page.assert_field_has_value('Год', new_year)
    past_date = doc_create_page.change_date_via_calendar('Дата от', future_date=False)
    doc_create_page.assert_field_has_value('Дата от', past_date)


def test_create_document_with_all_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.fill_all_not_default_fields()
    doc_create_page.check_not_default_checkboxes()
    doc_create_page.click_bottom_save_button()

def test_create_document_with_only_required_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Входящий (Автотест)')
    doc_create_page.fill_required_fields()
    doc_create_page.click_upper_save_button()

def test_create_document_via_upper_edit_button(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий МЭДО (Автотест)')
    doc_create_page.fill_short_description()
    doc_create_page.click_upper_edit_button()

def test_create_document_via_bottom_edit_button(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Внутренний. Без Шаблона Печати (Автотест)')
    doc_create_page.fill_short_description()
    doc_create_page.click_bottom_edit_button()

def test_click_upper_save_button_without_filling_required_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.click_upper_save_button()
    doc_create_page.assert_field_filling_error_displayed()

def test_click_bottom_save_button_without_filling_required_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Входящий (Автотест)')
    doc_create_page.click_bottom_save_button()
    doc_create_page.assert_field_filling_error_displayed()

def test_click_bottom_edit_button_without_filling_required_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий МЭДО (Автотест)')
    doc_create_page.click_bottom_edit_button()
    doc_create_page.assert_field_filling_error_displayed()

def test_click_upper_edit_button_without_filling_required_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Внутренний. Без Шаблона Печати (Автотест)')
    doc_create_page.click_upper_edit_button()
    doc_create_page.assert_field_filling_error_displayed()

def test_change_print_template(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.assert_field_has_value('Шаблон (для печати) *', 'Первый автотестовый шаблон')
    doc_create_page.change_print_template('второй')
    doc_create_page.assert_field_has_value('Шаблон (для печати) *', 'Второй для печати')
def test_search_nonexistent_print_template(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.assert_field_has_value('Шаблон (для печати) *', 'Первый автотестовый шаблон')
    doc_create_page.clear_classifier('Шаблон (для печати) *')
    doc_create_page.enter_text_in_the_classifier('Шаблон (для печати) *','второй несуществующий')
    doc_create_page.assert_dropdown_list_without_options()
def test_check_empty_print_template(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Внутренний. Без Шаблона Печати (Автотест)')
    doc_create_page.assert_field_is_empty('Шаблон (для печати)')
    doc_create_page.click_classifier('Шаблон (для печати)')
    doc_create_page.assert_dropdown_list_without_options()

def test_fill_content_editor_via_content_template(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.assert_content_editor_is_empty()
    doc_create_page.select_content_template('Первый шаблон для Исходящего документа')
    doc_create_page.assert_content_editor_has_first_template()
    doc_create_page.select_content_template('Второй свой шаблон для Исходящего документа')
    doc_create_page.assert_content_editor_has_two_templates()

def test_select_empty_content_template(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.select_content_template('Без шаблона')
    doc_create_page.assert_content_editor_is_empty()

def test_search_option_in_classifier(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.enter_text_in_the_classifier('Вид документа *','9')
    doc_create_page.assert_dropdown_list_contain_text('9')
    doc_create_page.enter_text_in_the_classifier('Тематика', 'Тест')
    doc_create_page.assert_dropdown_list_contain_text('Тест')
    doc_create_page.enter_text_in_the_classifier('Корреспондент', '9999 | Тест значение')
    doc_create_page.assert_dropdown_list_contain_text('9999 | Тест значение')
    doc_create_page.enter_text_in_the_classifier('Размер шрифта(при печати)', '13')
    doc_create_page.assert_dropdown_list_contain_text('13')

def test_search_user_in_creation_document_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.clear_multivalues_field('От кого')
    doc_create_page.assert_picker_contain_users('От кого', doc_create_page.cross_department_users)
    doc_create_page.assert_picker_contain_users('Кому', doc_create_page.cross_department_users)
    doc_create_page.assert_picker_contain_users('Подпись', doc_create_page.users_with_mku_and_curators)
    doc_create_page.assert_picker_not_contain_users('Подпись', doc_create_page.users_from_other_departments)
    doc_create_page.assert_picker_contain_users('Имя согласователя', doc_create_page.users_with_mku_and_curators)
    doc_create_page.assert_picker_not_contain_users('Имя согласователя', doc_create_page.users_from_other_departments)
    doc_create_page.assert_picker_contain_users('Ответственный исполнитель', doc_create_page.cross_department_users)
    doc_create_page.assert_picker_contain_users('Получатели после подписания', doc_create_page.users_with_mku_and_curators)
    doc_create_page.assert_picker_not_contain_users('Получатели после подписания', doc_create_page.users_from_other_departments)
    doc_create_page.assert_picker_contain_users('Пользователи своей орги', doc_create_page.users_with_mku_and_curators, fill_field=False)
    doc_create_page.assert_picker_not_contain_users('Пользователи своей орги', doc_create_page.users_from_other_departments, fill_field=False)

def test_search_user_in_creation_document_medo_fields(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий МЭДО (Автотест)')
    doc_create_page.clear_multivalues_field('От кого')
    doc_create_page.assert_picker_contain_users('От кого', doc_create_page.users_without_curators)
    doc_create_page.assert_picker_not_contain_users('От кого', doc_create_page.department_curators)
    doc_create_page.assert_picker_contain_users('Кому', doc_create_page.cross_department_users, fill_field=False)
    doc_create_page.assert_picker_contain_users('Подпись', doc_create_page.cross_department_users, fill_field=False)
    doc_create_page.assert_picker_contain_users('Имя согласователя', doc_create_page.cross_department_users, fill_field=False)
    doc_create_page.assert_picker_contain_users('Ответственный исполнитель', doc_create_page.cross_department_users, fill_field=False)
    doc_create_page.assert_picker_contain_users('Получатели после подписания', doc_create_page.users_with_mku)
    doc_create_page.assert_picker_not_contain_users('Получатели после подписания', doc_create_page.curators_and_other_departments)
    doc_create_page.assert_picker_contain_users('Пользователи своей орги', doc_create_page.users_with_mku_and_curators)
    doc_create_page.assert_picker_not_contain_users('Пользователи своей орги', doc_create_page.users_from_other_departments)

def test_retest(main_page_with_responsible):
    doc_create_page = main_page_with_responsible.open_doc_create_page('Исходящий (Автотест)')
    doc_create_page.test_example()








