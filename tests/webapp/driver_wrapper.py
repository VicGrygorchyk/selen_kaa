"""Just a class to verify the wrapping works"""
import re
import time
import logging

from selenium.common.exceptions import WebDriverException, UnexpectedAlertPresentException

from se_wrapper.browser_driver import BrowserDriver
from se_wrapper.element.se_web_element import SeWebElement
from se_wrapper.element.se_elements_array import SeElementsArray
from se_wrapper.web_driver_config import WebDriverConfig
from se_wrapper.utils import se_utils


DEFAULT_TIMEOUT = 7
TimeoutType = se_utils.TimeoutType


class WebElementWrapper(SeWebElement):

    def __init__(self, webdriver, selector, timeout=DEFAULT_TIMEOUT):
        super().__init__(webdriver, selector, timeout)

    def should_be_unclickable(self, timeout: TimeoutType = 0.1):
        """ Tries to click element to check if it clickable.
        Unclickable element should throw ElementNotClickableException.
        As this method tries to click an element, it's safe to use only on expected unclickable, otherwise,
        an element would trigger onclick event.
        :return: if element can handle click. :type: bool
        """
        try:
            self.click(timeout)
        except ElementNotClickableError:
            return True
        return False


class WrappedElementsArray(SeElementsArray):

    def __init__(self, webdriver, css_selector, timeout):
        super().__init__(webdriver, css_selector, WebElementWrapper, timeout)


class ElementNotClickableError(WebDriverException):
    """ Special exception for cases where element can't receive a click. """

    @staticmethod
    def can_handle_exception(error: WebDriverException):
        pattern = re.compile(r"is not clickable at point \([0-9]+, [0-9]+\). Other element would receive the click:")
        return pattern.search(error.msg) is not None


class Config(WebDriverConfig):

    WrappedElementType: type = WebElementWrapper
    WrappedElementArrayType: type = WrappedElementsArray
    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT


class DriverWrapper(BrowserDriver):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.config = Config()

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
