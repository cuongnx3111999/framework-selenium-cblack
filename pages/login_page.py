from .base_page import BasePage
from locators.login_locators import LoginLocators
from utils.config_reader import ConfigReader
from utils.screenshot import Screenshot
import time


class LoginPage(BasePage):
    """
    Page Object cho trang đăng nhập.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginLocators

    def navigate_to_login_page(self):
        """
        Điều hướng đến trang đăng nhập.
        """
        env = ConfigReader.get_environment_config()
        self.open_url(env["url"])
        return self

    def login(self, username, password, capture_screenshot=False):
        """
        Đăng nhập với thông tin tài khoản.

        Args:
            username: Tên đăng nhập
            password: Mật khẩu
            capture_screenshot: True nếu muốn chụp ảnh màn hình khi đăng nhập

        Returns:
            self để hỗ trợ chuỗi phương thức
        """
        # Nhập tên đăng nhập
        self.send_keys(self.locators.USERNAME_INPUT, username)

        if capture_screenshot:
            Screenshot.capture_screenshot(self.driver, f"login_entered_username_{username}")

        # Nhập mật khẩu
        self.send_keys(self.locators.PASSWORD_INPUT, password)

        if capture_screenshot:
            Screenshot.capture_screenshot(self.driver, "login_entered_password")

        # Click nút đăng nhập
        self.click(self.locators.LOGIN_BUTTON)

        if capture_screenshot:
            Screenshot.capture_screenshot(self.driver, "login_after_click")

        # Đợi một chút để chuyển trang
        time.sleep(1)

        return self

    def get_error_message(self):
        """
        Lấy thông báo lỗi nếu có.

        Returns:
            Nội dung thông báo lỗi hoặc None nếu không có lỗi
        """
        if self.is_displayed(self.locators.ERROR_MESSAGE):
            return self.get_text(self.locators.ERROR_MESSAGE)
        return None

    def is_error_displayed(self):
        """
        Kiểm tra xem có thông báo lỗi được hiển thị không.

        Returns:
            True nếu thông báo lỗi được hiển thị, ngược lại là False
        """
        return self.is_displayed(self.locators.ERROR_MESSAGE)

    def is_on_login_page(self):
        """
        Kiểm tra xem hiện tại có đang ở trang đăng nhập không.

        Returns:
            True nếu đang ở trang đăng nhập, ngược lại là False
        """
        return (self.is_element_present(self.locators.USERNAME_INPUT) and
                self.is_element_present(self.locators.PASSWORD_INPUT) and
                self.is_element_present(self.locators.LOGIN_BUTTON))

    def clear_inputs(self):
        """
        Xóa nội dung các trường nhập.

        Returns:
            self để hỗ trợ chuỗi phương thức
        """
        self.find_element(self.locators.USERNAME_INPUT).clear()
        self.find_element(self.locators.PASSWORD_INPUT).clear()
        return self

    def get_page_title(self):
        """
        Lấy tiêu đề trang đăng nhập.

        Returns:
            Tiêu đề của trang đăng nhập
        """
        return self.get_text(self.locators.PAGE_TITLE)
