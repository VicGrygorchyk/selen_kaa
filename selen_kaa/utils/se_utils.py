from re import match
from typing import List

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selen_kaa.utils import custom_types


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
