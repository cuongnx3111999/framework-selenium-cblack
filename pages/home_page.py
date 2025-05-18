from .base_page import BasePage
from selenium.webdriver.common.by import By
import time


class HomePageLocators:
    """
    Locators cho trang chính sau khi đăng nhập.
    """
    # Locators cho Saucedemo
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    SHOPPING_CART = (By.ID, "shopping_cart_container")
    PAGE_TITLE = (By.CLASS_NAME, "app_logo")
    PRODUCT_SORT = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")


class HomePage(BasePage):
    """
    Page Object cho trang chính sau khi đăng nhập.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = HomePageLocators

    def is_home_page_displayed(self):
        """
        Kiểm tra xem đã chuyển hướng đến trang chính hay chưa.

        Returns:
            True nếu đang ở trang chính, ngược lại là False
        """
        return (self.is_element_present(self.locators.MENU_BUTTON) and
                self.is_element_present(self.locators.SHOPPING_CART) and
                self.is_element_present(self.locators.PRODUCT_SORT))

    def get_product_count(self):
        """
        Lấy số lượng sản phẩm hiển thị.

        Returns:
            Số lượng sản phẩm
        """
        products = self.find_elements(self.locators.INVENTORY_ITEMS)
        return len(products)

    def click_menu(self):
        """
        Mở menu bên.

        Returns:
            self để hỗ trợ chuỗi phương thức
        """
        self.click(self.locators.MENU_BUTTON)
        # Đợi menu hiển thị
        time.sleep(0.5)
        return self

    def logout(self):
        """
        Đăng xuất khỏi ứng dụng.

        Returns:
            self để hỗ trợ chuỗi phương thức
        """
        self.click_menu()
        self.click(self.locators.LOGOUT_LINK)
        return self
