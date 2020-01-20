from selen_kaa.waits import Wait

from tests.webapp.pages.index_page import IndexPage
from tests.webapp.setup import URL


class WebApp:

    def __init__(self, web_driver):
        self.web_driver = web_driver
        self.wait = Wait(self.web_driver)

    def goto_index_page(self):
        self.web_driver.get(URL)
        return IndexPage(self.web_driver)
