from time import sleep

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
        self.timeout = ConfigReader.get_config_value("timeout", 10)

    def navigate_to_login_page(self):
        """
        Điều hướng đến trang đăng nhập.
        """
        URL = "https://lab.connect247.vn/ucrm-ver3/dashboard"
        self.open_url(URL)
        self.wait_for_clickable(LoginLocators.btn_login,timeout=120)
        sleep(1)
        self.click(LoginLocators.btn_login)
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
        self.wait_for_clickable(LoginLocators.btn_login)
        # Nhập tên đăng nhập
        self.send_keys(self.locators.username, username)

        if capture_screenshot:
            Screenshot.capture_screenshot(self.driver, f"login_entered_username_{username}")

        # Nhập mật khẩu
        self.send_keys(self.locators.password, password)

        if capture_screenshot:
            Screenshot.capture_screenshot(self.driver, "login_entered_password")

        # Click nút đăng nhập
        self.click(self.locators.btn_login)

        if capture_screenshot:
            Screenshot.capture_screenshot(self.driver, "login_after_click")

        # Đợi một chút để chuyển trang
        time.sleep(5)

        return self

    def get_error_message(self):
        """
        Lấy thông báo lỗi nếu có.

        Returns:
            Nội dung thông báo lỗi hoặc None nếu không có lỗi
        """
        if self.is_displayed(self.locators.notice_error):
            return self.get_text(self.locators.notice_error)
        return None

    def get_error_username(self):
        if self.is_displayed(self.locators.explain_errors_username):
            return self.get_text(self.locators.explain_errors_username)
        return None

    def get_error_password(self):
        if self.is_displayed(self.locators.explain_errors_password):
            return self.get_text(self.locators.explain_errors_password)
        return None

    def is_on_login_page(self):
        """
        Kiểm tra xem hiện tại có đang ở trang đăng nhập không.

        """

        return (self.is_displayed(self.locators.btn_login) and self.is_displayed(self.locators.username) and self.is_displayed(self.locators.password))==False

    def clear_inputs(self):
        """
        Xóa nội dung các trường nhập.

        Returns:
            self để hỗ trợ chuỗi phương thức
        """
        self.find_element(self.locators.username).clear()
        self.find_element(self.locators.password).clear()
        return self

    def choiseLanguange(self,languange='English'):
        self.wait_for_clickable(self.locators.btn_AddLanguage).click()
        sleep(1)
        if languange == 'English':
            self.wait_for_clickable(self.locators.btn_EnglishLanguage).click()
        else:
            self.wait_for_clickable(self.locators.btn_VietNamesLanguage).click()

    def checkHidePassword(self,password=""):
        self.click(self.locators.icon_eye_invisible)
        return password==self.find_element(self.locators.password).get_attribute('value')
