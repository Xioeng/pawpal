"""Schedule model class"""

from datetime import date
from typing import List

from .task import Task


class Schedule:
    """Represents a daily schedule of pet care tasks."""

    def __init__(self, date_: date, available_time: int):
        """
        Initialize a Schedule.

        Args:
            date_: Date for the schedule
            available_time: Available time in minutes for the day
        """
        self.date = date_
        self.available_time = available_time
        self.scheduled_tasks: List[Task] = []
        self.total_time_used = 0

    def add_task_to_schedule(self, task: Task) -> bool:
        """
        Add a task to the schedule if time permits.

        Args:
            task: Task to add

        Returns:
            True if added successfully, False otherwise
        """
        if self.total_time_used + task.duration * task.frequency <= self.available_time:
            self.scheduled_tasks.append(task)
            self.total_time_used += task.duration * task.frequency
            return True
        return False

    def is_feasible(self) -> bool:
        """Check if all tasks fit within available time."""
        return self.total_time_used <= self.available_time

    def get_daily_plan(self) -> str:
        """Get the daily plan as a formatted string."""
        plan = f"Daily Plan for {self.date}\n"
        plan += f"Available time: {self.available_time} mins\n"
        plan += f"Used time: {self.total_time_used} mins\n\n"
        for task in self.scheduled_tasks:
            plan += f"- {task.get_task_info()}\n"
        return plan

    def explain_reasoning(self) -> str:
        """Explain why tasks were scheduled this way."""
        # To be implemented with scheduling logic
        pass
