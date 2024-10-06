import pytest

from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', help="Choose browser: gost or yandex")


@pytest.fixture(scope="session")
def browser(playwright, request):
    browser_name = request.config.getoption("browser_name")
    if browser_name == "gost":
        browser = playwright.chromium.launch(executable_path=r"C:\Program Files (x86)\krtech\chrome\chrome.exe",
                                             headless=False)
    elif browser_name == "yandex":
        browser = playwright.chromium.launch(
            executable_path=r"C:\Users\KSK-SHOP\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
            headless=False)
    else:
        browser = playwright.chromium.launch()
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def login_page(page):   
    login_page = LoginPage(page)
    login_page.navigate()
    yield login_page
