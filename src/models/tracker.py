"""Main tracker class"""

from datetime import date
from typing import List

from .enums import Priority
from .pet import Pet
from .schedule import Schedule
from .task import Task


class PetCareTracker:
    """Main controller for pet care tracking and scheduling."""

    def __init__(self, owner_name: str, available_time: int = 480):
        """
        Initialize the tracker.

        Args:
            owner_name: Name of the pet owner
            available_time: Available time per day in minutes (default 8 hours)
        """
        self.owner_name = owner_name
        self.available_time = available_time
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the tracker."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add a task to the tracker."""
        self.tasks.append(task)

    def create_daily_schedule(self, date_: date = None) -> Schedule:
        """
        Create a daily schedule considering constraints.

        Args:
            date_: Date for the schedule (default today)

        Returns:
            Schedule object with optimized task ordering
        """
        if date_ is None:
            date_ = date.today()

        schedule = Schedule(date_, self.available_time)

        # Sort tasks by priority (high to low)
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority)

        # Try to add each task to schedule
        for task in sorted_tasks:
            schedule.add_task_to_schedule(task)

        return schedule

    def get_summary(self) -> str:
        """Get summary of owner and their pets."""
        summary = f"Owner: {self.owner_name}\n"
        summary += f"Pets: {len(self.pets)}\n"
        for pet in self.pets:
            summary += f"- {pet.get_info()}\n"
        return summary
