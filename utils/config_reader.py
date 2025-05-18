import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class ConfigReader:
    @staticmethod
    def load_config(file_path):
        """Load configuration from a JSON file."""
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def get_browser_config(browser_name="chrome"):
        """Get browser configuration."""
        file_path = os.path.join(os.path.dirname(__file__), '../config/browsers.json')
        browsers = ConfigReader.load_config(file_path)
        return browsers.get(browser_name, {})

    @staticmethod
    def get_environment_config(env="dev"):
        """Get environment configuration."""
        file_path = os.path.join(os.path.dirname(__file__), '../config/environments.json')
        environments = ConfigReader.load_config(file_path)
        return environments.get(env, {})

    @staticmethod
    def get_base_config():
        """Get base configuration."""
        file_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
        return ConfigReader.load_config(file_path)

    @staticmethod
    def get_config_value(key, default=None):
        """Get a specific configuration value."""
        config = ConfigReader.get_base_config()
        return config.get(key, default)
