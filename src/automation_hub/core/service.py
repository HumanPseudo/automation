from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

class BaseService(ABC):
    """Base class for all service integrations."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the service."""
        pass

    @abstractmethod
    def disconnect(self):
        """Clean up connection."""
        pass
