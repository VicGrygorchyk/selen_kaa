""" Wrapper around Selenium WebDriver.
 Calls all methods on self._webdriver.
 Added some method for usability.

"""
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from se_wrapper.element.wrapped_webelement import WrappedWebElement
from se_wrapper.waits import Wait
from se_wrapper import help_utils


DEFAULT_TIMEOUT = help_utils.DEFAULT_TIMEOUT
TimeoutType = help_utils.TimeoutType


class BrowserDriver:

    def __init__(self, webdriver: WebDriver):
        self._webdriver: WebDriver = webdriver
        self.wait_for = Wait(self._webdriver)

    def __getattr__(self, attr):
        """Calls method or properties on self._webdriver.
        Returns callable or attribute of WebDriver.
        :param attr: any attr of the WebDriver
        :return: Any

        """
        try:
            orig_attr = self._webdriver.__getattribute__(attr)
            if callable(orig_attr):
                def hooked(*args, **kwargs):
                    result = orig_attr(*args, **kwargs)
                    # prevent recursion
                    if result == self._webdriver:
                        return self
                    return result
                return hooked
            return orig_attr
        except AttributeError as exc:
            raise AttributeError(f"WebDriver has no attribute {attr}.\n{exc}")

    @property
    def action_chains(self):
        return ActionChains(self._webdriver)

    def init_web_element(self, selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT) -> WrappedWebElement:
        """Init a new WebElementWrapper.
        :param selector: str as css selector or xpath
        :param timeout: time to wait until element appears
        :return: WebElementAdapter
        """
        if selector is None:
            raise Exception("Selector should be not empty.")
        return WrappedWebElement(self, selector, timeout)

    def find_element_by_css(self, selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT) -> WebElement:
        """ Universal method to look for the web element by provided selector.
        Checks if selector is css or xpath, then waits for element.
        If element not present in DOM raises NoSuchElementException,
        if wait reached timeout, raises TimeOutException.
        :param selector: str as css selector or xpath
        :param timeout: int
        :return: WebElement

        """
        try:
            if self.wait_element_be_in_dom(selector, timeout=timeout):
                return self._webdriver.find_element(by=help_utils.get_selector_type(selector), value=selector)
            raise NoSuchElementException(msg=f"Can't find element with locator='{selector}'")
        except TimeoutException:
            raise TimeoutException(msg=f"Waited {timeout} seconds. Can't find element with locator='{selector}'")

    def find_all_elements_by_css(self, selector: str, timeout=DEFAULT_TIMEOUT) -> List[WebElement]:
        """ Universal method to look for the web elements by provided selector.
        Checks if selector is css or xpath, then wait for elements.
        If no element present, returns empty list
        :param selector: str
        :param timeout: int
        :return: list[type: WebElement]

        """
        result = []
        try:
            if self.wait_for.element_be_in_dom(selector, timeout=timeout):
                result = self._webdriver.find_elements(by=self.get_selector_type(selector), value=selector)
        except TimeoutException:
            pass
        return result

