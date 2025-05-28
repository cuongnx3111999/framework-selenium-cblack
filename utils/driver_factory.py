from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from .config_reader import ConfigReader

class DriverFactory:
    @staticmethod
    def get_driver(browser_name=None, headless=False):
        """
        Initialize and return a WebDriver instance based on the specified browser.
        If no browser is specified, it uses the default browser from config.
        """
        if not browser_name:
            browser_name = ConfigReader.get_config_value("default_browser", "chrome")

        browser_name = browser_name.lower()
        browser_config = ConfigReader.get_browser_config(browser_name)

        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Thêm các argument mặc định từ config (nếu có)
            for arg in browser_config.get("arguments", []):
                options.add_argument(arg)

            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            # THÊM CÁC ARGUMENT MỚI CỦA BẠN TẠI ĐÂY
            # Ví dụ:
            options.add_argument("--start-maximized")  # Mở Chrome ở chế độ toàn màn hình
            options.add_argument("--disable-infobars")  # Tắt thanh thông tin "Chrome is being controlled by automated test software"
            options.add_argument("--disable-extensions") # Tắt các tiện ích mở rộng
            options.add_argument("--disable-gpu") # Cần thiết cho một số môi trường headless, hoặc khi chạy trong Docker
            options.add_argument("--no-sandbox") # Cần thiết khi chạy với quyền root (ví dụ trong Docker)
            options.add_argument("--disable-dev-shm-usage") # Khắc phục sự cố với không gian bộ nhớ chia sẻ trong Docker
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36") # Thay đổi User-Agent
            options.add_argument("--incognito") # Mở ở chế độ ẩn danh
            # options.add_argument("--window-size=1920,1080") # Thiết lập kích thước cửa sổ
            # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

            for key, value in browser_config.get("preferences", {}).items():
                options.add_experimental_option("prefs", {key: value})

            if headless:
                options.add_argument("--headless") # Đảm bảo argument này được thêm nếu headless=True

            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser_name == "firefox":
            # ... (mã cho Firefox giữ nguyên) ...
            options = webdriver.FirefoxOptions()
            for arg in browser_config.get("arguments", []):
                options.add_argument(arg)

            if headless:
                options.add_argument("--headless")

            profile = webdriver.FirefoxProfile()
            for key, value in browser_config.get("preferences", {}).items():
                profile.set_preference(key, value)

            options.profile = profile

            return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)


        elif browser_name == "edge":
            # ... (mã cho Edge giữ nguyên) ...
            options = webdriver.EdgeOptions()
            for arg in browser_config.get("arguments", []):
                options.add_argument(arg)

            if headless:
                options.add_argument("--headless")

            return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")