from selenium.common.exceptions import TimeoutException

from se_wrapper.utils import custom_types
from se_wrapper.element.element_waits import ElementWaits

TimeoutType = custom_types.TimeoutType


class Expectations(ElementWaits):
    """True if expectation is fulfilled else False.
    Errors are handled by returning False.
    """

    def be_visible(self, timeout: TimeoutType):
        """True when an element is visible on the html page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self._timeout
        try:
            return super().be_visible(timeout=timeout_)
        except TimeoutException:
            return False

    def be_invisible(self, timeout: TimeoutType):
        """True if an element is not visible on the page.
        :param timeout: time to wait element visibility.

        """
        timeout_ = timeout if timeout else self._timeout
        try:
            return super().be_invisible(timeout=timeout_)
        except TimeoutException:
            return False

    def have_class(self, expected_class: str, timeout: TimeoutType):
        """True when an element has a specific class.
        :param expected_class: class_name for expected class (not css_selector).
        :param timeout: time to wait for an element ho have a class name.

        """
        timeout_ = timeout if timeout else self._timeout
        try:
            return super().have_class(expected_class, timeout=timeout_)
        except TimeoutException:
            return False

    def include_element(self, child_css_selector: str, timeout: TimeoutType):
        """True when an element gets a desired child element.
        :param child_css_selector: a css selector for a child element.
        :param timeout: time to wait for the condition.

        """
        timeout_ = timeout if timeout else self._timeout
        try:
            return super().include_element(child_css_selector, timeout_)
        except TimeoutException:
            return False

    def contain_text(self, text: str, timeout: TimeoutType):
        """True if an element contains a provided text in its text attribute.
        :param text: expected text.
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        try:
            return super().contain_text(text, timeout_)
        except TimeoutException:
            return False

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
        try:
            return super().have_similar_text(text, timeout_)
        except TimeoutException:
            return False

    def have_exact_text(self, text: str, timeout: TimeoutType):
        """True if an element has exactly provided text, and no other text.
        Precise comparision, e.g. returns False if "some" == "this is some text"
        :param text: exact text to search inside an element
        :param timeout: time to wait for the condition.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        try:
            return super().have_exact_text(text, timeout_)
        except TimeoutException:
            return False

    def not_present_in_dom(self, timeout: TimeoutType):
        """True for an element to be stale or absent in DOM.
        :param timeout: equal to the self.timeout if other not passed. :type: int

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        try:
            return super().not_present_in_dom(timeout_)
        except TimeoutException:
            return False

    def be_on_the_screen(self, timeout: TimeoutType):
        """True for an element is present on the screen (inside the viewport).
        False if element's coordinates don't match viewport height and width.
        :param timeout: equal to the self.timeout if other not passed.

        """
        timeout_ = self._timeout
        if timeout:
            timeout_ = timeout
        try:
            return super().be_on_the_screen(timeout_)
        except TimeoutException:
            return False
