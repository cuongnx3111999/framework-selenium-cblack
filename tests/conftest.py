import pytest
import os
from pathlib import Path
from datetime import datetime
from utils.driver_factory import DriverFactory
from utils.screenshot import Screenshot  # Import class Screenshot
from utils.config_reader import ConfigReader
from utils.data_loader import DataLoader

# Dictionary để lưu trữ đường dẫn screenshot cho báo cáo HTML
screenshots_dict = {}


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

    # Gán driver vào request để có thể truy cập trong teardown
    request.node.driver = driver

    yield driver

    driver.quit()


# Fixture để lấy thông tin môi trường test
@pytest.fixture(scope="session")
def env(request):
    """Get environment configuration."""
    env_name = request.config.getoption("--env")
    return ConfigReader.get_environment_config(env_name)


# Fixture để chụp screenshot theo yêu cầu trong test case
@pytest.fixture
def take_screenshot(request, driver):
    """
    Fixture để chụp screenshot trong test case

    Ví dụ:
    def test_example(driver, take_screenshot):
        driver.get("https://example.com")
        take_screenshot("home_page")  # Chụp ảnh có tên
    """

    def _take_screenshot(name=None):
        test_name = request.node.name
        if name:
            test_name = f"{test_name}_{name}"

        screenshot_path = Screenshot.capture_screenshot(driver, test_name)

        # Lưu đường dẫn vào dictionary
        if screenshot_path:
            key = f"{request.node.nodeid}::{name}" if name else request.node.nodeid
            screenshots_dict[key] = screenshot_path

        return screenshot_path

    return _take_screenshot


# Hook to customize HTML report title
def pytest_html_report_title(report):
    report.title = "Selenium Test Automation Report"


# Fixture để tạo báo cáo HTML với screenshot khi test fail
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Chỉ xử lý khi test thực sự thất bại (trong giai đoạn call)
    if report.when == "call" and report.failed:
        # Lấy driver từ fixture hoặc từ node
        driver = None
        if hasattr(item, "funcargs") and "driver" in item.funcargs:
            driver = item.funcargs["driver"]
        elif hasattr(item, "driver"):
            driver = item.driver

        if driver:
            try:
                # Tạo tên test có thể nhận dạng
                test_name = item.nodeid.replace("::", "_").replace("/", "_").replace(".", "_")

                # Thêm xdist worker id nếu chạy song song
                worker_id = os.environ.get('PYTEST_XDIST_WORKER', '')
                if worker_id:
                    test_name = f"{test_name}_{worker_id}"

                # Sử dụng class Screenshot để chụp ảnh
                screenshot_path = Screenshot.capture_screenshot(driver, test_name, status="fail")

                # Kiểm tra file đã được tạo thành công
                if screenshot_path and os.path.exists(screenshot_path):
                    # Lưu đường dẫn để sử dụng trong báo cáo HTML
                    screenshots_dict[item.nodeid] = screenshot_path
                    print(f"\nĐã chụp màn hình khi test thất bại: {screenshot_path}")

            except Exception as e:
                print(f"\nLỗi khi chụp màn hình: {str(e)}")


# Hook để thêm screenshot vào báo cáo HTML
def pytest_html_results_table_html(report, data):
    """Add screenshot to HTML report"""
    # Xử lý screenshot khi test thất bại
    if report.failed and report.nodeid in screenshots_dict:
        screenshot_path = screenshots_dict[report.nodeid]
        try:
            # Sử dụng đường dẫn tương đối từ vị trí báo cáo HTML
            # Ảnh được lưu trong reports/screenshots, báo cáo HTML trong reports
            relative_path = f"screenshots/{os.path.basename(screenshot_path)}"

            # Thêm ảnh vào báo cáo HTML
            html = f'<div><p><strong>Screenshot khi test thất bại:</strong></p>'
            html += f'<img src="{relative_path}" alt="Screenshot" style="width:800px;height:auto;border:1px solid #ddd;"></div>'
            data.append(html)
        except Exception as e:
            html = f'<div><p>Không thể thêm screenshot vào báo cáo: {str(e)}</p></div>'
            data.append(html)

    # Xử lý các screenshot được chụp thủ công trong test
    for key in list(screenshots_dict.keys()):
        # Nếu key có định dạng nodeid::name
        if "::" in key and key.startswith(report.nodeid + "::"):
            step_name = key.split("::")[-1]
            screenshot_path = screenshots_dict[key]
            try:
                relative_path = f"screenshots/{os.path.basename(screenshot_path)}"
                html = f'<div><p><strong>Screenshot ({step_name}):</strong></p>'
                html += f'<img src="{relative_path}" alt="Screenshot" style="width:800px;height:auto;border:1px solid #ddd;"></div>'
                data.append(html)
            except Exception as e:
                html = f'<div><p>Không thể thêm screenshot cho "{step_name}": {str(e)}</p></div>'
                data.append(html)


# Hook để thêm thông tin hữu ích vào báo cáo
@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Add metadata to HTML report"""
    # Kiểm tra xem plugin pytest-html có được sử dụng không
    if hasattr(config, "_metadata"):
        # Thêm metadata vào báo cáo
        config._metadata["Tên dự án"] = "Framework Selenium Testing"
        config._metadata["Thời gian chạy"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config._metadata["Môi trường"] = config.getoption("--env")
        config._metadata["Trình duyệt"] = config.getoption("--browser")
        config._metadata["Headless"] = str(config.getoption("--headless"))

        # Xóa các mục mặc định không cần thiết
        if "Packages" in config._metadata:
            del config._metadata["Packages"]
