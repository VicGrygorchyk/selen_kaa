from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from se_wrapper.browser_driver import BrowserDriver
from se_wrapper.help_utils import TimeoutType


class Condition:

    def __init__(self, webdriver: BrowserDriver, web_element: WebElement, timeout: TimeoutType):
        self.webdriver = webdriver
        self.web_element = web_element
        self.timeout = timeout
        self._expected_positive = True

    def to_be_displayed(self, timeout: TimeoutType):
        """True when an element is visible on the html page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self.timeout
        return self.webdriver.wait_for.element_to_appear(self.web_element, timeout=timeout_)

    def not_to_be_displayed(self, timeout: TimeoutType):
        """True if an element is not visible on the html page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self.timeout
        return self.webdriver.wait_for.element_to_disappear(self.web_element, timeout=timeout_)

    def have_class(self, expected_class: str, timeout: TimeoutType):
        """True when an element has a specific class.
        :param expected_class: class_name for expected class (not css_selector).
        :param timeout: time to wait for an element ho have a class name.

        """
        timeout_ = timeout if timeout else self.timeout
        return self.webdriver.wait_for.element_to_get_class(self.web_element, expected_class, timeout=timeout_)

    def not_have_class(self, expected_class: str, timeout: TimeoutType):
        """True when an element doesn't have a specific class.
        :param expected_class: class_name for expected class (not css_selector).
        :param timeout: time to wait for an element ho have a class name.

        """
        timeout_ = timeout if timeout else self.timeout
        try:
            self.webdriver.wait_for.element_to_get_class(self.web_element, expected_class, timeout=timeout_)
            return
        except TimeoutException as exc:


    def should_have_element(self, child_selector, timeout=None):
        """
        Wait until web_element get a desired child element.
        :param child_selector: str
        :param timeout: int
        :return: bool.
        """
        timeout_ = timeout if timeout else self.timeout
        result = False
        try:
            if self.webdriver.wait_element_be_in_dom(child_selector, timeout=timeout_):
                if self.find_element(by=self.webdriver.get_selector_type(child_selector), value=child_selector):
                    result = True
            return result
        except TimeoutException:
            raise TimeoutException(msg=f"{self.selector} has no element with locator='{child_selector}'")

    def should_contain_text(self, text: str, timeout=None):
        """ Checks element has provided text in texts attribute.
        Not precise comparision, e.g. returns True for:
        "some" in "this is some text", " test\n" and "test", "TEST" and "test"
        :param text: str
        :param timeout: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        return self.webdriver.wait_element_have_similar_text(self.selector, text, timeout=timeout_)

    def should_have_exact_text(self, text: str, timeout=None):
        """ Checks element has exactly provided text, and no other text.
        Precise comparision, e.g. returns False if "some" == "this is some text"
        :param text: str
        :param timeout: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        if self.webdriver.wait_element_to_contain_text(self.selector, text, timeout=timeout_):
            return self.webdriver.find_element_by_selector(self.selector).text == text
        return False

    def should_be_stale(self, timeout=None):
        """ Check for web element to be stale or absent on the html page.
        :param timeout: equal to the self.timeout if other not passed. :type: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        return self.webdriver.wait_element_staleness(self.selector, timeout=timeout_)

    def should_be_invisible(self, timeout=None):
        """ Check for web element to be invisible to the end user.
        :param timeout: equal to the self.timeout if other not passed. :type: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        return self.webdriver.wait_element_invisibility(self.selector, timeout=timeout_)
