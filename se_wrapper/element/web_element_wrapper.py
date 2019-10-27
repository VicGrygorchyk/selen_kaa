from abc import ABC


class WebElementWrapper(ABC):
    """Abstract class for wrapped web element.
    Used for type reference. Shall be implemented in separate class.
    """

    @property
    def web_element(self):
        raise NotImplementedError()
