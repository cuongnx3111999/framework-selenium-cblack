from selenium.webdriver.common.by import By


class LoginLocators:

    # Demo locators cho Saucedemo website
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    PAGE_TITLE = (By.CSS_SELECTOR, ".login_logo")

    # Demo locators cho trang web tổng quát
    # USERNAME_INPUT = (By.ID, "username")
    # PASSWORD_INPUT = (By.ID, "password")
    # LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    # ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    # FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password")
