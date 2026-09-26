from pages.components.layout_component import LayoutComponent
from pages.login_page import LoginPage


def test_logout(login_page: LoginPage, responsible_user: LayoutComponent):
    responsible_user.click_logout_button()
    responsible_user.click_logout_confirm_button()
    login_page.assert_login_page_logo_visible()


def test_cancel_logout(responsible_user: LayoutComponent):
    responsible_user.click_logout_button()
    responsible_user.click_cancel_logout_button()
    responsible_user.assert_profile_button_visible()


def test_click_krtech_logo_from_main_page(responsible_user: LayoutComponent):
    krtech_page = responsible_user.click_krtech_logo()
    responsible_user.assert_krtech_website_opened(krtech_page)


def test_click_telegram_button_from_main_page(
    responsible_user: LayoutComponent,
):
    telegram_page = responsible_user.click_telegram_button()
    responsible_user.assert_telegram_website_opened(telegram_page)


def test_click_vkontakte_button_from_main_page(
    responsible_user: LayoutComponent,
):
    vkontakte_page = responsible_user.click_vkontakte_button()
    responsible_user.assert_vkontakte_website_opened(vkontakte_page)


def test_switch_sidebar(responsible_user: LayoutComponent):
    responsible_user.click_hide_sidebar_button()
    responsible_user.assert_sidebar_hidden()
    responsible_user.click_open_sidebar_button()
    responsible_user.assert_sidebar_visible()


def test_click_home_button(responsible_user: LayoutComponent):
    responsible_user.click_profile_button()
    event_page = responsible_user.click_home_button()
    event_page.assert_event_container_visible()


def test_display_date(responsible_user: LayoutComponent):
    responsible_user.assert_displayed_date()


def test_display_time(responsible_user: LayoutComponent):
    responsible_user.assert_displayed_time()
