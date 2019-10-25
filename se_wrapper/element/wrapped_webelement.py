import time

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement

from se_wrapper import help_utils
from se_wrapper.browser_driver import BrowserDriver
from se_wrapper.element.web_element_wrapper import WebElementWrapper
from se_wrapper.errors import ElementNotClickableError


DEFAULT_TIMEOUT = help_utils.DEFAULT_TIMEOUT
TimeoutType = help_utils.TimeoutType


class WrappedWebElement(WebElementWrapper):
    """Class is used to provide a lazy initialization of the WebElement.
    WebElement is going to be searched only when is called.
    Web element can be declared in __init__ of the page class and be found only when needed for interaction.

    """

    def __init__(self, webdriver: BrowserDriver, selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        self.webdriver = webdriver
        self.selector = selector
        self.timeout = timeout
        self._element = None

    @property
    def web_element(self):
        """Get reference to Selenium webelement. """
        if self._element is None:
            try:
                self._element = self.webdriver.find_element_by_selector(self.selector)
            except NoSuchElementException as exc:
                raise NoSuchElementException(f"Web Element with selector {self.selector} has not been found."
                                             f"\n{exc.msg}")
        return self._element

    @web_element.setter
    def web_element(self, element: WebElement):
        self._element = element

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

    def double_click(self):
        """Click web_element two times."""
        self.web_element.click()
        self.web_element.click()

    def click(self, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """ Click element, throws ElementNotClickableException if element can't handle click.
        Wait with timeout, if click is not possible.
        """
        start_time = time.time()
        while True:
            try:
                self.web_element.click()
                break
            except WebDriverException as exc:
                if ElementNotClickableError.can_handle_exception(exc):
                    if time.time() - start_time > timeout:
                        error = f"Element location is {self.web_element.location}. {exc.msg}"
                        raise ElementNotClickableError(msg=error)
                    continue
                else:
                    raise WebDriverException(msg=exc.msg)

    def get_class(self):
        """Get class of element."""
        return self.web_element.get_attribute("class")
