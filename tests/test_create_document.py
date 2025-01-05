


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
    main_page_with_responsible.enter_document_type_in_field("исходящий")
    main_page_with_responsible.assert_outgoing_document_option_visible()
    main_page_with_responsible.assert_outgoing_medo_document_option_visible()
    main_page_with_responsible.assert_internal_document_option_hidden()
    main_page_with_responsible.assert_incoming_document_option_hidden()


def test_reselect_document_type_in_document_creation_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.select_internal_document_type()
    main_page_with_responsible.assert_internal_document_option_selected()
    main_page_with_responsible.assert_internal_document_option_selected()
    main_page_with_responsible.click_document_type_selection_button()
    main_page_with_responsible.assert_internal_document_option_hidden()
    main_page_with_responsible.assert_outgoing_document_option_visible()
    main_page_with_responsible.assert_incoming_document_option_visible()
    main_page_with_responsible.assert_outgoing_medo_document_option_visible()
    main_page_with_responsible.click_outgoing_document_option()
    main_page_with_responsible.assert_outgoing_document_option_selected()


def test_create_document_button_disabled_after_clearing_field(main_page_with_responsible):
    main_page_with_responsible.click_quick_document_creation_button()
    main_page_with_responsible.assert_create_document_button_disabled()
    main_page_with_responsible.assert_document_type_search_field_empty()
    main_page_with_responsible.select_outgoing_document_type()
    main_page_with_responsible.assert_outgoing_document_option_selected()
    main_page_with_responsible.assert_create_document_button_enabled()
    main_page_with_responsible.click_document_type_search_field_clear_button()
    main_page_with_responsible.assert_document_type_search_field_empty()
    main_page_with_responsible.assert_create_document_button_disabled()


def test_open_outgoing_document_creation_page(main_page_with_responsible):
    main_page_with_responsible.click_profile_button()
    user_information = main_page_with_responsible.get_basic_user_information(array=True)
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.assert_outgoing_document_creation_tab_visible()
    document_creation_page.assert_multivalues_field_has_value("От кого", user_information)
    document_creation_page.assert_default_field_are_filled()
    document_creation_page.assert_default_checkboxes_are_checked()


def test_create_document_with_all_fields(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.fill_all_not_default_fields()
    document_creation_page.check_not_default_checkboxes()

def test_example(main_page_with_responsible):
    document_creation_page = main_page_with_responsible.open_outgoing_document_creation_page()
    document_creation_page.example_method()





