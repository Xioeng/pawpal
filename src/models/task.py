"""Task model class"""

from .enums import Priority
from .pet import Pet


class Task:
    """Represents a pet care task."""

    def __init__(
        self,
        task_type: str,
        pet: Pet,
        frequency: int,
        duration: int,
        priority: Priority = Priority.MEDIUM,
    ):
        """
        Initialize a Task.

        Args:
            task_type: Type of task (e.g., 'feeding', 'walk', 'medication')
            pet: Pet object this task is for
            frequency: How many times per day
            duration: Duration in minutes
            priority: Priority enum value (Priority.HIGH, Priority.MEDIUM, Priority.LOW)
        """
        self.task_type = task_type
        self.pet = pet
        self.frequency = frequency
        self.duration = duration
        self.priority = priority
        self.preferred_times = []

    def is_urgent(self) -> bool:
        """Check if task is urgent (high priority)."""
        return self.priority == Priority.HIGH

    def get_task_info(self) -> str:
        """Get task details as a string."""
        return f"{self.task_type} for {self.pet.name}: {self.frequency}x/day, {self.duration} mins"
