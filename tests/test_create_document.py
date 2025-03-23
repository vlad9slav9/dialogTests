from pages.main_page import MainPage

def test_open_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.assert_document_creation_window_visible()


def test_cancel_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.click_cancel_document_creation_button()
    main_page_with_responsible.assert_document_creation_window_hidden()


def test_close_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.click_close_document_creation_button()
    main_page_with_responsible.assert_document_creation_window_hidden()


def test_search_document_type_in_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.click_document_type_selection_field()
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Входящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Внутренний. Без Шаблона Печати (Автотест)')
    main_page_with_responsible.fill_document_type_search_field('исходящий')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_dropdown_list_not_contain_options('Входящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_not_contain_options('Внутренний. Без Шаблона Печати (Автотест)')


def test_search_nonexistent_document_type(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.click_document_type_selection_button()
    main_page_with_responsible.fill_document_type_search_field('Негативный тест')
    main_page_with_responsible.assert_dropdown_list_without_options()


def test_reselect_document_type_in_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.click_document_type_selection_button()
    main_page_with_responsible.select_document_type('Исходящий (Автотест)')
    main_page_with_responsible.assert_document_option_selected('Исходящий (Автотест)')
    main_page_with_responsible.click_document_type_selection_field()
    main_page_with_responsible.assert_dropdown_list_not_contain_options('Исходящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Входящий (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_dropdown_list_contain_options('Внутренний. Без Шаблона Печати (Автотест)')
    main_page_with_responsible.select_document_type('Входящий (Автотест)')
    main_page_with_responsible.assert_document_option_selected('Входящий (Автотест)')


def test_create_document_button_disabled_after_clearing_field(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.assert_document_type_search_field_is_empty()
    main_page_with_responsible.assert_create_document_button_disabled()
    main_page_with_responsible.click_document_type_selection_field()
    main_page_with_responsible.select_document_type('Входящий (Автотест)')
    main_page_with_responsible.assert_document_option_selected('Входящий (Автотест)')
    main_page_with_responsible.assert_create_document_button_enabled()
    main_page_with_responsible.click_document_type_search_field_clear_button()
    main_page_with_responsible.assert_document_type_search_field_is_empty()
    main_page_with_responsible.assert_create_document_button_disabled()


def test_autofill_default_fields_when_creating_a_document(main_page_with_responsible):
    user_information = main_page_with_responsible.get_basic_user_information()
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.assert_outgoing_document_creation_tab_visible()
    document_creation_page.assert_default_field_are_filled(user_information)


def test_create_document_with_all_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.fill_all_not_default_fields()
    document_creation_page.check_not_default_checkboxes()
    document_creation_page.click_bottom_save_button()

def test_create_document_with_only_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Входящий (Автотест)')
    document_creation_page.fill_required_fields()
    document_creation_page.click_upper_save_button()

def test_create_document_via_upper_edit_button(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий МЭДО (Автотест)')
    document_creation_page.fill_short_description()
    document_creation_page.click_upper_edit_button()

def test_create_document_via_bottom_edit_button(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Внутренний. Без Шаблона Печати (Автотест)')
    document_creation_page.fill_short_description()
    document_creation_page.click_bottom_edit_button()

def test_click_upper_save_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.click_upper_save_button()
    document_creation_page.assert_field_filling_error_displayed()

def test_click_bottom_save_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Входящий (Автотест)')
    document_creation_page.click_bottom_save_button()
    document_creation_page.assert_field_filling_error_displayed()

def test_click_bottom_edit_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий МЭДО (Автотест)')
    document_creation_page.click_bottom_edit_button()
    document_creation_page.assert_field_filling_error_displayed()

def test_click_upper_edit_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Внутренний. Без Шаблона Печати (Автотест)')
    document_creation_page.click_upper_edit_button()
    document_creation_page.assert_field_filling_error_displayed()

#def test_change_default_fields(main_page_with_responsible):




def test_change_print_template(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.assert_field_has_value('Шаблон (для печати) *', 'Первый автотестовый шаблон')
    document_creation_page.change_print_template('второй')
    document_creation_page.assert_field_has_value('Шаблон (для печати) *', 'Второй для печати')
def test_search_nonexistent_print_template(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.assert_field_has_value('Шаблон (для печати) *', 'Первый автотестовый шаблон')
    document_creation_page.clear_classifier('Шаблон (для печати) *')
    document_creation_page.enter_text_in_the_classifier('Шаблон (для печати) *','второй несуществующий')
    document_creation_page.assert_dropdown_list_without_options()
def test_check_empty_print_template(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Внутренний. Без Шаблона Печати (Автотест)')
    document_creation_page.assert_field_is_empty('Шаблон (для печати)')
    document_creation_page.click_classifier('Шаблон (для печати)')
    document_creation_page.assert_dropdown_list_without_options()

def test_fill_content_editor_via_content_template(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.assert_content_editor_is_empty()
    document_creation_page.select_first_content_template()
    document_creation_page.assert_content_editor_has_first_template()
    document_creation_page.select_second_content_template()
    document_creation_page.assert_content_editor_has_two_templates()

def test_select_empty_content_template(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.select_empty_content_template()
    document_creation_page.assert_content_editor_is_empty()

def test_search_option_in_classifier(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.enter_text_in_the_classifier('Вид документа *','9')
    document_creation_page.assert_dropdown_list_contain_text('9')
    document_creation_page.enter_text_in_the_classifier('Тематика', 'Тест')
    document_creation_page.assert_dropdown_list_contain_text('Тест')
    document_creation_page.enter_text_in_the_classifier('Корреспондент', '9999 | Тест значение')
    document_creation_page.assert_dropdown_list_contain_text('9999 | Тест значение')
    document_creation_page.enter_text_in_the_classifier('Размер шрифта(при печати)', '13')
    document_creation_page.assert_dropdown_list_contain_text('13')


def test_example(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.click_classifier('Кому')
    document_creation_page.assert_picker_contain_all_users()
    document_creation_page.click_classifier('Подпись')
    document_creation_page.assert_picker_contain_users_with_curators_and_mku()
    document_creation_page.assert_picker_not_contain_users_from_other_departments()
    document_creation_page.click_classifier('Имя согласователя')
    document_creation_page.assert_picker_contain_users_with_curators_and_mku()
    document_creation_page.assert_picker_not_contain_users_from_other_departments()
    document_creation_page.click_classifier('Ответственный исполнитель')
    document_creation_page.assert_picker_contain_all_users()
    document_creation_page.click_classifier('Пользователи своей орги')
    document_creation_page.assert_picker_contain_users_with_curators_and_mku()
    document_creation_page.assert_picker_not_contain_users_from_other_departments()

def test_retest(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_document_creation_page('Исходящий (Автотест)')
    document_creation_page.assert_picker_contain_department_users('Кому')







