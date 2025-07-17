from datetime import datetime
import pytest
from pages.installation_page import InstallationPage
from pages.main_page import MainPage
from pages.uninstallation_page import UnInstallationPage

# 显式导入helpers模块
pytest_plugins = ["utils.helpers"]

@pytest.fixture(scope="module")
def setup_path(request):
    return request.config.getoption("--setup-path")

@pytest.fixture(scope="module")
def app_path(request):
    return request.config.getoption("--app-path")

@pytest.fixture(scope="module")
def window_title(request):
    return request.config.getoption("--window-title")

@pytest.fixture(scope="module")
def uninstall_path(request):
    return request.config.getoption("--uninstall-path")

@pytest.fixture(scope="module")
def installation_page(setup_path):
    return InstallationPage(setup_path)

@pytest.fixture(scope="module")
def uninstallation_page(uninstall_path):
    return UnInstallationPage(uninstall_path)

@pytest.fixture(scope="function")
def main_page(app_path, window_title):
    page = MainPage(app_path, window_title)
    yield page
    page.close_application()

def pytest_addoption(parser):
    parser.addini("current_time", help="current time for report name")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # 设置当前时间格式
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config._inicache["current_time"] = current_time
    # 替换addopts中的{current_time}
    config.option.htmlpath = config.option.htmlpath.replace("{current_time}", current_time)
