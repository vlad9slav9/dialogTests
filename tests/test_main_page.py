def test_logout(login_page):
    event_page = login_page.login_with_responsible()
    event_page.click_logout_button()
    event_page.click_confirm_logout_button()
    login_page.assert_login_page_logo_visible()


def test_cancel_logout(login_page):
    event_page = login_page.login_with_responsible()
    event_page.click_logout_button()
    event_page.click_cancel_logout_button()
    event_page.assert_responsible_profile_button_visible()


def test_click_krtech_logo_from_event_page(login_page):
    event_page = login_page.login_with_responsible()
    krtech_page = event_page.click_krtech_logo()
    event_page.assert_krtech_website_opened(krtech_page)


def test_click_telegram_button_from_event_page(login_page):
    event_page = login_page.login_with_responsible()
    telegram_page = event_page.click_telegram_button()
    event_page.assert_telegram_website_opened(telegram_page)


def test_click_vkontakte_button_from_event_page(login_page):
    event_page = login_page.login_with_responsible()
    vkontakte_page = event_page.click_vkontakte_button()
    event_page.assert_vkontakte_website_opened(vkontakte_page)
