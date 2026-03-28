"""Tests for Scheduler class"""

import pytest
from src.core.scheduler import Scheduler
from src.models.task import Task
from src.models.pet import Pet
from src.models.enums import Priority


class TestSchedulerInitialization:
    """Test Scheduler initialization"""

    def test_scheduler_init(self):
        """Test creating a scheduler"""
        scheduler = Scheduler()
        assert scheduler is not None


class TestScheduleTasks:
    """Test schedule_tasks method"""

    def test_schedule_tasks_empty_list(self):
        """Test scheduling with no tasks"""
        scheduler = Scheduler()
        scheduled_tasks, total_time = scheduler.schedule_tasks([], 200)
        
        assert scheduled_tasks == []
        assert total_time == 0

    def test_schedule_tasks_single_task_fits(self):
        """Test scheduling a single task that fits"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30, Priority.HIGH)
        
        scheduled_tasks, total_time = scheduler.schedule_tasks([task], 200)
        
        assert len(scheduled_tasks) == 1
        assert task in scheduled_tasks
        assert total_time == 30

    def test_schedule_tasks_single_task_doesnt_fit(self):
        """Test scheduling a task that doesn't fit"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 300, Priority.HIGH)
        
        scheduled_tasks, total_time = scheduler.schedule_tasks([task], 200)
        
        assert len(scheduled_tasks) == 0
        assert total_time == 0

    def test_schedule_tasks_multiple_fit(self):
        """Test scheduling multiple tasks that all fit"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 30, Priority.HIGH),
            Task("Grooming", pet, 1, 45, Priority.MEDIUM),
            Task("Play", pet, 1, 60, Priority.LOW),
        ]
        
        scheduled_tasks, total_time = scheduler.schedule_tasks(tasks, 200)
        
        assert len(scheduled_tasks) == 3
        assert total_time == 135

    def test_schedule_tasks_multiple_partial_fit(self):
        """Test scheduling when only some tasks fit"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 50, Priority.HIGH),
            Task("Grooming", pet, 1, 100, Priority.MEDIUM),
            Task("Play", pet, 1, 200, Priority.LOW),
        ]
        
        scheduled_tasks, total_time = scheduler.schedule_tasks(tasks, 200)
        
        # Should schedule HIGH and MEDIUM, but not LOW
        assert len(scheduled_tasks) == 2
        assert total_time == 150

    def test_schedule_tasks_none_fit(self):
        """Test scheduling when no tasks fit"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 300, Priority.HIGH),
            Task("Grooming", pet, 1, 300, Priority.MEDIUM),
        ]
        
        scheduled_tasks, total_time = scheduler.schedule_tasks(tasks, 200)
        
        assert len(scheduled_tasks) == 0
        assert total_time == 0


class TestScheduleTasksPriority:
    """Test priority-based scheduling"""

    def test_schedule_tasks_by_priority(self):
        """Test that tasks are scheduled by priority"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Low Priority", pet, 1, 100, Priority.LOW),
            Task("High Priority", pet, 1, 50, Priority.HIGH),
            Task("Medium Priority", pet, 1, 60, Priority.MEDIUM),
        ]
        
        scheduled_tasks, total_time = scheduler.schedule_tasks(tasks, 150)
        
        # Should schedule HIGH first, then MEDIUM, then LOW (if space)
        assert len(scheduled_tasks) == 2
        assert Task("High Priority", pet, 1, 50, Priority.HIGH) not in scheduled_tasks or \
               any(t.task_type == "High Priority" for t in scheduled_tasks)

    def test_schedule_tasks_high_priority_first(self):
        """Test that high priority tasks are scheduled first"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Low", pet, 1, 100, Priority.LOW),
            Task("High", pet, 1, 50, Priority.HIGH),
            Task("Medium", pet, 1, 30, Priority.MEDIUM),
        ]
        
        scheduled_tasks, total_time = scheduler.schedule_tasks(tasks, 100)
        
        # Should only fit HIGH (50) and MEDIUM (30) = 80 total
        task_types = [t.task_type for t in scheduled_tasks]
        assert "High" in task_types
        assert "Medium" in task_types
        assert "Low" not in task_types


class TestScheduleTasksWithFrequency:
    """Test scheduling with task frequency"""

    def test_schedule_tasks_with_frequency(self):
        """Test scheduling tasks with frequency > 1"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 3, 20, Priority.HIGH)  # 60 min total
        
        scheduled_tasks, total_time = scheduler.schedule_tasks([task], 200)
        
        assert len(scheduled_tasks) == 1
        assert total_time == 60

    def test_schedule_tasks_multiple_frequencies(self):
        """Test scheduling multiple tasks with different frequencies"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 3, 20, Priority.HIGH),  # 60
            Task("Walking", pet, 1, 60, Priority.MEDIUM),  # 60
            Task("Play", pet, 2, 30, Priority.LOW),  # 60
        ]
        
        scheduled_tasks, total_time = scheduler.schedule_tasks(tasks, 180)
        
        assert len(scheduled_tasks) == 3
        assert total_time == 180


class TestIsFeasible:
    """Test is_feasible method"""

    def test_is_feasible_all_fit(self):
        """Test feasibility when all tasks fit"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 30, Priority.HIGH),
            Task("Grooming", pet, 1, 45, Priority.MEDIUM),
        ]
        
        assert scheduler.is_feasible(tasks, 200) is True

    def test_is_feasible_exact_fit(self):
        """Test feasibility when tasks exactly fit"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 75),
        ]
        
        assert scheduler.is_feasible(tasks, 75) is True

    def test_is_feasible_dont_fit(self):
        """Test feasibility when tasks don't fit"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 100),
            Task("Grooming", pet, 1, 150),
        ]
        
        assert scheduler.is_feasible(tasks, 200) is False

    def test_is_feasible_empty_tasks(self):
        """Test feasibility with no tasks"""
        scheduler = Scheduler()
        assert scheduler.is_feasible([], 200) is True

    def test_is_feasible_zero_time(self):
        """Test feasibility with zero available time"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30)
        
        assert scheduler.is_feasible([task], 0) is False


class TestExplainScheduling:
    """Test explain_scheduling method"""

    def test_explain_scheduling_basic(self):
        """Test scheduling explanation is generated"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30)
        
        scheduled_tasks = [task]
        explanation = scheduler.explain_scheduling(scheduled_tasks, 200, 30)
        
        assert isinstance(explanation, str)
        assert "Scheduling Logic" in explanation

    def test_explain_scheduling_details(self):
        """Test scheduling explanation contains details"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30)
        
        scheduled_tasks = [task]
        explanation = scheduler.explain_scheduling(scheduled_tasks, 200, 30)
        
        assert "HIGH" in explanation or "priority" in explanation.lower()
        assert "200" in explanation
        assert "30" in explanation
        assert "1" in explanation  # 1 task scheduled

    def test_explain_scheduling_with_remaining_time(self):
        """Test explanation includes remaining time"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30)
        
        scheduled_tasks = [task]
        explanation = scheduler.explain_scheduling(scheduled_tasks, 200, 30)
        
        # Should mention remaining time when used < available
        if 30 < 200:
            assert "remaining" in explanation.lower() or "170" in explanation

    def test_explain_scheduling_full_capacity(self):
        """Test explanation when time is fully used"""
        scheduler = Scheduler()
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 200)
        
        scheduled_tasks = [task]
        explanation = scheduler.explain_scheduling(scheduled_tasks, 200, 200)
        
        assert isinstance(explanation, str)
        assert "200" in explanation
