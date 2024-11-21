def test_logout(login_page, main_page_with_responsible):
    main_page_with_responsible.click_logout_button()
    main_page_with_responsible.click_confirm_logout_button()
    login_page.assert_login_page_logo_visible()


def test_cancel_logout(main_page_with_responsible):
    main_page_with_responsible.click_logout_button()
    main_page_with_responsible.click_cancel_logout_button()
    main_page_with_responsible.assert_responsible_profile_button_visible()


def test_click_krtech_logo_from_main_page(main_page_with_responsible):
    krtech_page = main_page_with_responsible.click_krtech_logo()
    main_page_with_responsible.assert_krtech_website_opened(krtech_page)


def test_click_telegram_button_from_main_page(main_page_with_responsible):
    telegram_page = main_page_with_responsible.click_telegram_button()
    main_page_with_responsible.assert_telegram_website_opened(telegram_page)


def test_click_vkontakte_button_from_main_page(main_page_with_responsible):
    vkontakte_page = main_page_with_responsible.click_vkontakte_button()
    main_page_with_responsible.assert_vkontakte_website_opened(vkontakte_page)


def test_hide_sidebar(main_page_with_responsible):
    main_page_with_responsible.click_hide_sidebar_button()
    main_page_with_responsible.assert_sidebar_hidden()


def test_open_sidebar(main_page_with_responsible):
    main_page_with_responsible.click_hide_sidebar_button()
    main_page_with_responsible.assert_sidebar_hidden()
    main_page_with_responsible.click_open_sidebar_button()
    main_page_with_responsible.assert_sidebar_visible()


def test_click_home_button(main_page_with_responsible):
    main_page_with_responsible.click_responsible_profile_button()
    main_page_with_responsible.click_home_button()
    main_page_with_responsible.assert_event_container_visible()


def test_display_date(main_page_with_responsible):
    main_page_with_responsible.assert_displayed_date()


def test_display_time(main_page_with_responsible):
    main_page_with_responsible.assert_displayed_time()


def test_open_quick_create_document_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_create_document_button()
    main_page_with_responsible.assert_create_document_window_opened()


def test_cancel_create_document_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_create_document_button()
    main_page_with_responsible.click_cancel_create_document_button()
    main_page_with_responsible.assert_create_document_window_hidden()


def test_close_create_document_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_create_document_button()
    main_page_with_responsible.click_close_create_document_button()
    main_page_with_responsible.assert_create_document_window_hidden()


def test_search_document_type_in_create_document_window(main_page_with_responsible):
    main_page_with_responsible.click_quick_create_document_button()
    main_page_with_responsible.enter_document_type_in_field("исходящий")
    main_page_with_responsible.assert_outgoing_document_visible()
    main_page_with_responsible.assert_outgoing_MEDO_document_visible()
    main_page_with_responsible.assert_internal_document_hidden()
    main_page_with_responsible.assert_incoming_document_hidden()


def test_create_document_button_disabled_after_clearing_field(main_page_with_responsible):
    main_page_with_responsible.click_quick_create_document_button()
    main_page_with_responsible.assert_create_document_button_disabled()
    main_page_with_responsible.select_outgoing_document_type()
    main_page_with_responsible.assert_create_document_button_enabled()
    main_page_with_responsible.click_clear_document_type_search_field_button()
    main_page_with_responsible.assert_create_document_button_disabled()
