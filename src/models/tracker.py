"""Main tracker class"""

from datetime import date
from typing import List

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
        from ..core import Scheduler
        # Import here to avoid circular imports
        self.scheduler: Scheduler = Scheduler()

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

        # Use scheduler to determine which tasks fit
        scheduled_tasks, total_time_used = self.scheduler.schedule_tasks(
            self.tasks, self.available_time
        )

        # Create and return the schedule
        schedule = Schedule(date_, self.available_time, scheduled_tasks)
        return schedule

    def get_schedule_explanation(self, schedule: Schedule) -> str:
        """Get explanation for why tasks were scheduled this way."""
        return self.scheduler.explain_scheduling(
            schedule.scheduled_tasks, schedule.available_time, schedule.total_time_used
        )

    def get_summary(self) -> str:
        """Get summary of owner and their pets."""
        summary = f"Owner: {self.owner_name}\n"
        summary += f"Pets: {len(self.pets)}\n"
        for pet in self.pets:
            summary += f"- {pet.get_info()}\n"
        return summary
