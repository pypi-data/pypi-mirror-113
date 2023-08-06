import logging
import subprocess


class WebBrowserOpener:
    _logging = logging.getLogger(__name__)
    SYS_COMMAND_OPEN = "open"

    def open(self, command_string):
        subprocess.call([self.SYS_COMMAND_OPEN, command_string])
