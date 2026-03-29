"""Tests for Task model"""

import pytest

from src.models.enums import Priority
from src.models.pet import Pet
from src.models.task import Task


def test_task_init_required_fields():
    """Test creating a task with required fields"""
    pet = Pet("Fluffy", "Cat", 3)
    task = Task("Feeding", pet, 2, 30)

    assert task.task_type == "Feeding"
    assert task.pet == pet
    assert task.frequency == 2
    assert task.duration == 30
    assert task.priority == Priority.MEDIUM


def test_task_init_with_priority():
    """Test creating a task with custom priority"""
    pet = Pet("Buddy", "Dog", 5)
    task = Task("Walking", pet, 1, 60, Priority.HIGH)

    assert task.task_type == "Walking"
    assert task.priority == Priority.HIGH
    assert task.preferred_times == []


def test_task_init_all_priorities():
    """Test creating tasks with all priority levels"""
    pet = Pet("Max", "Dog", 4)

    task_high = Task("Medication", pet, 2, 15, Priority.HIGH)
    task_medium = Task("Grooming", pet, 1, 45, Priority.MEDIUM)
    task_low = Task("Play", pet, 1, 30, Priority.LOW)

    assert task_high.priority == Priority.HIGH
    assert task_medium.priority == Priority.MEDIUM
    assert task_low.priority == Priority.LOW


def test_is_urgent_high_priority():
    """Test is_urgent for high priority task"""
    pet = Pet("Luna", "Cat", 2)
    task = Task("Medication", pet, 2, 15, Priority.HIGH)
    assert task.is_urgent() is True


def test_is_urgent_medium_priority():
    """Test is_urgent for medium priority task"""
    pet = Pet("Luna", "Cat", 2)
    task = Task("Grooming", pet, 1, 45, Priority.MEDIUM)
    assert task.is_urgent() is False


def test_is_urgent_low_priority():
    """Test is_urgent for low priority task"""
    pet = Pet("Luna", "Cat", 2)
    task = Task("Play", pet, 1, 30, Priority.LOW)
    assert task.is_urgent() is False


def test_get_task_info():
    """Test getting task information"""
    pet = Pet("Fluffy", "Cat", 3)
    task = Task("Feeding", pet, 2, 30)

    info = task.get_task_info()
    assert "Feeding" in info
    assert "Fluffy" in info
    assert "2" in info
    assert "60" in info


def test_get_task_info_various_tasks():
    """Test getting info for different task types"""
    pet = Pet("Buddy", "Dog", 5)

    feeding_task = Task("Feeding", pet, 2, 30)
    walking_task = Task("Walking", pet, 1, 60)
    grooming_task = Task("Grooming", pet, 1, 45)

    assert "Feeding" in feeding_task.get_task_info()
    assert "Walking" in walking_task.get_task_info()
    assert "Grooming" in grooming_task.get_task_info()


def test_task_total_duration_single():
    """Test calculating total time for single frequency task"""
    pet = Pet("Max", "Dog", 4)
    task = Task("Feeding", pet, 1, 30)

    total_time = task.duration * task.frequency
    assert total_time == 30


def test_task_total_duration_multiple():
    """Test calculating total time for multiple frequency task"""
    pet = Pet("Max", "Dog", 4)
    task = Task("Feeding", pet, 3, 20)

    total_time = task.duration * task.frequency
    assert total_time == 60


def test_task_total_duration_zero():
    """Test task with zero duration"""
    pet = Pet("Max", "Dog", 4)
    task = Task("Check-in", pet, 1, 0)

    total_time = task.duration * task.frequency
    assert total_time == 0


def test_preferred_times_initialization():
    """Test preferred times are initialized as empty"""
    pet = Pet("Fluffy", "Cat", 3)
    task = Task("Feeding", pet, 2, 30)

    assert task.preferred_times == []


def test_preferred_times_can_be_set():
    """Test that preferred times can be added"""
    pet = Pet("Fluffy", "Cat", 3)
    task = Task("Feeding", pet, 2, 30)

    task.preferred_times = ["08:00", "20:00"]
    assert len(task.preferred_times) == 2
    assert "08:00" in task.preferred_times
    assert "20:00" in task.preferred_times
