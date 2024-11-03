def test_logout(login_page, responsible_main_page):
    responsible_main_page.click_logout_button()
    responsible_main_page.click_confirm_logout_button()
    login_page.assert_login_page_logo_visible()


def test_cancel_logout(responsible_main_page):
    responsible_main_page.click_logout_button()
    responsible_main_page.click_cancel_logout_button()
    responsible_main_page.assert_responsible_profile_button_visible()


def test_click_krtech_logo_from_main_page(responsible_main_page):
    krtech_page = responsible_main_page.click_krtech_logo()
    responsible_main_page.assert_krtech_website_opened(krtech_page)


def test_click_telegram_button_from_main_page(responsible_main_page):
    telegram_page = responsible_main_page.click_telegram_button()
    responsible_main_page.assert_telegram_website_opened(telegram_page)


def test_click_vkontakte_button_from_main_page(responsible_main_page):
    vkontakte_page = responsible_main_page.click_vkontakte_button()
    responsible_main_page.assert_vkontakte_website_opened(vkontakte_page)


def test_hide_sidebar(responsible_main_page):
    responsible_main_page.click_hide_sidebar_button()
    responsible_main_page.assert_sidebar_hidden()


def test_open_sidebar(responsible_main_page):
    responsible_main_page.click_hide_sidebar_button()
    responsible_main_page.click_open_sidebar_button()
    responsible_main_page.assert_sidebar_visible()
