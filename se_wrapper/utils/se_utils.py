from re import match
from typing import List

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from se_wrapper.waits import Wait
from se_wrapper.utils import custom_types


TimeoutType = custom_types.TimeoutType


def get_selector_type(selector):
    """ Checks if selector is css or xpath
    >>>get_selector_type(".css")
    css selector
    >>>get_selector_type("#css")
    css selector
    >>>get_selector_type("some attr")
    css selector
    >>>get_selector_type("./dv//")
    xpath
    >>>get_selector_type("//div")
    xpath
    >>>get_selector_type("/div")
    xpath
    """
    pattern_xpath = r"^(./)|^/"
    return By.XPATH if match(pattern_xpath, selector) else By.CSS_SELECTOR


def find_element_by_css(webdriver: WebDriver, selector: str, timeout: TimeoutType) -> WebElement:
    """ Universal method to look for the web element by provided selector.
    Checks if selector is css or xpath, then waits for element.
    If element not present in DOM raises NoSuchElementException,
    if wait reached timeout, raises TimeOutException.
    :param webdriver reference to Selenium WebDriver
    :param selector: str as css selector or xpath
    :param timeout: int
    :return: WebElement

    """
    wait_ = Wait(webdriver)
    try:
        return wait_.element_be_in_dom(selector, timeout=timeout)
    except TimeoutException:
        raise NoSuchElementException(msg=f"Waited {timeout} seconds. Can't find element with locator='{selector}'")


def find_all_elements_by_css(webdriver: WebDriver, selector: str, timeout: TimeoutType) -> List[WebElement]:
    """ Universal method to look for the web elements by provided selector.
    Checks if selector is css or xpath, then wait for elements.
    If no element present, returns empty list
    :param webdriver WebDriver
    :param selector: str
    :param timeout: int
    :return: list[type: WebElement]

    """
    result = []
    wait_ = Wait(webdriver)
    try:
        if wait_.element_be_in_dom(selector, timeout=timeout):
            result = webdriver.find_elements(by=get_selector_type(selector), value=selector)
    except TimeoutException:
        pass
    return result
