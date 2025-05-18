from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = ConfigReader.get_config_value("timeout", 10)

    def open_url(self, url):
        """Open a URL."""
        self.driver.get(url)

    def get_title(self):
        """Get the page title."""
        return self.driver.title

    def find_element(self, locator_or_element):
        """Find an element by locator (By, value) or return the element if it's already an element."""
        if isinstance(locator_or_element, tuple):
            # Locator format: (By.XXX, "value")
            return self.driver.find_element(*locator_or_element)
        else:
            # Element itself
            return locator_or_element

    def find_elements(self, locator):
        """Find elements by locator (By, value)."""
        return self.driver.find_elements(*locator)

    def find_element_by_text(self, text, element_type="*"):
        """Find element by exact text."""
        xpath = f"//{element_type}[text()='{text}']"
        return self.driver.find_element(By.XPATH, xpath)

    def find_element_containing_text(self, text, element_type="*"):
        """Find element containing specific text."""
        xpath = f"//{element_type}[contains(text(),'{text}')]"
        return self.driver.find_element(By.XPATH, xpath)

    def find_button_by_text(self, text):
        """Find button by exact text."""
        return self.find_element_by_text(text, element_type="button")

    def is_element_present(self, locator_or_element):
        """Check if an element is present."""
        try:
            self.find_element(locator_or_element)
            return True
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def wait_for_element(self, locator_or_element, timeout=None):
        """Wait for an element to be visible."""
        if timeout is None:
            timeout = self.timeout

        wait = WebDriverWait(self.driver, timeout)
        try:
            if isinstance(locator_or_element, tuple):
                # Locator format: (By.XXX, "value")
                element = wait.until(EC.visibility_of_element_located(locator_or_element))
            else:
                # Element itself
                element = wait.until(EC.visibility_of(locator_or_element))
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not visible after {timeout} seconds")

    def wait_for_clickable(self, locator_or_element, timeout=None):
        """Wait for an element to be clickable."""
        if timeout is None:
            timeout = self.timeout

        wait = WebDriverWait(self.driver, timeout)
        try:
            if isinstance(locator_or_element, tuple):
                # Locator format: (By.XXX, "value")
                element = wait.until(EC.element_to_be_clickable(locator_or_element))
            else:
                # Element itself
                element = wait.until(EC.element_to_be_clickable(locator_or_element))
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not clickable after {timeout} seconds")

    def click(self, locator_or_element):
        """Click an element."""
        element = self.wait_for_clickable(locator_or_element)
        element.click()

    def click_button_by_text(self, button_text):
        """Click a button with the given text."""
        button = self.find_button_by_text(button_text)
        self.click(button)

    def send_keys(self, locator_or_element, text):
        """Input text to an element."""
        element = self.wait_for_element(locator_or_element)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator_or_element):
        """Get text from an element."""
        element = self.wait_for_element(locator_or_element)
        return element.text

    def is_displayed(self, locator_or_element):
        """Check if an element is displayed."""
        try:
            element = self.find_element(locator_or_element)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
            return False

    def get_element_by_placeholder(self, placeholder_text):
        """Find an element by placeholder text."""
        return self.driver.find_element(By.CSS_SELECTOR, f'input[placeholder="{placeholder_text}"]')

    def get_element_by_partial_placeholder(self, partial_placeholder):
        """Find an element by partial placeholder text."""
        return self.driver.find_element(By.CSS_SELECTOR, f'input[placeholder*="{partial_placeholder}"]')
