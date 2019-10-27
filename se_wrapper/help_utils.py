from re import match
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from se_wrapper.element.wrapped_element_interface import WrappedElementInterface


ElementType = Union[str, WebElement, WrappedElementInterface]
TimeoutType = Union[int, float]
DEFAULT_TIMEOUT = 4


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
