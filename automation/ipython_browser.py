#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.driver_factory import DriverFactory
from utils.config_reader import ConfigReader
# Import các page objects khác nếu cần
import argparse
import sys
import time
import IPython

URL=""

def setup_ipython_environment():
    """Thiết lập môi trường IPython với các đối tượng đã khởi tạo sẵn."""
    parser = argparse.ArgumentParser(description='IPython Interactive Selenium Browser')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox', 'edge'],
                        help='Browser to use')
    parser.add_argument('--env', default='dev', choices=['dev', 'staging', 'prod'],
                        help='Environment to connect to')
    parser.add_argument('--url', default=None,
                        help='Initial URL to navigate to (optional)')

    args = parser.parse_args()

    print(f"Initializing {args.browser} browser in IPython mode...")
    driver = DriverFactory.get_driver(args.browser, headless=False)
    driver.maximize_window()

    env_config = ConfigReader.get_environment_config(args.env)
    print(f"Connected to environment: {args.env}")

    # Tạo các page objects

    # Điều hướng đến URL nếu được cung cấp
    if args.url:
        print(f"Navigating to: {args.url}")
        driver.get(args.url)
    else:
        base_url = env_config.get("url", URL)
        print(f"Navigating to base URL: {base_url}")
        driver.get(base_url)

    # Tạo namespace
    namespace = {
        'driver': driver,
        'env_config': env_config,
        # Thêm các đối tượng page khác nếu cần
    }

    print("\n============ IPython Interactive Browser Session ============")
    print("Available objects:")
    for var_name, var_obj in namespace.items():
        print(f" - {var_name}: {var_obj.__class__.__name__}")

    print("\nExample commands:")
    print(" - driver.get('https://google.com')")
    print(" - element = driver.find_element('id', 'some_id')")
    print(" - search_page.navigate_to_homepage(env_config)")
    print(" - search_page.search_for_product('laptop')")
    print("\nPress Ctrl+D to exit IPython. Remember to run driver.quit() before exiting.")

    return namespace


if __name__ == "__main__":
    # Thiết lập môi trường và lấy các biến
    namespace = setup_ipython_environment()

    # Bắt đầu IPython shell với các biến đã được định nghĩa
    IPython.start_ipython(argv=[], user_ns=namespace)

    # Kiểm tra xem người dùng đã đóng trình duyệt chưa
    if 'driver' in namespace and hasattr(namespace['driver'], 'session_id'):
        try:
            # Kiểm tra xem trình duyệt còn mở không
            _ = namespace['driver'].window_handles
            print("Browser is still open. Closing...")
            namespace['driver'].quit()
        except:
            print("Browser was already closed.")

