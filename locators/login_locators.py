from selenium.webdriver.common.by import By


class LoginLocators:

    # Demo locators cho Saucedemo website
    btn_login=(By.CSS_SELECTOR,"button.ant-btn.ant-btn-primary")
    username = (By.CSS_SELECTOR, "#basic_email")
    password=(By.CSS_SELECTOR, "#basic_pass")
    icon_eye_invisible=(By.CSS_SELECTOR, ".ant-input-suffix")
    explain_errors_username=(By.CSS_SELECTOR, "#basic_email_help .ant-form-item-explain-error")
    explain_errors_password=(By.CSS_SELECTOR, "#basic_pass_help .ant-form-item-explain-error")
    notice_error=(By.CSS_SELECTOR,".ant-notification-notice-description")
    btn_AddLanguage=(By.CSS_SELECTOR,".language_app")
    btn_VietNamesLanguage=(By.XPATH,"//*[contains(text(), 'Tiếng Việt')]")
    btn_EnglishLanguage=(By.XPATH,"//*[contains(text(), 'English')]")
