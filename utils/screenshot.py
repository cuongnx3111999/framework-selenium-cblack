import os
from datetime import datetime
from pathlib import Path


class Screenshot:
    @staticmethod
    def get_screenshot_dir():
        """
        Tạo và trả về đường dẫn thư mục lưu screenshot
        """
        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        return screenshot_dir

    @staticmethod
    def generate_filename(test_name, status=""):
        """
        Tạo tên file screenshot duy nhất

        Args:
            test_name: Tên của test case
            status: Trạng thái test (fail, pass, etc.)

        Returns:
            str: Tên file screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status_prefix = f"{status}_" if status else ""
        # Đảm bảo tên file an toàn
        safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in test_name)
        return f"{status_prefix}{safe_name}_{timestamp}.png"

    @classmethod
    def capture_screenshot(cls, driver, test_name, status=""):
        """
        Chụp ảnh màn hình và lưu vào thư mục reports/screenshots

        Args:
            driver: WebDriver instance
            test_name: Tên của test case
            status: Trạng thái của test (fail, pass, etc.)

        Returns:
            str: Đường dẫn đến file ảnh đã lưu
            None: Nếu có lỗi xảy ra
        """
        try:
            screenshot_dir = cls.get_screenshot_dir()
            filename = cls.generate_filename(test_name, status)
            screenshot_path = screenshot_dir / filename

            # Chụp màn hình
            driver.save_screenshot(str(screenshot_path))

            # Kiểm tra file đã được tạo thành công
            if os.path.exists(screenshot_path):
                print(f"Screenshot đã được lưu tại: {screenshot_path}")
                return str(screenshot_path)
            else:
                print(f"Không thể lưu screenshot tại: {screenshot_path}")
                return None

        except Exception as e:
            print(f"Lỗi khi chụp màn hình: {str(e)}")
            return None