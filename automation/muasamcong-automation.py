import argparse
import os
import sys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_factory import DriverFactory
from utils.config_reader import ConfigReader
from pages.base_page import BasePage
from locators.muasamcong_locator import muasamcongLocator
from time import sleep


def parse_arguments():
    parser = argparse.ArgumentParser(description='Automation Tool')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox', 'edge'],
                        help='Browser to use for automation')
    parser.add_argument('--env', default='dev', choices=['dev', 'staging', 'prod'],
                        help='Environment to run automation on')
    parser.add_argument('--headless', action='store_true',
                        help='Run in headless mode')
    parser.add_argument('--output', default='file/all_tenders.csv',
                        help='Path to output file')
    parser.add_argument('--search-term', default='Thuốc',
                        help='Term to search for')

    return parser.parse_args()


def init_driver(browser, env, headless=False):
    """Khởi tạo và trả về đối tượng WebDriver"""
    # Get environment configuration
    env_config = ConfigReader.get_environment_config(env)

    # Initialize webdriver
    driver = DriverFactory.get_driver(browser, headless=headless)

    # Cài đặt timeout mặc định
    driver.implicitly_wait(10)

    return driver


def extract_tender_data(tender_item):
    """Trích xuất thông tin từ một element gói thầu"""
    data = {}

    try:
        # 1. Mã TBMT
        bid_code_element = tender_item.find_element(By.CLASS_NAME, "content__body__left__item__infor__code")
        if bid_code_element:
            bid_code_text = bid_code_element.text.strip()
            data["ma_tbmt"] = bid_code_text.split(":")[-1].strip()

        # 2. Trạng thái
        status_element = tender_item.find_element(By.CLASS_NAME, "content__body__left__item__infor__notice--be")
        if status_element:
            data["trang_thai"] = status_element.text.strip()

        # 3. Tên gói thầu
        name_element = tender_item.find_element(By.CLASS_NAME, "content__body__left__item__infor__contract__name")
        if name_element:
            data["ten_goi_thau"] = name_element.text.strip()

        # Thông tin khác
        other_info_elements = tender_item.find_elements(By.CLASS_NAME, "format__text")
        for element in other_info_elements:
            text = element.text.strip()
            if "Bên mời thầu" in text:
                data["ben_moi_thau"] = text.split(":")[-1].strip()
            elif "Chủ đầu tư" in text:
                data["chu_dau_tu"] = text.split(":")[-1].strip()
            elif "Ngày đăng tải thông báo" in text:
                data["ngay_dang_tai"] = text.split(":")[-1].strip()
            elif "Lĩnh vực" in text:
                data["linh_vuc"] = text.split(":")[-1].strip()

        # Địa điểm
        try:
            location_element = tender_item.find_element(By.XPATH, ".//h6[contains(text(), 'Địa điểm')]/span")
            if location_element:
                data["dia_diem"] = location_element.text.strip()
        except Exception:
            data["dia_diem"] = ""

        # Thời điểm đóng thầu
        try:
            closing_time_elements = tender_item.find_elements(By.XPATH,
                                                              ".//div[contains(@class, 'content__body__right__item__infor__contract')]//h1")
            if len(closing_time_elements) >= 2:
                time = closing_time_elements[0].text.strip()
                date = closing_time_elements[1].text.strip()
                data["thoi_diem_dong_thau"] = f"{time} {date}"
        except Exception:
            data["thoi_diem_dong_thau"] = ""

        # Hình thức dự thầu
        try:
            bid_form_element = tender_item.find_element(By.XPATH,
                                                        ".//p[contains(text(), 'Hình thức dự thầu')]/following-sibling::h1")
            if bid_form_element:
                data["hinh_thuc_du_thau"] = bid_form_element.text.strip()
        except Exception:
            data["hinh_thuc_du_thau"] = ""

        # URL chi tiết
        try:
            link_element = tender_item.find_element(By.XPATH, ".//a[contains(@href, 'muasamcong.mpi.gov.vn')]")
            if link_element:
                data["url_chi_tiet"] = link_element.get_attribute("href")
        except Exception:
            data["url_chi_tiet"] = ""

    except Exception as e:
        print(f"Lỗi khi trích xuất dữ liệu: {str(e)}")

    return data


def ensure_output_directory(output_path):
    """Đảm bảo thư mục đầu ra tồn tại"""
    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def main():
    args = parse_arguments()

    driver = None
    all_tenders = []

    try:
        # Khởi tạo driver
        driver = init_driver(args.browser, args.env, args.headless)
        base_page = BasePage(driver)
        locators = muasamcongLocator()

        # Mở trang web
        URL = "https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?render=search"
        driver.get(URL)

        # Đợi cho trang tải xong và xử lý thông báo nếu có
        wait = WebDriverWait(driver, 20)

        # Xử lý thông báo nếu xuất hiện
        if base_page.is_element_present(locators.NOTIC):
            base_page.click(locators.X_NOTE)

        # Nhập thông tin tìm kiếm
        wait.until(EC.visibility_of_element_located(locators.TimTheoThuoc))
        base_page.send_keys(locators.TimTheoThuoc, args.search_term)

        # Xử lý chọn ngày từ calendar
        calendar_inputs = base_page.find_elements(locators.Caledar_input_NgayPheDuyet)

        # Chọn ngày đầu
        base_page.click(calendar_inputs[0])
        sleep(2)
        base_page.wait_for_element(locators.bntToday)
        base_page.click(locators.bntToday)

        # Chọn ngày cuối
        base_page.click(calendar_inputs[1])
        sleep(2)
        base_page.wait_for_element(locators.bntToday)
        base_page.click(locators.bntToday)

        # Nhấn tìm kiếm
        base_page.click(locators.search_button)

        sleep(10)

        # Xử lý phân trang và thu thập dữ liệu
        page_count = 1
        try:
            while True:
                print(f"Đang xử lý trang {page_count}...")
                # Thu thập dữ liệu từ các gói thầu
                tender_items = base_page.find_elements(locators.GoiThau)
                for tender_item in tender_items:
                    tender_data = extract_tender_data(tender_item)
                    all_tenders.append(tender_data)
                    print(f"Đã thu thập: {tender_data.get('ma_tbmt', 'Unknown')}")

                # Kiểm tra có thể chuyển trang tiếp theo không
                next_button = base_page.find_element(locators.bntNext)
                if next_button.get_attribute("disabled"):
                    print("Đã đến trang cuối cùng.")
                    break

                # Chuyển đến trang tiếp theo
                base_page.click(locators.bntNext)

                # Đợi page load xong
                wait.until(EC.staleness_of(tender_items[0]))
                wait.until(EC.presence_of_element_located(locators.GoiThau))

                page_count += 1
        except Exception as e:
            print(f"Lỗi khi thực thi: {str(e)}")
            import traceback
            traceback.print_exc()
        # Lưu kết quả vào file CSV
        if all_tenders:
            df = pd.DataFrame(all_tenders)

            # Đảm bảo thư mục đầu ra tồn tại
            ensure_output_directory(args.output)

            # Lưu file với định dạng phù hợp
            file_extension = os.path.splitext(args.output)[1].lower()
            if file_extension == '.csv':
                df.to_csv(args.output, index=False, encoding='utf-8')
            elif file_extension == '.xlsx':
                df.to_excel(args.output, index=False)
            elif file_extension == '.json':
                df.to_json(args.output, orient='records', force_ascii=False, indent=4)
            else:
                # Mặc định là txt/csv
                df.to_csv(args.output, index=False, encoding='utf-8', sep=',')

            print(f"Đã lưu {len(all_tenders)} gói thầu vào file {args.output}")
        else:
            print("Không tìm thấy gói thầu nào.")

    except Exception as e:
        print(f"Lỗi khi thực thi: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Đóng driver khi hoàn thành
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
