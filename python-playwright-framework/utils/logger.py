"""
Logger utility for test execution logging
Provides structured logging with different levels
"""

import logging
import os
from pathlib import Path
from datetime import datetime


class Logger:
    """Custom logger for test automation"""
    
    def __init__(self, log_file_name: str = "test_execution.log", console_output: bool = True):
        # Create logs directory
        logs_dir = Path(os.getcwd()) / "reports" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = logs_dir / log_file_name
        self.console_output = console_output
        
        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
    
    def _get_emoji(self, level: str) -> str:
        """Get emoji for log level"""
        emojis = {
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'DEBUG': '🐛',
            'SUCCESS': '✅',
            'START': '🚀',
            'END': '🏁'
        }
        return emojis.get(level, '')
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(f"{self._get_emoji('INFO')} {message}")
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(f"{self._get_emoji('WARNING')} {message}")
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(f"{self._get_emoji('ERROR')} {message}")
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(f"{self._get_emoji('DEBUG')} {message}")
    
    def success(self, message: str) -> None:
        """Log success message"""
        self.logger.info(f"{self._get_emoji('SUCCESS')} {message}")
    
    def test_start(self, test_name: str) -> None:
        """Log test start"""
        self.logger.info(f"{self._get_emoji('START')} Test Started: {test_name}")
    
    def test_end(self, test_name: str, status: str) -> None:
        """Log test end"""
        emoji = '✅' if status == 'PASSED' else '❌'
        self.logger.info(f"{emoji} Test {status}: {test_name}")
    
    def step(self, step_description: str) -> None:
        """Log step in test"""
        self.logger.info(f"  📌 Step: {step_description}")
    
    def api(self, method: str, endpoint: str, status: int, duration: float) -> None:
        """Log API request/response"""
        self.logger.info(
            f"🌐 API {method} {endpoint} - Status: {status} - Duration: {duration:.2f}ms"
        )


# Singleton instance
logger = Logger()
