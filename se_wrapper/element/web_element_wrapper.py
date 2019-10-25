from abc import ABC


class WebElementWrapper(ABC):
    """Abstract class for wrapped web element.
    Used for type reference. Shall be implemented in separate class.
    """

    def __init__(self):
        raise NotImplementedError()
