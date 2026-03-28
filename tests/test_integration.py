"""Integration tests for PawPal with realistic owner scenarios"""

import pytest
from datetime import date
from src.models.owner import Owner
from src.models.pet import Pet
from src.models.task import Task
from src.models.schedule import Schedule
from src.models.enums import Priority
from src.core.scheduler import Scheduler


# Fixtures for creating owner scenarios
@pytest.fixture
def busy_owner():
    """Create a busy professional owner with limited time"""
    owner = Owner("Sarah", email="sarah@work.com", phone="555-0101")
    owner.set_preference("daily_time", 120)
    owner.set_preference("schedule_type", "strict")
    
    dog = Pet("Max", "Dog", 7, breed="Labrador", weight=35.0)
    dog.add_special_need("hip dysplasia")
    dog.add_medication("Joint supplements")
    
    cat = Pet("Whiskers", "Cat", 4, breed="Persian", weight=5.5)
    cat.add_allergy("fish")
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    return owner


@pytest.fixture
def moderate_owner():
    """Create a moderate-schedule owner"""
    owner = Owner("James", email="james@home.com", phone="555-0202")
    owner.set_preference("daily_time", 200)
    owner.set_preference("schedule_type", "balanced")
    
    dog = Pet("Buddy", "Dog", 5, breed="Golden Retriever", weight=30.0)
    dog.add_medication("Allergy medication")
    
    rabbit = Pet("Hoppy", "Rabbit", 3)
    rabbit.add_special_need("requires daily exercise")
    
    bird = Pet("Tweety", "Parrot", 8)
    
    owner.add_pet(dog)
    owner.add_pet(rabbit)
    owner.add_pet(bird)
    
    return owner


@pytest.fixture
def flexible_owner():
    """Create a flexible-schedule owner with ample time"""
    owner = Owner("Margaret", email="margaret@retired.com", phone="555-0303")
    owner.set_preference("daily_time", 350)
    owner.set_preference("schedule_type", "flexible")
    
    dogs = [
        Pet("Buddy", "Dog", 2, breed="Mixed"),
        Pet("Scout", "Dog", 8, breed="Beagle"),
        Pet("Luna", "Dog", 3, breed="Husky"),
    ]
    
    dogs[1].add_special_need("senior dog - requires frequent breaks")
    dogs[1].add_medication("Heart medication")
    dogs[1].add_medication("Arthritis medication")
    
    dogs[2].add_special_need("high energy - needs lots of exercise")
    
    cats = [
        Pet("Mittens", "Cat", 5),
        Pet("Shadow", "Cat", 10),
        Pet("Patches", "Cat", 2),
    ]
    
    cats[1].add_medication("Kidney medication")
    
    for dog in dogs:
        owner.add_pet(dog)
    for cat in cats:
        owner.add_pet(cat)
    
    return owner


# Busy Owner Tests
def test_busy_owner_profile_setup(busy_owner):
    """Test busy owner profile is correctly set up"""
    assert busy_owner.name == "Sarah"
    assert busy_owner.preferences["daily_time"] == 120
    assert busy_owner.preferences["schedule_type"] == "strict"
    assert len(busy_owner.pets) == 2


def test_busy_owner_pets_info(busy_owner):
    """Test all pets have correct information"""
    dog = busy_owner.pets[0]
    cat = busy_owner.pets[1]
    
    assert dog.name == "Max"
    assert dog.age == 7
    assert "hip dysplasia" in dog.special_needs
    assert "Joint supplements" in dog.medications
    
    assert cat.name == "Whiskers"
    assert "fish" in cat.allergies


def test_busy_owner_critical_tasks_fit(busy_owner):
    """Test that critical/essential tasks fit in busy owner's schedule"""
    dog = busy_owner.pets[0]
    cat = busy_owner.pets[1]
    
    essential_tasks = [
        Task("Medication", dog, 1, 10, Priority.HIGH),
        Task("Feeding", dog, 2, 15, Priority.HIGH),
        Task("Feeding", cat, 2, 15, Priority.HIGH),
        Task("Medication check", cat, 1, 5, Priority.MEDIUM),
    ]
    
    scheduler = Scheduler()
    available_time = busy_owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(essential_tasks, available_time)
    
    assert total_time == 75
    assert len(scheduled) == 4
    assert scheduler.is_feasible(essential_tasks, available_time) is True


def test_busy_owner_full_schedule(busy_owner):
    """Test creating a realistic full day schedule for busy owner"""
    dog = busy_owner.pets[0]
    cat = busy_owner.pets[1]
    
    all_tasks = [
        Task("Morning walk", dog, 1, 25, Priority.HIGH),
        Task("Feeding", dog, 2, 15, Priority.HIGH),
        Task("Medication", dog, 1, 10, Priority.HIGH),
        Task("Evening walk", dog, 1, 20, Priority.MEDIUM),
        Task("Playtime", dog, 1, 15, Priority.LOW),
        Task("Feeding", cat, 2, 10, Priority.HIGH),
        Task("Litter box", cat, 2, 5, Priority.HIGH),
        Task("Grooming", cat, 1, 15, Priority.MEDIUM),
        Task("Play session", cat, 1, 10, Priority.LOW),
    ]
    
    scheduler = Scheduler()
    available_time = busy_owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(all_tasks, available_time)
    
    schedule = Schedule(date.today(), available_time, scheduled)
    
    assert schedule.is_feasible() is True
    assert schedule.total_time_used <= available_time
    plan = schedule.get_daily_plan()
    
    assert "Daily Plan" in plan
    assert str(date.today()) in plan
    assert "120" in plan


def test_busy_owner_tradeoffs(busy_owner):
    """Test which tasks get prioritized when not everything fits"""
    dog = busy_owner.pets[0]
    cat = busy_owner.pets[1]
    
    all_tasks = [
        Task("Walk", dog, 1, 30, Priority.HIGH),
        Task("Feeding", dog, 2, 15, Priority.HIGH),
        Task("Medication", dog, 1, 10, Priority.HIGH),
        Task("Grooming", dog, 1, 60, Priority.LOW),
        Task("Feeding", cat, 2, 10, Priority.HIGH),
        Task("Litter", cat, 2, 5, Priority.HIGH),
        Task("Grooming", cat, 1, 45, Priority.LOW),
        Task("Play", cat, 1, 30, Priority.LOW),
    ]
    
    scheduler = Scheduler()
    available_time = busy_owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(all_tasks, available_time)
    
    high_priority_tasks = [t for t in scheduled if t.priority == Priority.HIGH]
    assert len(high_priority_tasks) > 0
    assert total_time <= available_time


# Moderate Owner Tests
def test_moderate_owner_profile_setup(moderate_owner):
    """Test moderate owner profile"""
    assert moderate_owner.name == "James"
    assert moderate_owner.preferences["daily_time"] == 200
    assert len(moderate_owner.pets) == 3


def test_moderate_owner_balanced_schedule(moderate_owner):
    """Test balanced scheduling for moderate owner"""
    dog, rabbit, bird = moderate_owner.pets
    
    tasks = [
        Task("Morning walk", dog, 1, 20, Priority.HIGH),
        Task("Feeding", dog, 2, 15, Priority.HIGH),
        Task("Medication", dog, 1, 5, Priority.HIGH),
        Task("Evening walk", dog, 1, 20, Priority.MEDIUM),
        Task("Playtime", dog, 1, 30, Priority.MEDIUM),
        Task("Feeding", rabbit, 2, 10, Priority.HIGH),
        Task("Exercise", rabbit, 1, 30, Priority.HIGH),
        Task("Cleaning", rabbit, 1, 20, Priority.MEDIUM),
        Task("Feeding", bird, 1, 10, Priority.HIGH),
        Task("Interaction", bird, 1, 20, Priority.MEDIUM),
        Task("Cage cleaning", bird, 1, 30, Priority.MEDIUM),
        Task("Supplies", None, 1, 15, Priority.LOW),
    ]
    
    scheduler = Scheduler()
    available_time = moderate_owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(tasks, available_time)
    
    assert len(scheduled) >= 8
    assert total_time <= available_time
    
    schedule = Schedule(date.today(), available_time, scheduled)
    assert schedule.is_feasible() is True


def test_moderate_owner_variety_of_tasks(moderate_owner):
    """Test variety of pet care tasks for moderate owner"""
    dog, rabbit, bird = moderate_owner.pets
    
    feeding_tasks = [
        Task("Feeding", dog, 2, 15, Priority.HIGH),
        Task("Feeding", rabbit, 2, 10, Priority.HIGH),
        Task("Feeding", bird, 1, 10, Priority.HIGH),
    ]
    
    exercise_tasks = [
        Task("Walk", dog, 1, 30, Priority.HIGH),
        Task("Exercise", rabbit, 1, 30, Priority.HIGH),
    ]
    
    grooming_tasks = [
        Task("Grooming", dog, 1, 45, Priority.MEDIUM),
        Task("Cleaning", rabbit, 1, 20, Priority.MEDIUM),
    ]
    
    enrichment_tasks = [
        Task("Playtime", dog, 1, 20, Priority.LOW),
        Task("Interaction", bird, 1, 20, Priority.LOW),
    ]
    
    all_tasks = feeding_tasks + exercise_tasks + grooming_tasks + enrichment_tasks
    
    scheduler = Scheduler()
    available_time = moderate_owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(all_tasks, available_time)
    
    scheduled_feeding = [t for t in scheduled if "Feeding" in t.task_type]
    assert len(scheduled_feeding) == 3
    
    priorities_scheduled = [t.priority for t in scheduled]
    assert Priority.HIGH in priorities_scheduled


# Flexible Owner Tests
def test_flexible_owner_profile_setup(flexible_owner):
    """Test flexible owner setup with many pets"""
    assert flexible_owner.name == "Margaret"
    assert flexible_owner.preferences["daily_time"] == 350
    assert len(flexible_owner.pets) == 6


def test_flexible_owner_comprehensive_care(flexible_owner):
    """Test comprehensive care schedule for flexible owner with many pets"""
    available_time = flexible_owner.preferences["daily_time"]
    
    all_tasks = []
    
    for dog in flexible_owner.pets[:3]:
        if dog.age >= 8:
            all_tasks.extend([
                Task(f"Morning walk - {dog.name}", dog, 1, 20, Priority.HIGH),
                Task(f"Medication - {dog.name}", dog, 2, 10, Priority.HIGH),
                Task(f"Feeding - {dog.name}", dog, 2, 20, Priority.HIGH),
                Task(f"Afternoon rest break - {dog.name}", dog, 1, 15, Priority.HIGH),
                Task(f"Evening walk - {dog.name}", dog, 1, 15, Priority.MEDIUM),
            ])
        else:
            all_tasks.extend([
                Task(f"Morning walk - {dog.name}", dog, 1, 30, Priority.HIGH),
                Task(f"Feeding - {dog.name}", dog, 2, 15, Priority.HIGH),
                Task(f"Playtime - {dog.name}", dog, 1, 40, Priority.MEDIUM),
                Task(f"Evening walk - {dog.name}", dog, 1, 30, Priority.MEDIUM),
            ])
    
    for cat in flexible_owner.pets[3:]:
        cat_tasks = [
            Task(f"Feeding - {cat.name}", cat, 2, 10, Priority.HIGH),
            Task(f"Litter box - {cat.name}", cat, 2, 5, Priority.HIGH),
            Task(f"Interactive play - {cat.name}", cat, 1, 20, Priority.MEDIUM),
        ]
        
        if cat.age >= 10:
            cat_tasks.append(
                Task(f"Medication - {cat.name}", cat, 1, 5, Priority.HIGH)
            )
        
        all_tasks.extend(cat_tasks)
    
    scheduler = Scheduler()
    scheduled, total_time = scheduler.schedule_tasks(all_tasks, available_time)
    
    assert len(scheduled) > 10
    assert total_time <= available_time
    
    schedule = Schedule(date.today(), available_time, scheduled)
    assert schedule.is_feasible() is True
    
    plan = schedule.get_daily_plan()
    assert "Daily Plan" in plan
    assert str(date.today()) in plan


def test_flexible_owner_senior_pet_priority(flexible_owner):
    """Test that senior pets with medications get priority"""
    available_time = flexible_owner.preferences["daily_time"]
    
    senior_dog = flexible_owner.pets[1]
    senior_cat = flexible_owner.pets[4]
    
    tasks = [
        Task("Heart medication", senior_dog, 2, 10, Priority.HIGH),
        Task("Arthritis medication", senior_dog, 2, 10, Priority.HIGH),
        Task("Kidney medication", senior_cat, 1, 5, Priority.HIGH),
        Task("Senior dog walk", senior_dog, 1, 20, Priority.HIGH),
        Task("Senior cat food", senior_cat, 2, 10, Priority.HIGH),
        Task("Regular tasks for other pets", None, 1, 100, Priority.MEDIUM),
    ]
    
    scheduler = Scheduler()
    scheduled, total_time = scheduler.schedule_tasks(tasks, available_time)
    
    high_priority = [t for t in scheduled if t.priority == Priority.HIGH]
    assert len(high_priority) >= 4


def test_flexible_owner_time_optimization(flexible_owner):
    """Test that flexible owner can optimize time usage"""
    available_time = flexible_owner.preferences["daily_time"]
    
    ideal_tasks = [
        Task("Dog walks", None, 3, 25, Priority.HIGH),
        Task("Dog feeding", None, 6, 15, Priority.HIGH),
        Task("Dog medications", None, 2, 10, Priority.HIGH),
        Task("Cat feeding", None, 6, 10, Priority.HIGH),
        Task("Cat litter", None, 2, 5, Priority.HIGH),
        Task("Cat medications", None, 1, 5, Priority.HIGH),
        Task("Dog grooming", None, 1, 60, Priority.MEDIUM),
        Task("Cat grooming", None, 1, 30, Priority.MEDIUM),
        Task("Training", None, 1, 45, Priority.MEDIUM),
        Task("Play/enrichment", None, 2, 30, Priority.LOW),
        Task("Cleaning supplies", None, 1, 30, Priority.LOW),
    ]
    
    scheduler = Scheduler()
    scheduled, total_time = scheduler.schedule_tasks(ideal_tasks, available_time)
    
    assert total_time <= available_time
    remaining_time = available_time - total_time
    assert remaining_time >= 0


# Cross-Owner Comparison Tests
def test_same_tasks_different_feasibility():
    """Test how same tasks fit for different owners"""
    dog = Pet("TestDog", "Dog", 4)
    
    critical_tasks = [
        Task("Feeding", dog, 2, 30, Priority.HIGH),
        Task("Walk", dog, 1, 45, Priority.HIGH),
        Task("Play", dog, 1, 30, Priority.MEDIUM),
        Task("Grooming", dog, 1, 60, Priority.LOW),
    ]
    
    scheduler = Scheduler()
    
    busy_time = 120
    moderate_time = 200
    flexible_time = 350
    
    busy_scheduled, _ = scheduler.schedule_tasks(critical_tasks, busy_time)
    moderate_scheduled, _ = scheduler.schedule_tasks(critical_tasks, moderate_time)
    flexible_scheduled, _ = scheduler.schedule_tasks(critical_tasks, flexible_time)
    
    assert len(busy_scheduled) < len(moderate_scheduled)
    assert len(moderate_scheduled) < len(flexible_scheduled)
    
    assert not scheduler.is_feasible(critical_tasks, busy_time)
    assert scheduler.is_feasible(critical_tasks, moderate_time)
    assert scheduler.is_feasible(critical_tasks, flexible_time)


def test_priority_strategy_effectiveness():
    """Test that priority-based scheduling works across owner types"""
    pet = Pet("Priority Test", "Dog", 3)
    
    tasks = [
        Task("Life-saving medication", pet, 2, 10, Priority.HIGH),
        Task("Essential walk", pet, 1, 20, Priority.HIGH),
        Task("Regular grooming", pet, 1, 60, Priority.MEDIUM),
        Task("Nice-to-have enrichment", pet, 2, 30, Priority.LOW),
    ]
    
    scheduler = Scheduler()
    limited_time = 35
    scheduled, total = scheduler.schedule_tasks(tasks, limited_time)
    
    scheduled_types = [t.task_type for t in scheduled]
    
    assert "Life-saving medication" in scheduled_types
    assert "Essential walk" in scheduled_types
    assert "Nice-to-have enrichment" not in scheduled_types

