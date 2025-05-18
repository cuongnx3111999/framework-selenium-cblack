import pytest
import json
import os
import time
from pages.login_page import LoginPage
from utils.screenshot import Screenshot
from utils.config_reader import ConfigReader


# Load dữ liệu test
@pytest.fixture
def login_data():
    """Fixture để tải dữ liệu login."""
    data_file = os.path.join(os.path.dirname(__file__), '../data/login_data.json')
    with open(data_file, 'r') as file:
        return json.load(file)


@pytest.mark.login
class TestLogin:
    """
    Class test đăng nhập với nhiều test case khác nhau.
    """

    @pytest.mark.parametrize("index", [0, 1, 2])
    def test_valid_login(self, driver, login_data, index):
        """
        Test đăng nhập thành công với thông tin hợp lệ.
        Dùng parametrize để chạy test với nhiều tài khoản hợp lệ.
        """
        # Lấy dữ liệu test từ fixture
        valid_user = login_data["valid_users"][index]

        # Khởi tạo trang đăng nhập
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        # Đăng nhập
        login_page.login(valid_user["username"], valid_user["password"], capture_screenshot=True)

        # Xác nhận đăng nhập thành công
        expected_url = valid_user["expected_landing_page"]
        assert expected_url in driver.current_url, f"Login failed with {valid_user['username']}, not redirected to expected page"

        # Chụp ảnh màn hình sau khi đăng nhập thành công
        Screenshot.capture_screenshot(driver, f"success_login_{valid_user['role']}")

    @pytest.mark.parametrize("index", [0, 1, 2])
    def test_invalid_login(self, driver, login_data, index):
        """
        Test đăng nhập thất bại với thông tin không hợp lệ.
        Dùng parametrize để chạy test với nhiều trường hợp không hợp lệ.
        """
        # Lấy dữ liệu test từ fixture
        invalid_user = login_data["invalid_users"][index]

        # Khởi tạo trang đăng nhập
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        # Đăng nhập
        login_page.login(invalid_user["username"], invalid_user["password"])

        # Xác nhận hiển thị thông báo lỗi
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message not displayed"
        assert invalid_user[
                   "expected_error"] in error_message, f"Expected error message not found: {invalid_user['expected_error']}"

        # Chụp ảnh màn hình khi có lỗi
        Screenshot.capture_screenshot(driver, f"invalid_login_{index}")

    @pytest.mark.parametrize("index", [0, 1])
    def test_validation_cases(self, driver, login_data, index):
        """
        Test các trường hợp validation như trường rỗng.
        """
        # Lấy dữ liệu test từ fixture
        validation_case = login_data["validation_cases"][index]

        # Khởi tạo trang đăng nhập
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        # Đăng nhập
        login_page.login(validation_case["username"], validation_case["password"])

        # Xác nhận hiển thị thông báo lỗi validation
        error_message = login_page.get_error_message()
        assert error_message is not None, "Validation error message not displayed"
        assert validation_case["expected_error"] in error_message, f"Expected validation message not found"

    def test_login_logout_flow(self, driver, login_data):
        """
        Test luồng đăng nhập và đăng xuất.
        """
        # Lấy dữ liệu test từ fixture
        valid_user = login_data["valid_users"][0]

        # Khởi tạo trang đăng nhập
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        # Đăng nhập
        login_page.login(valid_user["username"], valid_user["password"])

        # Xác nhận đăng nhập thành công
        expected_url = valid_user["expected_landing_page"]
        assert expected_url in driver.current_url, "Login failed, not redirected to inventory page"

        # Mở menu
        driver.find_element_by_id("react-burger-menu-btn").click()
        time.sleep(1)

        # Click vào nút logout
        driver.find_element_by_id("logout_sidebar_link").click()
        time.sleep(1)

        # Xác nhận quay lại trang đăng nhập
        assert login_page.is_on_login_page(), "Logout failed, not returned to login page"

        # Chụp ảnh màn hình sau khi đăng xuất
        Screenshot.capture_screenshot(driver, "after_logout")

    def test_login_performance(self, driver, login_data):
        """
        Test hiệu năng đăng nhập.
        """
        # Lấy dữ liệu test từ fixture - sử dụng tài khoản performance_glitch_user
        performance_user = next(user for user in login_data["valid_users"] if user["role"] == "performance")

        # Khởi tạo trang đăng nhập
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        # Đo thời gian đăng nhập
        start_time = time.time()
        login_page.login(performance_user["username"], performance_user["password"])
        end_time = time.time()

        # Tính thời gian đăng nhập
        login_time = end_time - start_time
        print(f"Login time: {login_time:.2f} seconds")

        # Xác nhận đăng nhập thành công
        expected_url = performance_user["expected_landing_page"]
        assert expected_url in driver.current_url, "Login failed, not redirected to expected page"

        # Kiểm tra hiệu năng - có thể điều chỉnh ngưỡng thời gian tùy theo yêu cầu
        assert login_time < 10, f"Login time ({login_time:.2f}s) exceeds threshold (10s)"
