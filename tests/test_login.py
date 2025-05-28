import pytest
from pages.login_page import LoginPage
from utils.pytest_data_helpers import csv_data_provider, filter_by_category, filter_by_expected_result, filter_by_expected_message

@pytest.mark.login
class TestLogin:
    """Test cases cho tính năng đăng nhập"""

    @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_expected_result('success'))
    def test_success(self, driver, test_data):
        """Test các trường hợp đăng nhập thành công"""
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])
        assert login_page.is_on_login_page() is True

    @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_expected_result('error'))
    def test_fail(self, driver, test_data):
        """Test các trường hợp đăng nhập không thành công"""
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])

        assert login_page.is_on_login_page() is False

    @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_expected_message('Nhập email'))
    def test_validation_username(self, driver, test_data):
        """Test các trường hợp xác thực đăng nhập lỗi username """
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])

        # Kiểm tra kết quả
        error_message=login_page.get_error_username()
        if error_message:
            assert test_data['expected_message'] in error_message, error_message
        else:
            assert False,test_data['expected_message']

    @csv_data_provider('csv/datatest_login.csv',filter_func= filter_by_expected_message('Nhập mật khẩu'))
    def test_validation_password(self, driver, test_data):
        """Test trường hợp bỏ trống password"""
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])

        # Kiểm tra kết quả
        error_message=login_page.get_error_password()
        if error_message:
            assert test_data['expected_message'] in error_message, error_message
        else:
            assert False,test_data['expected_message']

    @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_expected_message(['Username or password incorrect','User inactive, can’t log in', 'has been locked']))
    def test_error(self, driver, test_data):
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])

        # Kiểm tra kết quả
        error_message = login_page.get_error_message()
        if error_message:
            assert test_data['expected_message'] in error_message, error_message
        else:
            assert False, "Login failed."


