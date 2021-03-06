"""Just a class to verify the wrapping works"""
import re
import time
import logging

from selenium.common.exceptions import WebDriverException, UnexpectedAlertPresentException

from selen_kaa.webdriver import SeWebDriver
from selen_kaa.element.se_web_element import SeWebElement
from selen_kaa.utils import se_utils


DEFAULT_TIMEOUT = 7
TimeoutType = se_utils.TimeoutType


class WebElementWrapper(SeWebElement):

    def should_be_unclickable(self, timeout: TimeoutType = 0.1):
        try:
            self.click(timeout)
        except ElementNotClickableError:
            return True
        return False


class ElementNotClickableError(WebDriverException):
    """ Special exception for cases where element can't receive a click. """

    @staticmethod
    def can_handle_exception(error: WebDriverException):
        pattern = re.compile(r"is not clickable at point \([0-9]+, [0-9]+\). Other element would receive the click:")
        return pattern.search(error.msg) is not None


class DriverWrapper(SeWebDriver):

    def __init__(self, webdriver):
        super().__init__(webdriver)

    @staticmethod
    def be_idle_for(sleeptime):
        """Just sleep, when you need it.
        Warning! Don't use for wait element, better check out 'wait' functions.
        """
        time.sleep(sleeptime)

    def get_screenshot_as_png(self):
        try:
            return self.webdriver.get_screenshot_as_png()
        except (WebDriverException, UnexpectedAlertPresentException):
            logging.error("Unable to get a screenshot from WebDriver.")

    def init_web_element(self, selector: str, timeout: TimeoutType = 1):
        return WebElementWrapper(self.webdriver, selector, timeout)

    def init_all_web_elements(self, selector: str, timeout: TimeoutType = None):
        arr = super().init_all_web_elements(selector, timeout)
        arr.element_type = WebElementWrapper
        return arr
