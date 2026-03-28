"""Schedule model class"""

from datetime import date
from typing import List

from .task import Task


class Schedule:
    """Represents a finalized daily schedule of pet care tasks."""

    def __init__(self, date_: date, available_time: int, scheduled_tasks: List[Task] = None):
        """
        Initialize a Schedule.

        Args:
            date_: Date for the schedule
            available_time: Available time in minutes for the day
            scheduled_tasks: List of tasks that have been scheduled (optional)
        """
        self.date = date_
        self.available_time = available_time
        self.scheduled_tasks: List[Task] = scheduled_tasks or []
        self.total_time_used = sum(
            task.duration * task.frequency for task in self.scheduled_tasks
        )

    def is_feasible(self) -> bool:
        """Check if scheduled tasks fit within available time."""
        return self.total_time_used <= self.available_time

    def get_daily_plan(self) -> str:
        """Get the daily plan as a formatted string."""
        plan = f"Daily Plan for {self.date}\n"
        plan += f"Available time: {self.available_time} mins\n"
        plan += f"Used time: {self.total_time_used} mins\n"
        plan += f"Remaining time: {self.available_time - self.total_time_used} mins\n\n"
        
        if self.scheduled_tasks:
            plan += "Scheduled Tasks:\n"
            for task in self.scheduled_tasks:
                plan += f"- {task.get_task_info()}\n"
        else:
            plan += "No tasks scheduled.\n"
        
        return plan
