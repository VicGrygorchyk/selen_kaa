import os

from tests.webapp.server.app import app


class WebApp:

    def __init__(self, web_driver):
        self.web_driver = web_driver
        # port = int(os.environ.get("PORT", 5000))
        # app.run(debug=True, port=port)

    def print(self):
        print("Hello")
