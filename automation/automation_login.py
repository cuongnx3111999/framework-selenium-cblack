import pytest

from locators.login_locators import LoginLocators
from pages.login_page import LoginPage
from utils.pytest_data_helpers import csv_data_provider, filter_by_category, filter_by_expected_result, filter_by_expected_message
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
    parser.add_argument('--headless', default=False, action='store_true',
                        help='Run in headless mode')

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

args = parse_arguments()

driver = None
all_tenders = []

try:
    # Khởi tạo driver
    driver = init_driver(args.browser, args.env, args.headless)
    login_page = BasePage(driver)
    locators = LoginLocators()
    """Test các trường hợp đăng nhập thành công"""
    login_page = LoginPage(driver).navigate_to_login_page()
    username="Cuonga@gmail.com"
    password="Abc123456789@"
    login_page.send_keys(locators.password,password)
    login_page.click(locators.icon_eye_invisible)
    login_page.find_element(locators.password).get_attribute('value')
except Exception as e:
    print(f"Lỗi khi thực thi: {str(e)}")
    import traceback

    traceback.print_exc()

