"""Tests for Schedule model"""

import pytest
from datetime import date
from src.models.schedule import Schedule
from src.models.task import Task
from src.models.pet import Pet
from src.models.enums import Priority


class TestScheduleInitialization:
    """Test Schedule initialization"""

    def test_schedule_init_no_tasks(self):
        """Test creating a schedule without tasks"""
        today = date.today()
        schedule = Schedule(today, 200)
        
        assert schedule.date == today
        assert schedule.available_time == 200
        assert schedule.scheduled_tasks == []
        assert schedule.total_time_used == 0

    def test_schedule_init_with_tasks(self):
        """Test creating a schedule with tasks"""
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 30, Priority.HIGH),
            Task("Grooming", pet, 1, 45, Priority.LOW),
        ]
        today = date.today()
        
        schedule = Schedule(today, 200, tasks)
        
        assert schedule.date == today
        assert schedule.available_time == 200
        assert len(schedule.scheduled_tasks) == 2
        assert schedule.total_time_used == 75  # 30 + 45

    def test_schedule_init_with_empty_tasks_list(self):
        """Test creating a schedule with empty task list"""
        today = date.today()
        schedule = Schedule(today, 200, [])
        
        assert schedule.scheduled_tasks == []
        assert schedule.total_time_used == 0


class TestScheduleFeasibility:
    """Test schedule feasibility checks"""

    def test_is_feasible_within_time(self):
        """Test schedule that fits within available time"""
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 30),
            Task("Grooming", pet, 1, 45),
        ]
        today = date.today()
        
        schedule = Schedule(today, 200, tasks)
        assert schedule.is_feasible() is True

    def test_is_feasible_exact_time(self):
        """Test schedule that exactly matches available time"""
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 100),
        ]
        today = date.today()
        
        schedule = Schedule(today, 100, tasks)
        assert schedule.is_feasible() is True

    def test_is_feasible_exceeds_time(self):
        """Test schedule that exceeds available time"""
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 2, 100),  # 200 minutes
        ]
        today = date.today()
        
        schedule = Schedule(today, 150, tasks)
        assert schedule.is_feasible() is False

    def test_is_feasible_no_tasks(self):
        """Test schedule with no tasks"""
        today = date.today()
        schedule = Schedule(today, 200)
        assert schedule.is_feasible() is True


class TestScheduleTime:
    """Test time calculations"""

    def test_total_time_used_single_task(self):
        """Test total time with single task"""
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30)
        today = date.today()
        
        schedule = Schedule(today, 200, [task])
        assert schedule.total_time_used == 30

    def test_total_time_used_multiple_tasks(self):
        """Test total time with multiple tasks"""
        pet = Pet("Fluffy", "Cat", 3)
        tasks = [
            Task("Feeding", pet, 1, 30),
            Task("Walking", pet, 1, 60),
            Task("Grooming", pet, 1, 45),
        ]
        today = date.today()
        
        schedule = Schedule(today, 200, tasks)
        assert schedule.total_time_used == 135

    def test_remaining_time(self):
        """Test remaining time calculation"""
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30)
        today = date.today()
        
        schedule = Schedule(today, 200, [task])
        remaining = schedule.available_time - schedule.total_time_used
        assert remaining == 170

    def test_total_time_with_frequency(self):
        """Test total time accounts for frequency"""
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 3, 20)  # 3x per day, 20 mins each
        today = date.today()
        
        schedule = Schedule(today, 200, [task])
        assert schedule.total_time_used == 60


class TestScheduleDailyPlan:
    """Test daily plan output"""

    def test_get_daily_plan_no_tasks(self):
        """Test daily plan with no tasks"""
        today = date.today()
        schedule = Schedule(today, 200)
        
        plan = schedule.get_daily_plan()
        assert str(today) in plan
        assert "Available time: 200" in plan
        assert "Used time: 0" in plan
        assert "No tasks scheduled" in plan

    def test_get_daily_plan_with_tasks(self):
        """Test daily plan with tasks"""
        pet = Pet("Fluffy", "Cat", 3)
        task = Task("Feeding", pet, 1, 30)
        today = date.today()
        
        schedule = Schedule(today, 200, [task])
        plan = schedule.get_daily_plan()
        
        assert str(today) in plan
        assert "Available time: 200" in plan
        assert "Used time: 30" in plan
        assert "Remaining time: 170" in plan
        assert "Scheduled Tasks:" in plan
        assert "Feeding" in plan

    def test_get_daily_plan_multiple_tasks(self):
        """Test daily plan with multiple tasks"""
        pet1 = Pet("Fluffy", "Cat", 3)
        pet2 = Pet("Buddy", "Dog", 5)
        tasks = [
            Task("Feeding", pet1, 1, 30),
            Task("Walking", pet2, 1, 60),
        ]
        today = date.today()
        
        schedule = Schedule(today, 200, tasks)
        plan = schedule.get_daily_plan()
        
        assert "Feeding" in plan
        assert "Walking" in plan
        assert "90" in plan  # total time

    def test_get_daily_plan_format(self):
        """Test daily plan has proper format"""
        today = date.today()
        schedule = Schedule(today, 200)
        plan = schedule.get_daily_plan()
        
        assert "Daily Plan" in plan
        assert "Available time:" in plan
        assert "Used time:" in plan
        assert "Remaining time:" in plan


class TestScheduleDates:
    """Test schedule date handling"""

    def test_schedule_with_specific_date(self):
        """Test schedule can be created with specific date"""
        specific_date = date(2026, 3, 28)
        schedule = Schedule(specific_date, 200)
        
        assert schedule.date == specific_date

    def test_schedule_date_preservation(self):
        """Test that schedule date is preserved"""
        date1 = date(2026, 1, 1)
        date2 = date(2026, 12, 31)
        
        schedule1 = Schedule(date1, 200)
        schedule2 = Schedule(date2, 200)
        
        assert schedule1.date == date1
        assert schedule2.date == date2
        assert schedule1.date != schedule2.date
