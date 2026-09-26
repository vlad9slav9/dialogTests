import os

import pytest
from dotenv import load_dotenv

from pages.document_view_page import DocumentViewPage
from pages.login_page import LoginPage

load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        help="Choose browser: gost, yandex, or default",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def browser(playwright, request):
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("headless")

    if browser_name == "gost":
        browser_path = os.getenv("BROWSER_PATH_GOST")
    elif browser_name == "yandex":
        browser_path = os.getenv("BROWSER_PATH_YANDEX")
    else:
        browser_path = None

    if browser_path:
        browser = playwright.chromium.launch(
            executable_path=browser_path,
            headless=headless,
            args=["--ignore-certificate-errors"],
        )
    else:
        browser = playwright.chromium.launch(
            headless=headless, args=["--ignore-certificate-errors"]
        )

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def login_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    yield login_page


@pytest.fixture(scope="function")
def responsible_user(login_page):
    responsible_user = login_page.login_with_responsible()
    yield responsible_user


@pytest.fixture(scope="function")
def view(page):
    return DocumentViewPage(page)
