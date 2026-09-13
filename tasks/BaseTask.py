from colorama import Fore, Style, init
from datetime import datetime
from loguru import logger
import sys
class BaseTask:
    def __init__(self, task_id, description):
        self.task_id = task_id
        self.description = description
        self.state = 0
        logger.remove()
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>T{extra[task_id]} - {level: <8}</level> | <level>{message}</level>"
        )
        logger.level("PRE EDIT", no=21, color="<blue><bold>")
        logger.level("PRE-PASS", no=22, color="<yellow><bold>")
        logger.level("PROCESS", no=23, color="<cyan><bold>")
        logger.level("POST-PASS", no=24, color="<magenta><bold>")
        logger.level("PRE SAVE", no=26, color="<green><bold>")
        self._logger = logger.bind(task_id=self.task_id)

    def _preprocess(self, wikicode):
        self.state = 0
    
    def _process(self, wikicode):
        self.state = 1

    def _postprocess(self, wikicode):
        self.state = 2

    def run(self):
        self._log("INFO", f"{self.description} - Starting task.")
    def _log(self, level, message):
        self._logger.log(level, message)

    def _log_state(self, message):
        if self.state == 0:
            self._logger.log("PRE EDIT", message)
        elif self.state == 1:
            self._logger.log("PRE-PASS", message)
        elif self.state == 2:
            self._logger.log("PROCESS", message)
        elif self.state == 3:
            self._logger.log("POST-PASS", message)
        elif self.state == 4:
            self._logger.log("PRE SAVE", message)