from selenium.webdriver.common.by import By


class UsersLocators:
    btn_Seting=(By.CSS_SELECTOR,".ant-menu-item.ant-menu-item-selected")
    btn_Users=(By.XPATH,"//div[@class='title' and text()='Users']")
    btn_AddUser=(By.XPATH,"//span[text()='+ Add user']")
    btn_ThaoTacExcel = (By.XPATH, "//span[text()='Thao tác với Excel ']")
    FirstName=(By.CSS_SELECTOR,"#firstname")
    LastName=(By.CSS_SELECTOR,"#lastname")
    Email=(By.CSS_SELECTOR,"#email")
    MiddleName=(By.CSS_SELECTOR,"#middlename")
    PassWord=(By.CSS_SELECTOR,"#password")
    VerifyPassword=(By.CSS_SELECTOR,"#verifypassword")
    Role=(By.CSS_SELECTOR,"#role")
    reportTo=(By.CSS_SELECTOR,"#report_to")
    Radio_User=(By.CSS_SELECTOR,'input.ant-radio-input[type="radio"][value="user"]')
    Radio_Admin=(By.CSS_SELECTOR,'input.ant-radio[type="radio"][value="admin"]')
    btn_Save=(By.XPATH,"//button[./span[text()='Save']]]")
    btn_Cancel=(By.XPATH,"//button[./span[text()='Cancel']]")
    btn_Edit=(By.CSS_SELECTOR,'img[alt="edit"]')
    btn_ChangePass=(By.CSS_SELECTOR,'img[alt="changepass"]')
    btn_Delete=(By.CSS_SELECTOR,'img[alt="delete"]')
    btn_Switch=(By.CSS_SELECTOR,'.ant-switch')