import sys
from typing import Optional


class Logger:
    LEVELS = {"debug": 10, "info": 20, "warning": 30, "error": 40, "success": 25}
    COLORS = {
        "debug": "\033[36m",
        "info": "\033[34m",
        "warning": "\033[33m",
        "error": "\033[31m",
        "success": "\033[32m",
        "reset": "\033[0m",
    }

    def __init__(self):
        self.level = self.LEVELS["info"]

    def set_level(self, level: str):
        self.level = self.LEVELS.get(level, 20)

    def get_level(self) -> int:
        return self.level

    def _log(self, msg: str, level: str):
        if self.level <= self.LEVELS[level]:
            color = self.COLORS.get(level, "")
            reset = self.COLORS["reset"]
            print(f"{color}[{level.upper()}]{reset} {msg}", file=sys.stderr if level in ("error",) else sys.stdout)

    def debug(self, msg: str):
        self._log(msg, "debug")

    def info(self, msg: str):
        self._log(msg, "info")

    def warning(self, msg: str):
        self._log(msg, "warning")

    def error(self, msg: str):
        self._log(msg, "error")

    def success(self, msg: str):
        self._log(msg, "success")


logger = Logger()
