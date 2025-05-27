# import pytest
# import json
# import os
# import time
# from pages.login_page import LoginPage
# from pages.home_page import HomePage
# from utils.login_report_generator import LoginReportGenerator
#
#
# # Load dữ liệu test
# @pytest.fixture
# def login_data():
#     """Fixture để tải dữ liệu login."""
#     data_file = os.path.join(os.path.dirname(__file__), '../data/login_data.json')
#     with open(data_file, 'r') as file:
#         return json.load(file)
#
#
# @pytest.mark.login_report
# class TestLoginWithReport:
#     """
#     Kiểm tra đăng nhập và tạo báo cáo chi tiết.
#     """
#
#     def test_login_with_multiple_users(self, driver, login_data):
#         """
#         Test đăng nhập với nhiều tài khoản khác nhau và tạo báo cáo chi tiết.
#         """
#         # Khởi tạo các trang và report generator
#         login_page = LoginPage(driver)
#         home_page = HomePage(driver)
#         report_generator = LoginReportGenerator(driver)
#
#         # Đăng nhập với các tài khoản hợp lệ
#         for user in login_data["valid_users"]:
#             # Điều hướng đến trang đăng nhập
#             login_page.navigate_to_login_page()
#
#             # Đăng nhập
#             login_page.login(user["username"], user["password"])
#
#             # Kiểm tra kết quả
#             is_success = home_page.is_home_page_displayed()
#
#             # Thêm kết quả vào báo cáo
#             report_generator.add_login_test(
#                 username=user["username"],
#                 password=user["password"],
#                 success=is_success,
#                 error_message=None if is_success else login_page.get_error_message()
#             )
#
#             # Đăng xuất nếu đăng nhập thành công
#             if is_success:
#                 home_page.logout()
#
#         # Đăng nhập với các tài khoản không hợp lệ
#         for user in login_data["invalid_users"]:
#             # Điều hướng đến trang đăng nhập
#             login_page.navigate_to_login_page()
#
#             # Đăng nhập
#             login_page.login(user["username"], user["password"])
#
#             # Kiểm tra kết quả
#             is_success = home_page.is_home_page_displayed()
#             error_message = None if is_success else login_page.get_error_message()
#
#             # Thêm kết quả vào báo cáo
#             report_generator.add_login_test(
#                 username=user["username"],
#                 password=user["password"],
#                 success=is_success,
#                 error_message=error_message
#             )
#
#             # Kiểm tra thông báo lỗi
#             if not is_success and "expected_error" in user:
#                 assert user["expected_error"] in (error_message or ""), f"Expected error message not found"
#
#         # Tạo báo cáo
#         report_generator.generate_html_report()
#         report_generator.generate_json_report()
