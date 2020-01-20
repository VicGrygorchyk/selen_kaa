from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from selen_kaa.utils import custom_types
from selen_kaa.utils.se_utils import get_selector_type
from selen_kaa.element.element_waits import ElementWaits
from selen_kaa.element.se_element_interface import SeElementInterface
from selen_kaa.element.expectations import Expectations


TimeoutType = custom_types.TimeoutType


class SeWebElement(SeElementInterface):
    """Class is used to provide a lazy initialization of the WebElement.
    WebElement is going to be searched only when is called.
    Web element can be declared in __init__ of the page class and be found only when needed for interaction.

    """

    DEFAULT_TIMEOUT = 4

    def __init__(self, webdriver: WebDriver, selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self._webdriver = webdriver
        self._selector = selector
        self._element = None
        self._expect = None
        self._should = None

    @property
    def web_element(self):
        """Get reference to Selenium WebElement."""
        return self.get_web_element_by_timeout(self.timeout)

    def get_web_element_by_timeout(self, timeout):
        if self._element is None:
            try:
                return WebDriverWait(self._webdriver, timeout).until(
                    presence_of_element_located((get_selector_type(self.selector), self.selector))
                )
            except TimeoutException as exc:
                raise NoSuchElementException(f"Web Element with selector {self.selector} has not been found."
                                             f"\n{exc.msg}")
        return self._element

    @web_element.setter
    def web_element(self, element: WebElement):
        self._element = element

    @property
    def selector(self):
        """Shall be css selector."""
        return self._selector

    @property
    def expect(self) -> Expectations:
        """Expect returns True if the condition is positive till timeout is reached,
        after timeout it returns False.
        """
        if self._expect is None:
            self._expect = Expectations(self, self._webdriver, self.timeout)
        return self._expect

    @property
    def should(self) -> ElementWaits:
        """Should returns True if the condition is positive till timeout is reached,
        otherwise it throws TimeoutException.
        """
        if self._should is None:
            self._should = ElementWaits(self, self._webdriver, self.timeout)
        return self._should

    def __getattr__(self, attr):
        """Calls method or properties on self.web_element.
        Returns callable or attribute of WebElement.
        :param attr: any attr of the WebElement
        """
        try:
            orig_attr = self.web_element.__getattribute__(attr)
            if callable(orig_attr):
                def hooked(*args, **kwargs):
                    return orig_attr(*args, **kwargs)
                return hooked
            return orig_attr
        except AttributeError as exc:
            raise AttributeError(f"WebElement has no attribute {attr}.\n{exc}")

    def set_text_value(self, input_val):
        """Clears the input area before sending a new text value."""
        self.web_element.clear()
        self.web_element.send_keys(input_val)

    def get_class(self):
        """Get class of element."""
        return self.web_element.get_attribute("class")

    def __repr__(self):
        return f"Selen-kaa WebElement with selector `{self.selector}`."
