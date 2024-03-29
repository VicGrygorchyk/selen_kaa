from re import match

from selenium.webdriver.common.by import By
from selen_kaa.utils import custom_types


TimeoutType = custom_types.TimeoutType


def get_selector_type(selector: str):
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
