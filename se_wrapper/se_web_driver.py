""" Wrapper around Selenium WebDriver.
 Calls all methods on self._webdriver.
 Added some method for usability.

"""
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from se_wrapper.waits import Wait
from se_wrapper import help_utils


TimeoutType = help_utils.TimeoutType


class SeWebDriver:

    def __init__(self, webdriver: WebDriver):
        self._webdriver: WebDriver = webdriver
        self._wait_for = Wait(self._webdriver)

    def find_element_by_css(self, selector: str, timeout: TimeoutType) -> WebElement:
        """ Universal method to look for the web element by provided selector.
        Checks if selector is css or xpath, then waits for element.
        If element not present in DOM raises NoSuchElementException,
        if wait reached timeout, raises TimeOutException.
        :param selector: str as css selector or xpath
        :param timeout: int
        :return: WebElement

        """
        try:
            if self._wait_for.element_be_in_dom(selector, timeout=timeout):
                return self._webdriver.find_element(by=help_utils.get_selector_type(selector), value=selector)
            raise NoSuchElementException(msg=f"Can't find element with locator='{selector}'")
        except TimeoutException:
            raise NoSuchElementException(msg=f"Waited {timeout} seconds. Can't find element with locator='{selector}'")

    def find_all_elements_by_css(self, selector: str, timeout: TimeoutType) -> List[WebElement]:
        """ Universal method to look for the web elements by provided selector.
        Checks if selector is css or xpath, then wait for elements.
        If no element present, returns empty list
        :param selector: str
        :param timeout: int
        :return: list[type: WebElement]

        """
        result = []
        try:
            if self._wait_for.element_be_in_dom(selector, timeout=timeout):
                result = self._webdriver.find_elements(by=help_utils.get_selector_type(selector), value=selector)
        except TimeoutException:
            pass
        return result
