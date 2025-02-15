
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
    main_page_with_responsible.assert_document_option_visible('Исходящий (Автотест)')
    main_page_with_responsible.assert_document_option_visible('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_document_option_visible('Входящий (Автотест)')
    main_page_with_responsible.assert_document_option_visible('Внутренний. Без Шаблона Печати (Автотест)')
    main_page_with_responsible.search_document_type('исходящий')
    main_page_with_responsible.assert_document_option_visible('Исходящий (Автотест)')
    main_page_with_responsible.assert_document_option_visible('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_document_option_hidden('Входящий (Автотест)')
    main_page_with_responsible.assert_document_option_hidden('Внутренний. Без Шаблона Печати (Автотест)')


def test_reselect_document_type_in_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.click_document_type_selection_button()
    main_page_with_responsible.select_document_type('Исходящий (Автотест)')
    main_page_with_responsible.assert_document_option_selected('Исходящий (Автотест)')
    main_page_with_responsible.click_document_type_selection_field()
    main_page_with_responsible.assert_document_option_hidden('Исходящий (Автотест)')
    main_page_with_responsible.assert_document_option_visible('Входящий (Автотест)')
    main_page_with_responsible.assert_document_option_visible('Исходящий МЭДО (Автотест)')
    main_page_with_responsible.assert_document_option_visible('Внутренний. Без Шаблона Печати (Автотест)')
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
    main_page_with_responsible.click_profile_button()
    user_information = main_page_with_responsible.get_basic_user_information(array=True)


    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.assert_outgoing_document_creation_tab_visible()


    document_creation_page.assert_multivalues_field_has_value("От кого", user_information)
    document_creation_page.assert_default_field_are_filled()


def test_create_document_with_all_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.fill_all_not_default_fields()
    document_creation_page.check_not_default_checkboxes()
    document_creation_page.click_bottom_save_button()

def test_create_document_with_only_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_incoming_document_creation_page()
    document_creation_page.fill_required_fields()
    document_creation_page.click_upper_save_button()

def test_create_document_via_upper_edit_button(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_medo_creation_page()
    document_creation_page.fill_short_description()
    document_creation_page.click_upper_edit_button()

def test_create_document_via_bottom_edit_button(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_internal_document_creation_page()
    document_creation_page.fill_short_description()
    document_creation_page.click_bottom_edit_button()

def test_click_upper_save_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.click_upper_save_button()
    document_creation_page.assert_field_filling_error_displayed()

def test_click_bottom_save_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_incoming_document_creation_page()
    document_creation_page.click_bottom_save_button()
    document_creation_page.assert_field_filling_error_displayed()

def test_click_bottom_edit_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_medo_creation_page()
    document_creation_page.click_bottom_edit_button()
    document_creation_page.assert_field_filling_error_displayed()

def test_click_upper_edit_button_without_filling_required_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_internal_document_creation_page()
    document_creation_page.click_upper_edit_button()
    document_creation_page.assert_field_filling_error_displayed()

def test_change_default_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.change_print_template()

def test_fill_content_editor_via_content_template(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.assert_content_editor_is_empty()
    document_creation_page.select_first_content_template()
    document_creation_page.assert_content_editor_has_first_template()
    document_creation_page.select_second_content_template()
    document_creation_page.assert_content_editor_has_first_and_second_templates()

def test_select_empty_content_template(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.select_empty_content_template()
    document_creation_page.assert_content_editor_is_empty()

def test_search_in_classifier(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.search_in_classifier('Вид документа *', '9')
    document_creation_page.search_in_classifier('Тематика', 'Тест')
    document_creation_page.search_in_classifier('Корреспондент', '9999 | Тест значение')
    document_creation_page.search_in_classifier('Размер шрифта(при печати)', '13')

def test_example(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.fill_classifier('Выездные совещания', multiform=True, option_value='0')





