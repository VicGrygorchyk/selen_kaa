from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from tests.webapp.driver_wrapper import DriverWrapper
from tests.webapp.setup import LOGS_SETUP, BROWSER_WIDTH, BROWSER_HEIGHT


class BrowserManager:

    def __init__(self, browser_type="chrome", use_grid=False, grid_uri=None, options=None):
        self.browser_type = browser_type
        self.grid_uri = grid_uri
        self.use_grid = use_grid
        self.options = options
        self._web_driver = None

    @property
    def web_driver(self):
        if self._web_driver is None:
            if self.use_grid:
                self._web_driver = DriverWrapper(self._get_remote_driver())
            else:
                if self.browser_type != "chrome":
                    raise NotImplementedError(f"Not implemented setup for {self.browser_type}")
                else:
                    self._web_driver = DriverWrapper(self._get_chrome_driver())
        return self._web_driver

    @staticmethod
    def _get_chrome_driver():
        options = ChromeOptions()
        options.add_argument('--disable-translate')
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--verbose')
        options.add_argument('--no-sandbox')
        options.set_capability("goog:loggingPrefs", LOGS_SETUP)
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
        return driver

    def _get_remote_driver(self):
        return webdriver.Remote(command_executor=self.grid_uri,
                                desired_capabilities=self.options)
