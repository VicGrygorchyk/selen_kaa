"""Wrapper around Selenium WebDriver.
 Calls all methods on self._webdriver.
 Added some method for usability.

"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ActionChains

from selen_kaa.global_config import DEFAULT_TIMEOUT
from selen_kaa.utils import custom_types
from selen_kaa.element.se_web_element import SeWebElement
from selen_kaa.element.se_elements_array import SeElementsArray


TimeoutType = custom_types.TimeoutType


class SeWebDriver:

    def __init__(self, webdriver: WebDriver):
        self.webdriver: WebDriver = webdriver

    def __getattr__(self, attr):
        """Calls method or properties on self._webdriver.
        Returns callable or attribute of WebDriver.
        :param attr: any attr of the WebDriver
        :return: Any

        """
        try:
            orig_attr = self.webdriver.__getattribute__(attr)
            if callable(orig_attr):
                def hooked(*args, **kwargs):
                    result = orig_attr(*args, **kwargs)
                    # prevent recursion
                    if result == self.webdriver:
                        return self
                    return result
                return hooked
            return orig_attr
        except AttributeError as exc:
            raise AttributeError(f"WebDriver has no attribute {attr}.\n{exc}")

    @property
    def action_chains(self):
        return ActionChains(self.webdriver)

    def init_web_element(self, selector: str, timeout: TimeoutType = None, locator_strategy=None) -> SeWebElement:
        """Init a new WrappedWebElement.
        Lazy initialization. Element would be called on the time of first interaction.
        :param selector: str as any locator, css selector or xpath
        :param timeout: time to wait until element appears
        :param locator_strategy: field of class `selenium.webdriver.common.by::By` or `MobileBy` for Appium
        :return: SeWebElement
        """
        if selector is None:
            raise Exception("Selector should be not empty.")

        timeout_ = DEFAULT_TIMEOUT
        if timeout or timeout == 0:
            timeout_ = timeout
        return SeWebElement(self.webdriver, selector, timeout_, locator_strategy)

    def init_all_web_elements(self, selector: str, timeout: TimeoutType = None, locator_strategy=None) -> SeElementsArray:
        """Init a list with references to WrappedWebElement.
        Lazy initialization. All elements would be called on the time of first interaction
        with any of the elements.
        :param selector: str as any locator, css selector or xpath
        :param timeout: time to wait until element appears
        :param locator_strategy: field of class `selenium.webdriver.common.by::By` or `MobileBy` for Appium
        :return: List of SeWebElement
        """
        timeout_ = DEFAULT_TIMEOUT
        if timeout or timeout == 0:
            timeout_ = timeout
        arr = SeElementsArray(self.webdriver, selector, timeout_, locator_strategy)
        arr.element_type = SeWebElement
        return arr
