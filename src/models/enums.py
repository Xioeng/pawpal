"""Enums for PawPal models"""

from enum import Enum


class Priority(Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def __lt__(self, other):
        """Enable comparison for sorting (high < medium < low)."""
        priority_order = {
            Priority.HIGH: 0,
            Priority.MEDIUM: 1,
            Priority.LOW: 2,
        }
        return priority_order[self] < priority_order[other]
