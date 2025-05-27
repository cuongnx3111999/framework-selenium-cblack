import pytest
from pages.login_page import LoginPage
from utils.pytest_data_helpers import csv_data_provider, filter_by_category, filter_by_expected_result, filter_by_expected_message


class TestLogin:
    """Test cases cho tính năng đăng nhập"""

    @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_expected_result('success'))
    def test_success(self, driver, test_data):
        """Test các trường hợp đăng nhập thành công"""
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])

        assert login_page.is_on_login_page() is True

    @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_expected_result('error'))
    def test_success(self, driver, test_data):
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
        assert test_data['expected_message'] in error_message, error_message

    @csv_data_provider('csv/datatest_login.csv',filter_func= filter_by_expected_message('Nhập mật khẩu'))
    def test_validation_password(self, driver, test_data):
        """Test trường hợp bỏ trống password"""
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])

        # Kiểm tra kết quả
        error_message=login_page.get_error_password()
        assert test_data['expected_message'] in error_message, error_message

    @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_expected_message(['Username or password incorrect','User inactive', 'locked']))
    def test_validation_password(self, driver, test_data):
        """Test trường hợp bỏ trống password"""
        login_page = LoginPage(driver).navigate_to_login_page()
        login_page.login(test_data['username'], test_data['password'])

        # Kiểm tra kết quả
        error_message = login_page.get_error_message()
        assert test_data['expected_message'] in error_message, error_message


    # @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_category('account_status'))
    # def test_account_status(self, driver, test_data):
    #     """Test các trường hợp về trạng thái tài khoản (khóa, không hoạt động)"""
    #     login_page = LoginPage(driver).open()
    #     login_page.login(test_data['username'], test_data['password'])
    #
    #     # Kiểm tra thông báo lỗi về trạng thái tài khoản
    #     error_message = login_page.get_error_message()
    #     assert error_message is not None, "Không hiển thị thông báo lỗi"
    #     assert test_data['expected_message'] in error_message, f"Thông báo lỗi không đúng"
    #
    # @csv_data_provider('csv/datatest_login.csv', filter_func=filter_by_category('ui'))
    # def test_ui_features(self, driver, test_data):
    #     """Test các tính năng UI của form đăng nhập"""
    #     login_page = LoginPage(driver).open()
    #
    #     # Kiểm tra che mật khẩu
    #     if test_data['testcase'].lower().find('che mật khẩu') >= 0:
    #         login_page.enter_password(test_data['password'])
    #         assert login_page.is_password_masked(), "Mật khẩu không được che đúng cách"
