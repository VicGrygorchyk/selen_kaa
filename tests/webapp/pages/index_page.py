

THE_SAME_CLASS = ".well.the-same-class"


class IndexPage:

    def __init__(self, webdriver):
        self._webdriver = webdriver
        self.the_same_text = self._webdriver.init_all_web_elements(THE_SAME_CLASS)

