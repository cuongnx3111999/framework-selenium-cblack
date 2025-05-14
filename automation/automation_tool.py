import argparse
import os
import sys
import time
from utils.driver_factory import DriverFactory
from utils.config_reader import ConfigReader
from pages.base_page import BasePage


# Import các page object khác nếu cần

def parse_arguments():
    parser = argparse.ArgumentParser(description='Automation Tool')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox', 'edge'],
                        help='Browser to use for automation')
    parser.add_argument('--env', default='dev', choices=['dev', 'staging', 'prod'],
                        help='Environment to run automation on')

    return parser.parse_args()

def main():
    args = parse_arguments()

    # Get environment configuration
    env = ConfigReader.get_environment_config(args.env)

    # Initialize webdriver
    driver = DriverFactory.get_driver(args.browser, headless=False)



    # driver.quit()


if __name__ == "__main__":
    main()
