

THE_SAME_CLASS = ".well.the-same-class"
SHOW_DIV_BTN = "#click-to-make-el-visible"
HIDE_DIV_BTN = "#click-to-make-el-invisible"
TEST_DIV_VISIBILITY = "#five-sec-visible"


class IndexPage:

    def __init__(self, webdriver):
        self._webdriver = webdriver
        self.the_same_text = self._webdriver.init_all_web_elements(THE_SAME_CLASS)
        self.btn_show_div = self._webdriver.init_web_element(SHOW_DIV_BTN)
        self.btn_hide_div = self._webdriver.init_web_element(HIDE_DIV_BTN)
        self.test_div = self._webdriver.init_web_element(TEST_DIV_VISIBILITY)
        self.no_such_element = self._webdriver.init_web_element(".no-such-class-for-no-element")
