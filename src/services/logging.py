import logging
import sys
from pathlib import Path
from typing import Optional


class CustomFormatter(logging.Formatter):
    """Formatter customizado com cores para diferentes níveis de log"""

    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
        "RESET": "\033[0m",
    }

    EMOJIS = {
        "DEBUG": "🔍",
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🔥",
    }

    def format(self, record):
        levelname = record.levelname
        color = self.COLORS.get(levelname, self.COLORS["RESET"])
        emoji = self.EMOJIS.get(levelname, "")

        record.levelname = f"{color}{emoji} {levelname}{self.COLORS['RESET']}"

        return super().format(record)


class GameLogger:
    """
    Customized logger for the game application
    """

    def __init__(self, name: str = "BancoImobiliario", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = CustomFormatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        if log_file:
            self._add_file_handler(log_file)

    def _add_file_handler(self, log_file: str):
        """Adiciona handler para salvar logs em arquivo"""
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)


_logger_instance = None


def get_logger(
    name: str = "BancoImobiliario", log_file: Optional[str] = None
) -> GameLogger:
    """Retorna instância única do logger"""
    global _logger_instance

    if _logger_instance is None:
        _logger_instance = GameLogger(name, log_file)
    return _logger_instance


# Logger singleton
logger = get_logger(log_file="logs/game.log")
