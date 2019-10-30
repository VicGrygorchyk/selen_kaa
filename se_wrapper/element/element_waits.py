from selenium.webdriver.remote.webelement import WebElement

from se_wrapper.browser_driver import BrowserDriver
from se_wrapper.help_utils import TimeoutType


class ElementWaits:
    """True if condition is fulfilled else throws exception."""

    def __init__(self, webdriver: BrowserDriver, web_element: WebElement, timeout: TimeoutType):
        self._webdriver = webdriver
        self._web_element = web_element
        self._timeout = timeout

    def to_be_visible(self, timeout: TimeoutType):
        """True when an element is visible on the html page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._webdriver.wait_for.element_to_be_visible(self._web_element, timeout=timeout_)

    def to_be_invisible(self, timeout: TimeoutType):
        """True if an element is not visible on the html page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._webdriver.wait_for.element_to_be_invisible(self._web_element, timeout_)

    def to_have_class(self, expected_class: str, timeout: TimeoutType):
        """True when an element has a specific class.
        :param expected_class: class_name for expected class (not css_selector).
        :param timeout: time to wait for an element to have a class name.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._webdriver.wait_for.element_to_get_class(self._web_element, expected_class, timeout_)

    def to_include_element(self, child_css_selector: str, timeout: TimeoutType):
        """True when an element gets a desired child element.
        :param child_css_selector: a css selector for a child element.
        :param timeout: time to wait for the condition.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._webdriver.wait_for.element_to_include_child_element(
            self._web_element,
            child_css_selector,
            timeout_
        )

    def to_contain_text(self, text: str, timeout: TimeoutType):
        """True if an element contains a provided text in its text attribute.
        :param text: expected text.
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._webdriver.wait_for.element_to_contain_text(self._web_element, text, timeout_)

    def to_have_similar_text(self, text: str, timeout: TimeoutType):
        """True if an element has a similar text in texts attribute.
        Not precise comparision, e.g. returns True for:
        "some" in "this is some text", " test\n" and "test", "TEST" and "test"
        :param text: a text to compare for similarity.
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._webdriver.wait_for.element_have_similar_text(self._web_element, text, timeout_)

    def to_have_exact_text(self, text: str, timeout: TimeoutType):
        """True if an element has exactly provided text, and no other text.
        Precise comparision, e.g. returns False if "some" == "this is some text"
        :param text: exact text to search inside an element
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        if self._webdriver.wait_for.element_to_contain_text(self._web_element, text, timeout_):
            return self._web_element.text == text

    def not_present_in_dom(self, timeout: TimeoutType):
        """True for an element to be stale or absent in DOM.
        :param timeout: equal to the self.timeout if other not passed.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._webdriver.wait_for.no_element_in_dom(self._web_element, timeout_)
