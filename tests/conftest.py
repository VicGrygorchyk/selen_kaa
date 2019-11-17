import os
import time
import copy

import pytest

from tests.webapp.setup import BROWSER_LOG, DRIVER_LOG
from tests.webapp.app import App
from tests.webapp.browser_manager import BrowserManager
from tests.webapp.setup import BROWSER_WIDTH, BROWSER_HEIGHT


TEST_REPORTS_DIR = "./test_reports"
LOG_DIR = TEST_REPORTS_DIR + "/logs/"
SCREENSHOTS_DIR = TEST_REPORTS_DIR + "/screenshots/"


# pylint:disable=redefined-outer-name

def pytest_addoption(parser):
    """Command line options for test run"""
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests with: 'chrome' only for now"
    )
    parser.addoption(
        "--usegrid", action="store_true", default=False, help="If specified, test will run on grid"
    )
    parser.addoption(
        "--grid_uri", action="store",
        help="URI of grid hub"
    )
    parser.addoption(
        "--use_vd", action="store_true", default=False, help="If true - run tests in virtual displays."
    )


@pytest.fixture()
def app(request, browser_mg: BrowserManager):
    web_driver = browser_mg.web_driver
    application = App(web_driver)

    def teardown():
        """Save a screenshot and a log if test failed."""
        try:
            if request.node.rep_call.failed:
                make_screenshots_logs_dir()
                web_driver.get_screenshot_as_file(format_screenshot_log_name(directory=SCREENSHOTS_DIR,
                                                                             extension=".png"))
                logs = application.web_driver.get_log(BROWSER_LOG)
                logs.extend(application.web_driver.get_log(DRIVER_LOG))
                write_logs(logs, format_screenshot_log_name(directory=LOG_DIR, extension=".txt"))
        finally:
            web_driver.quit()

    request.addfinalizer(teardown)
    return application


@pytest.fixture(scope="session", autouse=True)
def virtual_display(request):
    """Starts virtual displays with session scope, where runs all tests."""
    is_virt_display = request.config.getoption("--use_vd")
    if is_virt_display:
        try:
            from pyvirtualdisplay.smartdisplay import SmartDisplay
            from pyvirtualdisplay.abstractdisplay import XStartTimeoutError
        except ImportError:
            raise ImportError("Virtual display Works only for Linux.\n"
                              "Please, install:\n"
                              "sudo apt-get install xserver-xephyr\n"
                              "pip install PyVirtualDisplay\n"
                              "pip install pyscreenshot\n"
                              "pip install xlib")
        virt_display = SmartDisplay(visible=1, size=(BROWSER_WIDTH, BROWSER_HEIGHT))
        try:
            virt_display.start()
        except XStartTimeoutError:
            # repeat the start if error
            virt_display.start()

        def teardown():
            virt_display.stop()

        request.addfinalizer(teardown)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Helper function to obtain test run status"""
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # change Test Report output to console if result failed
    # make output shorter
    if rep:
        if rep.longrepr and rep.outcome == "failed":
            error_msg = rep.longrepr
            error_msg.reprtraceback.reprentries = _parse_traceback(error_msg.reprtraceback.reprentries)
            rep.longrepr = error_msg
            outcome.force_result(rep)
    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


def _parse_traceback(traceback):
    """Remove all logs except first and last.
    Show only last 4 lines of each log.
    """
    show_lines = 4
    copy_tb = copy.deepcopy(traceback)
    for log in copy_tb:
        if log is copy_tb[0] or log is copy_tb[-1]:
            lines_ = copy.deepcopy(log.lines)
            log.lines = lines_[:1]
            log.lines.append("...")
            log.lines.extend(lines_[-show_lines:])
        else:
            copy_tb.remove(log)
    return copy_tb


def format_screenshot_log_name(directory, extension):
    test_path = os.environ.get('PYTEST_CURRENT_TEST').split(" ").pop(0)
    full_name = test_path.split(os.sep).pop()
    timestamp = time.strftime("%Y%m%d-%H:%M")

    return "".join([directory, full_name, timestamp, extension])


def write_logs(log, filename):
    with open(filename, 'a') as file_log:
        for line in log:
            file_log.write(f"{line}\n")


def make_screenshots_logs_dir():
    """ Make a screenshots and logs directory """
    for one_dir in [SCREENSHOTS_DIR, LOG_DIR]:
        if not os.path.exists(one_dir):
            os.makedirs(one_dir)
