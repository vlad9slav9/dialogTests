from faker import Faker

fake = Faker()
fake_ru = Faker("ru_RU")


def test_navigate_to_login_page(login_page):
    login_page.assert_login_page_logo_visible()


def test_correct_login(login_page):
    event_page = login_page.login_with_responsible()
    event_page.assert_responsible_profile_button_visible()


def test_incorrect_login(login_page):
    fake_username = fake.user_name()
    correct_password = login_page.get_responsible_password()
    login_page.do_login(fake_username, correct_password)
    login_page.assert_login_error_visible()


def test_incorrect_password(login_page):
    correct_username = login_page.get_responsible_username()
    fake_password = fake.password()
    login_page.do_login(correct_username, fake_password)
    login_page.assert_login_error_visible()


def test_login_button_disabled_without_username(login_page):
    login_page.enter_password("test_password")
    login_page.assert_login_button_disabled()


def test_login_button_disabled_without_password(login_page):
    login_page.enter_username("test_username")
    login_page.assert_login_button_disabled()


def test_navigate_to_krtech_website(login_page):
    krtech_page = login_page.click_krtech_logo()
    login_page.assert_krtech_website_opened(krtech_page)
