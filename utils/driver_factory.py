from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from .config_reader import ConfigReader
import os


class DriverFactory:
    @staticmethod
    def get_driver(browser_name=None, headless=None):
        """
        Initialize and return a WebDriver instance based on the specified browser.
        If no browser is specified, it uses the default browser from config.
        """
        if not browser_name:
            browser_name = ConfigReader.get_config_value("default_browser", "chrome")

        if headless is None:
            headless = ConfigReader.get_config_value("headless", False)
        browser_name = browser_name.lower()
        browser_config = ConfigReader.get_browser_config(browser_name)

        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            for arg in browser_config.get("arguments", []):
                options.add_argument(arg)

            for key, value in browser_config.get("preferences", {}).items():
                options.add_experimental_option("prefs", {key: value})

            if headless:
                options.add_argument("--headless")

            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser_name == "firefox":
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
            options = webdriver.EdgeOptions()
            for arg in browser_config.get("arguments", []):
                options.add_argument(arg)

            if headless:
                options.add_argument("--headless")

            return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
