"""Tests for Owner model"""

import pytest
from src.models.owner import Owner
from src.models.pet import Pet


class TestOwnerInitialization:
    """Test Owner initialization"""

    def test_owner_init_name_only(self):
        """Test creating an owner with name only"""
        owner = Owner("Alice")
        assert owner.name == "Alice"
        assert owner.email == ""
        assert owner.phone == ""
        assert owner.pets == []
        assert owner.preferences == {}

    def test_owner_init_with_contact_info(self):
        """Test creating an owner with all fields"""
        owner = Owner("Bob", email="bob@example.com", phone="555-1234")
        assert owner.name == "Bob"
        assert owner.email == "bob@example.com"
        assert owner.phone == "555-1234"


class TestAddRemovePets:
    """Test pet management"""

    def test_add_single_pet(self):
        """Test adding a single pet"""
        owner = Owner("Alice")
        pet = Pet("Fluffy", "Cat", 3)
        owner.add_pet(pet)
        
        assert len(owner.pets) == 1
        assert owner.pets[0] == pet
        assert pet.owner_name == "Alice"

    def test_add_multiple_pets(self):
        """Test adding multiple pets"""
        owner = Owner("Alice")
        pets = [
            Pet("Fluffy", "Cat", 3),
            Pet("Buddy", "Dog", 5),
            Pet("Charlie", "Rabbit", 2),
        ]
        for pet in pets:
            owner.add_pet(pet)
        
        assert len(owner.pets) == 3
        for pet in pets:
            assert pet in owner.pets
            assert pet.owner_name == "Alice"

    def test_remove_pet(self):
        """Test removing a pet"""
        owner = Owner("Alice")
        pet = Pet("Fluffy", "Cat", 3)
        owner.add_pet(pet)
        owner.remove_pet(pet)
        
        assert len(owner.pets) == 0
        assert pet not in owner.pets

    def test_remove_nonexistent_pet(self):
        """Test removing a pet that doesn't exist"""
        owner = Owner("Alice")
        pet1 = Pet("Fluffy", "Cat", 3)
        pet2 = Pet("Buddy", "Dog", 5)
        
        owner.add_pet(pet1)
        owner.remove_pet(pet2)  # Should not raise error
        
        assert len(owner.pets) == 1
        assert pet1 in owner.pets

    def test_remove_pet_from_empty_list(self):
        """Test removing a pet from empty pet list"""
        owner = Owner("Alice")
        pet = Pet("Fluffy", "Cat", 3)
        owner.remove_pet(pet)  # Should not raise error
        assert len(owner.pets) == 0


class TestPreferences:
    """Test preference management"""

    def test_set_single_preference(self):
        """Test setting a single preference"""
        owner = Owner("Alice")
        owner.set_preference("daily_time", 200)
        assert owner.preferences["daily_time"] == 200

    def test_set_multiple_preferences(self):
        """Test setting multiple preferences"""
        owner = Owner("Alice")
        owner.set_preference("daily_time", 200)
        owner.set_preference("wake_time", "08:00")
        owner.set_preference("bedtime", "22:00")
        
        assert len(owner.preferences) == 3
        assert owner.preferences["daily_time"] == 200
        assert owner.preferences["wake_time"] == "08:00"
        assert owner.preferences["bedtime"] == "22:00"

    def test_update_preference(self):
        """Test updating an existing preference"""
        owner = Owner("Alice")
        owner.set_preference("daily_time", 200)
        owner.set_preference("daily_time", 300)
        
        assert owner.preferences["daily_time"] == 300

    def test_preference_types(self):
        """Test preferences with different types"""
        owner = Owner("Alice")
        owner.set_preference("time_minutes", 200)
        owner.set_preference("is_available", True)
        owner.set_preference("schedule_type", "flexible")
        owner.set_preference("priority_weights", [0.3, 0.5, 0.2])
        
        assert isinstance(owner.preferences["time_minutes"], int)
        assert isinstance(owner.preferences["is_available"], bool)
        assert isinstance(owner.preferences["schedule_type"], str)
        assert isinstance(owner.preferences["priority_weights"], list)


class TestOwnerInfo:
    """Test owner information methods"""

    def test_get_info_name_only(self):
        """Test getting info for owner with name only"""
        owner = Owner("Alice")
        info = owner.get_info()
        assert "Owner: Alice" in info
        assert "Pets: 0" in info

    def test_get_info_with_contact(self):
        """Test getting info with email and phone"""
        owner = Owner("Alice", email="alice@example.com", phone="555-1234")
        info = owner.get_info()
        assert "Owner: Alice" in info
        assert "Email: alice@example.com" in info
        assert "Phone: 555-1234" in info

    def test_get_info_with_pets(self):
        """Test getting info with pets"""
        owner = Owner("Alice")
        pet1 = Pet("Fluffy", "Cat", 3)
        pet2 = Pet("Buddy", "Dog", 5)
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        info = owner.get_info()
        assert "Pets: 2" in info
        assert "Fluffy" in info
        assert "Buddy" in info

    def test_get_info_complete(self):
        """Test getting complete info"""
        owner = Owner("Alice", email="alice@example.com", phone="555-1234")
        pet = Pet("Fluffy", "Cat", 3)
        owner.add_pet(pet)
        
        info = owner.get_info()
        assert "Owner: Alice" in info
        assert "Email: alice@example.com" in info
        assert "Phone: 555-1234" in info
        assert "Pets: 1" in info
