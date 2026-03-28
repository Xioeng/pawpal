"""Scheduler - handles task scheduling logic and algorithms"""

from __future__ import annotations

from typing import List

from ..models import Task


class Scheduler:
    """Handles scheduling logic and task optimization."""

    def __init__(self):
        """Initialize the scheduler."""
        pass

    def schedule_tasks(
        self, tasks: List["Task"], available_time: int
    ) -> tuple[List["Task"], int]:
        """
        Schedule tasks by priority and available time.

        Args:
            tasks: List of tasks to schedule
            available_time: Available time in minutes

        Returns:
            Tuple of (scheduled_tasks, total_time_used)
        """
        # Sort tasks by priority (high to low)
        sorted_tasks = sorted(tasks, key=lambda t: t.priority)

        scheduled_tasks = []
        total_time_used = 0

        # Greedily add tasks if they fit
        for task in sorted_tasks:
            task_time = task.duration * task.frequency
            if total_time_used + task_time <= available_time:
                scheduled_tasks.append(task)
                total_time_used += task_time

        return scheduled_tasks, total_time_used

    def is_feasible(self, tasks: List["Task"], available_time: int) -> bool:
        """
        Check if all tasks can fit within available time.

        Args:
            tasks: List of tasks to check
            available_time: Available time in minutes

        Returns:
            True if all tasks fit, False otherwise
        """
        total_time = sum(task.duration * task.frequency for task in tasks)
        return total_time <= available_time

    def explain_scheduling(
        self, scheduled_tasks: List["Task"], available_time: int, total_time_used: int
    ) -> str:
        """
        Explain the scheduling decisions.

        Args:
            scheduled_tasks: Tasks that were scheduled
            available_time: Available time
            total_time_used: Total time used by scheduled tasks

        Returns:
            Explanation string
        """
        explanation = "Scheduling Logic:\n"
        explanation += "1. Tasks sorted by priority (HIGH → MEDIUM → LOW)\n"
        explanation += "2. Tasks added greedily if they fit in available time\n"
        explanation += f"3. Available time: {available_time} mins\n"
        explanation += f"4. Time used: {total_time_used} mins\n"
        explanation += f"5. Tasks scheduled: {len(scheduled_tasks)}\n"

        if total_time_used < available_time:
            explanation += (
                f"6. Time remaining: {available_time - total_time_used} mins\n"
            )

        return explanation
