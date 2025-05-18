from selenium.webdriver.common.by import By

class muasamcongLocator:
    NOTIC=(By.CSS_SELECTOR,".notification-popup")
    X_NOTE=(By.CSS_SELECTOR, "svg.bi.bi-x")
    TimTheoThuoc=(By.CSS_SELECTOR, 'input[placeholder="Nhập số TBMT/Tên gói thầu (ví dụ: IB0123456789 hoặc Thiết bị)"]')
    Caledar_input_NgayPheDuyet=(By.CSS_SELECTOR, ".ant-calendar-picker-input.ant-input")
    search_button =(By.XPATH, '//button[text()="Tìm kiếm"]')
    GoiThau = (By.CSS_SELECTOR, ".content__body__left__item__infor")
    bntToday = (By.CSS_SELECTOR,".ant-calendar-today-btn ")
    bntNext=(By.CSS_SELECTOR,".el-icon.el-icon-arrow-right")