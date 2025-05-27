# import os
# import time
# import json
# import datetime
# from utils.screenshot import Screenshot
#
#
# class LoginReportGenerator:
#     """
#     Tạo báo cáo về kết quả đăng nhập.
#     """
#
#     def __init__(self, driver):
#         self.driver = driver
#         self.report_data = {
#             "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "browser": driver.capabilities.get('browserName', 'unknown'),
#             "browser_version": driver.capabilities.get('browserVersion', 'unknown'),
#             "login_tests": [],
#             "summary": {
#                 "total": 0,
#                 "success": 0,
#                 "failed": 0
#             }
#         }
#         self.report_dir = os.path.join(os.path.dirname(__file__), '../reports/login_reports')
#         if not os.path.exists(self.report_dir):
#             os.makedirs(self.report_dir)
#
#     def add_login_test(self, username, password, success, error_message=None, screenshot_path=None):
#         """
#         Thêm kết quả một test đăng nhập vào báo cáo.
#
#         Args:
#             username: Tên đăng nhập
#             password: Mật khẩu (sẽ được che đi)
#             success: True nếu đăng nhập thành công, False nếu thất bại
#             error_message: Thông báo lỗi nếu có
#             screenshot_path: Đường dẫn ảnh chụp màn hình nếu có
#         """
#         # Che giấu mật khẩu
#         masked_password = "*" * len(password) if password else ""
#
#         # Tạo ảnh chụp màn hình nếu không được cung cấp
#         if not screenshot_path and self.driver:
#             timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#             status = "success" if success else "failed"
#             screenshot_path = Screenshot.capture_screenshot(self.driver, f"login_{status}_{timestamp}")
#
#         # Thêm kết quả test
#         self.report_data["login_tests"].append({
#             "username": username,
#             "password": masked_password,
#             "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "success": success,
#             "error_message": error_message,
#             "screenshot": screenshot_path
#         })
#
#         # Cập nhật tổng kết
#         self.report_data["summary"]["total"] += 1
#         if success:
#             self.report_data["summary"]["success"] += 1
#         else:
#             self.report_data["summary"]["failed"] += 1
#
#     def generate_json_report(self):
#         """
#         Tạo báo cáo dạng JSON.
#
#         Returns:
#             Đường dẫn đến file báo cáo JSON
#         """
#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         json_file = os.path.join(self.report_dir, f"login_report_{timestamp}.json")
#
#         with open(json_file, 'w') as f:
#             json.dump(self.report_data, f, indent=2)
#
#         print(f"JSON report created at: {json_file}")
#         return json_file
#
#     def generate_html_report(self):
#         """
#         Tạo báo cáo dạng HTML.
#
#         Returns:
#             Đường dẫn đến file báo cáo HTML
#         """
#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         html_file = os.path.join(self.report_dir, f"login_report_{timestamp}.html")
#
#         with open(html_file, 'w') as f:
#             f.write("<html><head><title>Login Test Report</title>")
#             f.write("<style>")
#             f.write("body{font-family:Arial,sans-serif;line-height:1.6;margin:0;padding:20px;color:#333;}")
#             f.write("h1{color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:10px;}")
#             f.write("table{width:100%;border-collapse:collapse;margin:20px 0;}")
#             f.write("th,td{padding:12px 15px;border-bottom:1px solid #ddd;text-align:left;}")
#             f.write("th{background-color:#f2f2f2;}")
#             f.write("tr.success{background-color:#d5f5e3;}")
#             f.write("tr.failed{background-color:#fadbd8;}")
#             f.write(".summary{background-color:#ebf5fb;padding:15px;border-radius:5px;margin-bottom:20px;}")
#             f.write(".screenshot{max-width:800px;border:1px solid #ddd;margin-top:10px;}")
#             f.write("</style></head><body>")
#
#             f.write("<h1>Login Test Report</h1>")
#
#             # Thông tin báo cáo
#             f.write("<div class='summary'>")
#             f.write(f"<p><strong>Date:</strong> {self.report_data['timestamp']}</p>")
#             f.write(
#                 f"<p><strong>Browser:</strong> {self.report_data['browser']} {self.report_data['browser_version']}</p>")
#             f.write("<h2>Summary</h2>")
#             f.write(f"<p>Total tests: {self.report_data['summary']['total']}</p>")
#             f.write(f"<p>Successful logins: {self.report_data['summary']['success']}</p>")
#             f.write(f"<p>Failed logins: {self.report_data['summary']['failed']}</p>")
#             f.write("</div>")
#
#             # Chi tiết các test case
#             f.write("<h2>Test Details</h2>")
#             f.write("<table>")
#             f.write(
#                 "<tr><th>#</th><th>Username</th><th>Password</th><th>Timestamp</th><th>Status</th><th>Error Message</th></tr>")
#
#             for i, test in enumerate(self.report_data["login_tests"], 1):
#                 row_class = "success" if test["success"] else "failed"
#                 status = "Success" if test["success"] else "Failed"
#                 error = test["error_message"] or ""
#
#                 f.write(f"<tr class='{row_class}'>")
#                 f.write(f"<td>{i}</td>")
#                 f.write(f"<td>{test['username']}</td>")
#                 f.write(f"<td>{test['password']}</td>")
#                 f.write(f"<td>{test['timestamp']}</td>")
#                 f.write(f"<td>{status}</td>")
#                 f.write(f"<td>{error}</td>")
#                 f.write("</tr>")
#
#                 # Thêm ảnh chụp màn hình nếu có
#                 if test["screenshot"]:
#                     rel_path = os.path.relpath(test["screenshot"], self.report_dir)
#                     f.write(
#                         f"<tr class='{row_class}'><td colspan='6'><img class='screenshot' src='{rel_path}' alt='Screenshot' /></td></tr>")
#
#             f.write("</table>")
#             f.write("</body></html>")
#
#         print(f"HTML report created at: {html_file}")
#         return html_file
