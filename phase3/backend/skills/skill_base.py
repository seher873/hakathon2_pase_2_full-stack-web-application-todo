"""
Base class for all AI skills in the Phase-3 system.

All skills should inherit from this base class to ensure consistent interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from uuid import UUID


class SkillBase(ABC):
    """
    Abstract base class for all skills in the AI system.
    """

    def __init__(self, base_url: str = None):
        """
        Initialize the skill with a base URL.

        Args:
            base_url: Base URL for API calls (defaults to system configuration)
        """
        self.base_url = base_url

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill with the provided parameters.

        Args:
            **kwargs: Skill-specific parameters

        Returns:
            Dictionary containing the result of the operation
        """
        pass

    def validate_parameters(self, **kwargs) -> bool:
        """
        Validate the provided parameters before execution.

        Args:
            **kwargs: Skill-specific parameters

        Returns:
            True if parameters are valid, False otherwise
        """
        return True