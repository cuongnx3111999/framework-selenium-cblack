import os
import datetime


class Screenshot:
    @staticmethod
    def capture_screenshot(driver, test_name):
        """
        Capture screenshot and save it to the screenshots directory.
        Returns the path to the saved screenshot.
        """
        screenshots_dir = os.path.join(os.path.dirname(__file__), '../reports/screenshots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{test_name}_{timestamp}.png"
        file_path = os.path.join(screenshots_dir, file_name)

        driver.save_screenshot(file_path)
        return file_path
