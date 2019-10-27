from re import compile

from selenium.common.exceptions import WebDriverException


class ElementNotClickableError(WebDriverException):
    """ Special exception for cases where element can't receive a click. """

    @staticmethod
    def can_handle_exception(error: WebDriverException):
        pattern = compile(r"is not clickable at point \([0-9]+, [0-9]+\). Other element would receive the click:")
        return pattern.search(error.msg) is not None
