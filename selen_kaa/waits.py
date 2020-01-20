import time
from typing import Callable

from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from selen_kaa.errors import TIMEOUT_BASE_ERR_MSG
from selen_kaa.utils import se_utils
from selen_kaa.element.se_element_interface import SeElementInterface
from selen_kaa.utils import custom_types
from selen_kaa.utils.custom_funcs import single_dispatch


TimeoutType = custom_types.TimeoutType
ElementType = custom_types.ElementType


class Wait:

    DEFAULT_TIMEOUT = 4
    PULL_FREQUENCY = 0.2

    def __init__(self, webdriver: WebDriver):
        self._webdriver: WebDriver = webdriver

    def element_be_in_dom(self, selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        if not isinstance(selector, str):
            raise TypeError("Selector should be a string for `element_be_in_dom()` method.")
        return self._set_condition_for_wait(selector, ec.presence_of_element_located, timeout)

    @single_dispatch
    def element_to_be_visible(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        self._check_target_type(target)

        def wrapped_visible():
            target.get_web_element_by_timeout(self.PULL_FREQUENCY)
            return target if target.is_displayed() else False

        return self.wait_fluently(wrapped_visible, timeout,
                                  TIMEOUT_BASE_ERR_MSG.format(timeout, target.selector, "be visible"))

    @element_to_be_visible.register(str)
    def __element_to_be_visible_str(self, target: str, timeout=DEFAULT_TIMEOUT):
        return self._set_condition_for_wait(target, ec.visibility_of_element_located, timeout)

    @element_to_be_visible.register(WebElement)
    def __element_to_be_visible_we(self, target: WebElement, timeout=DEFAULT_TIMEOUT):
        return self._wait_until(ec.visibility_of(target), timeout)

    @single_dispatch
    def element_to_be_invisible(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """True if the element is not present and/or not visible.
        Difference from `element_not_present`: returns True if element is not visible,
        but it's still present in DOM.
        """
        self._check_target_type(target)

        def wrapped_webelement_disappears():
            try:
                # init web_element within wait's timeout, not web_element's
                target.get_web_element_by_timeout(self.PULL_FREQUENCY)
                if target.web_element.is_displayed():
                    return False
                # return True if element is not stale and is not displayed
                return target
            except (NoSuchElementException, StaleElementReferenceException):
                return target

        return self.wait_fluently(wrapped_webelement_disappears, timeout,
                                  TIMEOUT_BASE_ERR_MSG.format(timeout, target.selector, "disappear"))

    @element_to_be_invisible.register(str)
    def __element_to_be_invisible_str(self, target: str, timeout):
        return self._set_condition_for_wait(target, ec.invisibility_of_element_located, timeout)

    @element_to_be_invisible.register(WebElement)
    def __element_to_be_invisible_we(self, target: WebElement, timeout):
        return self._wait_until(ec.invisibility_of_element(target), timeout)

    @single_dispatch
    def element_not_present(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """True if there is no NoSuchElementException or StaleElementReferenceException.
        Element should be neither visible, nor enabled, nor be present in DOM.
        """
        self._check_target_type(target)

        def no_wrapped_webelement_in_dom():
            try:
                target.get_web_element_by_timeout(self.PULL_FREQUENCY)
                if target.web_element.is_enabled():
                    return False
                # return False even element isn't enabled, but still present
                return False
            except (NoSuchElementException, StaleElementReferenceException):
                return target

        return self.wait_fluently(no_wrapped_webelement_in_dom, timeout,
                                  TIMEOUT_BASE_ERR_MSG.format(timeout, target.selector, "not be present in DOM"))

    @element_not_present.register(str)
    def __element_not_present_str(self, target: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        return self._set_condition_for_wait(target, ec.invisibility_of_element_located, timeout)

    @element_not_present.register(WebElement)
    def __element_not_present_we(self, target: WebElement, timeout: TimeoutType = DEFAULT_TIMEOUT):
        return self._wait_until(ec.staleness_of(target), timeout)


    @single_dispatch
    def element_to_contain_text(self, target: ElementType, text: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait for text attribute of the web element to contain expected text.
        True for `in` comparision, e.g. "test" in "some test here".
        """
        self._check_target_type(target)

        def has_text_in_target():
            target.get_web_element_by_timeout(self.PULL_FREQUENCY)
            return target if text in target.text else False

        err_msg = f"TimeoutException while waited {timeout} for the element {target.selector} to contain text '{text}'. " \
                  f"Actual text '{target.text}'"

        return self.wait_fluently(has_text_in_target, timeout, err_msg)

    @element_to_contain_text.register(str)
    def __element_to_contain_text_str(self, target: str, text: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        return self._wait_until(ec.text_to_be_present_in_element((se_utils.get_selector_type(target), target), text),
                                timeout)

    @element_to_contain_text.register(WebElement)
    def __element_to_contain_text_we(self, target: WebElement, text: str, timeout: TimeoutType = DEFAULT_TIMEOUT):

        def has_text_in_target():
            return target if text in target.text else False

        err_msg = f"TimeoutException while waited {timeout} for the element to contain text '{text}'. " \
                  f"Actual text '{target.text}'"

        return self.wait_fluently(has_text_in_target, timeout, err_msg),


    @single_dispatch
    def element_to_have_exact_text(self, target: ElementType, text: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait for the web element to have exact text
        True for exact comparision of expected text with actual text attribute of web element.
        """
        self._check_target_type(target)

        def has_exact_text_in_target():
            target.get_web_element_by_timeout(self.PULL_FREQUENCY)
            return target if text == target.text else False

        err_msg = f"TimeoutException while waited {timeout} for the element {target.selector} " \
                  f"to have exact text '{text}'. Actual text '{target.text}'"

        return self.wait_fluently(has_exact_text_in_target, timeout, err_msg)

    @element_to_have_exact_text.register(str)
    def __element_to_have_exact_text_str(self, target: str, text: str, timeout=DEFAULT_TIMEOUT):
        return self._wait_until(ec.text_to_be_present_in_element((se_utils.get_selector_type(target), target), text),
                                timeout)

    @element_to_have_exact_text.register(WebElement)
    def __element_to_have_exact_text_we(self, target: WebElement, text: str, timeout=DEFAULT_TIMEOUT):

        def has_exact_text_in_target():
            return target if text == target.text else False

        err_msg = f"TimeoutException while waited {timeout} for the element to have exact text '{text}'." \
                  f" Actual text '{target.text}'"
        return self.wait_fluently(has_exact_text_in_target, timeout, err_msg),

    @single_dispatch
    def element_have_similar_text(self, target: ElementType, text: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait until web element contains expected text.
        Returns True if similar text.
        This method is different from `wait_element_to_contain_text`,
        as it ignores whitespaces, newtabs, cases for similarity comparision.
        """
        self._check_target_type(target)
        target.get_web_element_by_timeout(timeout)
        element = target
        return self._element_have_similar_text_helper(element, text, timeout)

    def _element_have_similar_text_helper(self, element, text, timeout):
        text_ = None

        def get_text_in_element():
            """Func to check if element contains similar text."""
            nonlocal text_
            if text_ is None:
                text_ = element.text
            element_text = element.text
            if element_text == text:
                return element
            if text.lower() == element_text.lower():
                return element
            if "".join(text.split()) == "".join(element_text.split()):
                return element
            return False

        return self.wait_fluently(get_text_in_element, timeout,
                                  f"TimeoutException while waited {timeout} for text '{text}'. "
                                  f"Actual text is '{text_}'")

    @element_have_similar_text.register(str)
    def __element_have_similar_text_str(self, target: str, text: str, timeout=DEFAULT_TIMEOUT):
        selector_type = se_utils.get_selector_type(target)
        element = self._webdriver.find_element(by=selector_type, value=target)
        return self._element_have_similar_text_helper(element, text, timeout)

    @element_have_similar_text.register(WebElement)
    def __element_have_similar_text_we(self, target: WebElement, text: str, timeout=DEFAULT_TIMEOUT):
        return self._element_have_similar_text_helper(target, text, timeout)

    @single_dispatch
    def element_to_get_class(self, target: ElementType, expected_class: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait until web element gets expected class."""
        self._check_target_type(target)
        target.get_web_element_by_timeout(timeout)
        element = target
        return self._wait_element_to_get_class(element, expected_class, timeout)

    def _wait_element_to_get_class(self, element, expected_class, timeout):
        class_not_expected = None

        def check_class_in_element():
            """Func to check if class is present in element.
            Driver is passed by Selenium wait() method.
            """
            nonlocal class_not_expected
            result = []
            expected_class_ls = expected_class.split(" ")
            actual_class = element.get_attribute("class")
            for class_ in expected_class_ls:
                for element_class_ in actual_class.split(" "):
                    if element_class_ == class_:
                        result.append(element)
            if len(result) == len(expected_class_ls):
                return element
            if class_not_expected is None:
                class_not_expected = actual_class
            return False

        return self.wait_fluently(check_class_in_element, timeout,
                                  f"TimeoutException while waited  {timeout} for class '{expected_class}'. "
                                  f"Actual class is '{class_not_expected}'.")

    @element_to_get_class.register(str)
    def __element_to_get_class_str(self, target: str, expected_class: str, timeout=DEFAULT_TIMEOUT):
        selector_type = se_utils.get_selector_type(target)
        element = self._webdriver.find_element(by=selector_type, value=target)
        return self._wait_element_to_get_class(element, expected_class, timeout)

    @element_to_get_class.register(WebElement)
    def __element_to_get_class_we(self, target: WebElement, expected_class: str, timeout=DEFAULT_TIMEOUT):
        return self._wait_element_to_get_class(target, expected_class, timeout)

    def url_to_contain(self, expected_url: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait until webdriver gets expected url.
        Not much difference from standard Selenium url_contain,
        except this has better error text.
        """
        error_url = None

        def get_url(driver):
            if expected_url in str(driver.current_url):
                return True
            nonlocal error_url
            error_url = driver.current_url
            return False

        try:
            return self._wait_until(get_url, timeout)
        except TimeoutException as exc:
            raise TimeoutException(msg=f"TimeoutException while waited {timeout} for url '{expected_url}'. "
                                       f"Got '{error_url}'.\n{exc.msg}")

    def page_title_contains(self, title: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait for page's title to contain a specific string."""
        return self._wait_until(condition=ec.title_contains(title), timeout=timeout)

    @single_dispatch
    def element_to_include_child_element(self, target: ElementType,
                                         child_css_selector,
                                         timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait for a web element to have another web element as a child element."""
        self._check_target_type(target)
        target.get_web_element_by_timeout(timeout)
        webelement_ = target
        return self._wait_child_element(webelement_, child_css_selector, timeout)


    def _wait_child_element(self, parent, child_css_selector, timeout):
        def nested(web_element):
            try:
                return web_element.find_element(by=se_utils.get_selector_type(child_css_selector),
                                                value=child_css_selector)
            except NoSuchElementException:
                return False

        return self.wait_fluently(lambda: nested(parent),
                                  timeout,
                                  f"TimeoutException while waiting for the element "
                                  f"to have a child '{child_css_selector}'.")

    @element_to_include_child_element.register(str)
    def _element_to_include_child_element_for_str(self, target: str,
                                                  child_css_selector,
                                                  timeout=DEFAULT_TIMEOUT):
        self.element_be_in_dom(target)
        web_element_ = self._webdriver.find_element(by=se_utils.get_selector_type(target), value=target)
        return self._wait_child_element(web_element_, child_css_selector, timeout)

    @element_to_include_child_element.register(WebElement)
    def _element_to_include_child_element_for_we(self, target: WebElement, child_css_selector, timeout=DEFAULT_TIMEOUT):
        return self._wait_child_element(target, child_css_selector, timeout)

    @single_dispatch
    def element_to_be_in_viewport(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait until element gets into viewport's coordinates."""
        target.get_web_element_by_timeout(timeout)
        return self._wait_element_in_viewport(target, timeout)

    @element_to_be_in_viewport.register(str)
    def __element_to_be_in_viewport_str(self, target: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait until element gets into viewport's coordinates."""
        self.element_be_in_dom(target)
        web_element_ = self._webdriver.find_element(by=se_utils.get_selector_type(target), value=target)
        return self._wait_element_in_viewport(web_element_, timeout)

    @element_to_be_in_viewport.register(WebElement)
    def __element_to_be_in_viewport_str(self, target: WebElement, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait until element gets into viewport's coordinates."""
        return self._wait_element_in_viewport(target, timeout)

    def _wait_element_in_viewport(self, element, timeout):
        find_viewport_pos_script = """
              var height = document.documentElement.clientHeight;
              var width = document.documentElement.clientWidth;
              var arr = [height, width];
              return arr;
          """
        rect_ = self._webdriver.execute_script(find_viewport_pos_script)
        height = rect_[0]
        width = rect_[1]
        web_element_ = element

        def get_element_pos():
            nonlocal height, width, web_element_
            pos_x = web_element_.location.get('x')
            pos_y = web_element_.location.get('y')
            if all((pos_x < width, pos_y < height)):
                return web_element_
            return None

        return self.wait_fluently(get_element_pos,
                                  timeout,
                                  f"TimeoutException while waiting {timeout} sec for element "
                                  f"to be in viewport.")

    def _wait_until(self, condition, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wrapper method around Selenium WebDriverWait() with until().
        :param condition: Selenium expected_condtions
        :param timeout: int
        :return: boolean
        """
        if not timeout:
            timeout = 0
        return wait.WebDriverWait(self._webdriver, timeout).until(condition)

    def _wait_until_not(self, condition, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wrapper method around Selenium WebDriverWait() with until_not().
        :param condition: Selenium expected_conditions
        :param timeout: int
        :return: boolean
        """
        if not timeout:
            timeout = 0
        return wait.WebDriverWait(self._webdriver, timeout).until_not(condition)

    def _set_condition_for_wait(self, selector, condition, timeout):
        by_ = se_utils.get_selector_type(selector)
        if not timeout:
            timeout = 0
        return self._wait_until(condition((by_, selector)), timeout)

    @staticmethod
    def wait_fluently(condition: Callable, timeout: TimeoutType, err_msg: str):
        """Custom wait for special cases where driver is not needed as arg for condition.
        :param condition: function to verify if Condition is True
        :param timeout: time to wait for positive condition.
        :param err_msg: error message
        :return: element if condition is True, else raises TimeoutException

        """
        if not timeout:
            timeout = 0
        start_time = time.time()
        while True:
            if time.time() - start_time >= timeout:
                raise TimeoutException(err_msg)
            res = condition()
            if res:
                return res
            time.sleep(0.3)

    @staticmethod
    def _check_target_type(target):
        if not isinstance(target, SeElementInterface):
            raise TypeError(f"Error type: {type(target)}. "
                            f"Target shall be an instance of string, WebElement or WebElementWrapper.")
