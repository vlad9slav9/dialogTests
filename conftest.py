import configparser
import pytest
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', help="Choose browser: gost, yandex, or default")
    parser.addoption('--headless', action='store_true', default=False, help="Run browser in headless mode")


@pytest.fixture(scope="session")
def browser(playwright, request):
    config = configparser.ConfigParser()
    config.read('config.ini')

    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("headless")

    if browser_name == "gost":
        browser_path = config.get('browsers', 'browser_path_gost', fallback=None)
    elif browser_name == "yandex":
        browser_path = config.get('browsers', 'browser_path_yandex', fallback=None)
    else:
        browser_path = None

    if browser_path:
        browser = playwright.chromium.launch(executable_path=browser_path, headless=headless, args=["--ignore-certificate-errors"])
    else:
        browser = playwright.chromium.launch(headless=headless, args=["--ignore-certificate-errors"])

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def login_page(page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    login_page = LoginPage(page)
    login_page.navigate()
    yield login_page


@pytest.fixture(scope="function")
def main_page_with_responsible(login_page):
    main_page = login_page.login_with_responsible()
    yield main_page
