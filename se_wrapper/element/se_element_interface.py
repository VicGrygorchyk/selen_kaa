from abc import ABC


class SeElementInterface(ABC):
    """Abstract class for wrapped web element.
    Used for type reference. Shall be implemented in separate class.
    """

    @property
    def web_element(self):
        raise NotImplementedError()

    @web_element.setter
    def web_element(self, element):
        raise NotImplementedError()

    def get_web_element_by_timeout(self, timeout):
        raise NotImplementedError()

    @property
    def selector(self):
        raise NotImplementedError()
