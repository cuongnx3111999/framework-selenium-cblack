import pytest
import os
from utils.driver_factory import DriverFactory
from utils.screenshot import Screenshot
from utils.config_reader import ConfigReader
import datetime
from utils.data_loader import DataLoader


# Định nghĩa CLI options cho pytest
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests: chrome, firefox, edge")
    parser.addoption("--env", action="store", default="test",
                     help="Environment to run tests: dev, test, staging, prod")
    parser.addoption("--headless", action="store_true", default=True,
                     help="Run browser in headless mode")

@pytest.fixture(scope="session")
def data_loader():
    """Fixture để cung cấp instance của DataLoader"""
    return DataLoader()

@pytest.fixture(scope="session")
def config(request):
    """Return configuration dictionary."""
    config = ConfigReader.get_base_config()

    # Override config with command line options
    config["browser"] = request.config.getoption("--browser")
    config["env"] = request.config.getoption("--env")
    config["headless"] = request.config.getoption("--headless")

    return config
# Fixture để khởi tạo WebDriver

@pytest.fixture(scope="function")
def driver(request, config):
    """Initialize WebDriver and close it after test."""
    browser = config["browser"]
    headless = config["headless"]
    driver = DriverFactory.get_driver(browser, headless)

    yield driver

    driver.quit()

# Fixture để lấy thông tin môi trường test
@pytest.fixture(scope="session")
def env(request):
    """Get environment configuration."""
    env_name = request.config.getoption("--env")
    return ConfigReader.get_environment_config(env_name)


# Fixture để tạo báo cáo HTML
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            test_name = item.nodeid.split("::")[-1]
            Screenshot.capture_screenshot(driver, test_name)
