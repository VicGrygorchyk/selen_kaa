from selenium.webdriver.remote.webdriver import WebDriver

from se_wrapper.utils.custom_types import TimeoutType
from se_wrapper.waits import Wait


class ElementWaits:
    """True if condition is fulfilled else throws exception."""

    def __init__(self, se_web_element, webdriver: WebDriver, timeout: TimeoutType):
        self._wait = Wait(webdriver)
        self._web_element = se_web_element
        self._timeout = timeout

    def be_visible(self, timeout: TimeoutType):
        """True when an element is visible on the html page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._wait.element_to_be_visible(self._web_element, timeout=timeout_)

    def be_invisible(self, timeout: TimeoutType):
        """True if an element is not visible on the html page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._wait.element_to_be_invisible(self._web_element, timeout_)

    def have_class(self, expected_class: str, timeout: TimeoutType):
        """True when an element has a specific class.
        :param expected_class: class_name for expected class (not css_selector).
        :param timeout: time to wait for an element to have a class name.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._wait.element_to_get_class(self._web_element, expected_class, timeout_)

    def include_element(self, child_css_selector: str, timeout: TimeoutType):
        """True when an element gets a desired child element.
        :param child_css_selector: a css selector for a child element.
        :param timeout: time to wait for the condition.

        """
        timeout_ = timeout if timeout else self._timeout
        return self._wait.element_to_include_child_element(
            self._web_element,
            child_css_selector,
            timeout_
        )

    def contain_text(self, text: str, timeout: TimeoutType):
        """True if an element contains a provided text in its text attribute.
        :param text: expected text.
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._wait.element_to_contain_text(self._web_element, text, timeout_)

    def have_similar_text(self, text: str, timeout: TimeoutType):
        """True if an element has a similar text in texts attribute.
        Not precise comparision, e.g. returns True for:
        "some" in "this is some text", " test\n" and "test", "TEST" and "test"
        :param text: a text to compare for similarity.
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._wait.element_have_similar_text(self._web_element, text, timeout_)

    def have_exact_text(self, text: str, timeout: TimeoutType):
        """True if an element has exactly provided text, and no other text.
        Precise comparision, e.g. returns False if "some" == "this is some text"
        :param text: exact text to search inside an element
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._wait.element_to_have_exact_text(self._web_element, text, timeout_)

    def not_present_in_dom(self, timeout: TimeoutType):
        """True for an element to be stale or absent in DOM.
        :param timeout: equal to the self.timeout if other not passed.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._wait.element_not_present(self._web_element, timeout_)

    def be_on_the_screen(self, timeout: TimeoutType):
        """True for an element is present on the screen (inside the viewport).
        Checks if element's coordinates match viewport height and width.
        Different from `to_be_visible` as `to_be_visible` checks element has size > 1px
        and display is not `:none`.
        :param timeout: equal to the self.timeout if other not passed.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        return self._wait.element_to_be_in_viewport(self._web_element, timeout_)
