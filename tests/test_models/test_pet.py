"""Tests for Pet model"""

import pytest
from src.models.pet import Pet


def test_pet_init_required_fields():
    """Test creating a pet with required fields only"""
    pet = Pet("Fluffy", "Cat", 3)
    assert pet.name == "Fluffy"
    assert pet.species == "Cat"
    assert pet.age == 3
    assert pet.breed == ""
    assert pet.weight == 0.0


def test_pet_init_with_optional_fields():
    """Test creating a pet with all fields"""
    pet = Pet("Buddy", "Dog", 5, breed="Golden Retriever", weight=30.5)
    assert pet.name == "Buddy"
    assert pet.species == "Dog"
    assert pet.age == 5
    assert pet.breed == "Golden Retriever"
    assert pet.weight == 30.5


def test_pet_init_empty_lists():
    """Test that lists are initialized as empty"""
    pet = Pet("Charlie", "Rabbit", 2)
    assert pet.special_needs == []
    assert pet.medications == []
    assert pet.allergies == []
    assert pet.owner_name == ""


def test_add_special_need():
    """Test adding a special need"""
    pet = Pet("Max", "Dog", 7)
    pet.add_special_need("arthritis")
    assert "arthritis" in pet.special_needs
    assert len(pet.special_needs) == 1


def test_add_multiple_special_needs():
    """Test adding multiple special needs"""
    pet = Pet("Max", "Dog", 7)
    pet.add_special_need("arthritis")
    pet.add_special_need("anxiety")
    assert len(pet.special_needs) == 2
    assert "arthritis" in pet.special_needs
    assert "anxiety" in pet.special_needs


def test_add_duplicate_special_need():
    """Test that duplicate special needs are not added"""
    pet = Pet("Max", "Dog", 7)
    pet.add_special_need("arthritis")
    pet.add_special_need("arthritis")
    assert len(pet.special_needs) == 1


def test_remove_special_need():
    """Test removing a special need"""
    pet = Pet("Max", "Dog", 7)
    pet.add_special_need("arthritis")
    pet.remove_special_need("arthritis")
    assert "arthritis" not in pet.special_needs


def test_remove_nonexistent_special_need():
    """Test removing a special need that doesn't exist"""
    pet = Pet("Max", "Dog", 7)
    pet.remove_special_need("arthritis")  # Should not raise error
    assert len(pet.special_needs) == 0


def test_add_medication():
    """Test adding a medication"""
    pet = Pet("Luna", "Cat", 4)
    pet.add_medication("Insulin")
    assert "Insulin" in pet.medications


def test_add_multiple_medications():
    """Test adding multiple medications"""
    pet = Pet("Luna", "Cat", 4)
    pet.add_medication("Insulin")
    pet.add_medication("Thyroid medication")
    assert len(pet.medications) == 2


def test_add_duplicate_medication():
    """Test that duplicate medications are not added"""
    pet = Pet("Luna", "Cat", 4)
    pet.add_medication("Insulin")
    pet.add_medication("Insulin")
    assert len(pet.medications) == 1


def test_add_allergy():
    """Test adding an allergy"""
    pet = Pet("Bailey", "Dog", 3)
    pet.add_allergy("chicken")
    assert "chicken" in pet.allergies


def test_add_multiple_allergies():
    """Test adding multiple allergies"""
    pet = Pet("Bailey", "Dog", 3)
    pet.add_allergy("chicken")
    pet.add_allergy("wheat")
    assert len(pet.allergies) == 2


def test_add_duplicate_allergy():
    """Test that duplicate allergies are not added"""
    pet = Pet("Bailey", "Dog", 3)
    pet.add_allergy("chicken")
    pet.add_allergy("chicken")
    assert len(pet.allergies) == 1


def test_get_info_basic():
    """Test getting info for a basic pet"""
    pet = Pet("Fluffy", "Cat", 3)
    info = pet.get_info()
    assert "Fluffy (Cat, 3 years old)" in info


def test_get_info_with_breed():
    """Test getting info for a pet with breed"""
    pet = Pet("Buddy", "Dog", 5, breed="Golden Retriever")
    info = pet.get_info()
    assert "Buddy (Dog, Golden Retriever, 5 years old)" in info


def test_get_info_with_weight():
    """Test getting info for a pet with weight"""
    pet = Pet("Buddy", "Dog", 5, weight=30.5)
    info = pet.get_info()
    assert "Weight: 30.5 kg" in info


def test_get_info_with_special_needs():
    """Test getting info for a pet with special needs"""
    pet = Pet("Max", "Dog", 7)
    pet.add_special_need("arthritis")
    info = pet.get_info()
    assert "Special needs: arthritis" in info


def test_get_info_with_medications():
    """Test getting info for a pet with medications"""
    pet = Pet("Luna", "Cat", 4)
    pet.add_medication("Insulin")
    info = pet.get_info()
    assert "Medications: Insulin" in info


def test_get_info_with_allergies():
    """Test getting info for a pet with allergies"""
    pet = Pet("Bailey", "Dog", 3)
    pet.add_allergy("chicken")
    info = pet.get_info()
    assert "Allergies: chicken" in info


def test_str_representation():
    """Test string representation"""
    pet = Pet("Fluffy", "Cat", 3)
    assert str(pet) == "Fluffy"


def test_repr_representation():
    """Test repr representation"""
    pet = Pet("Buddy", "Dog", 5)
    repr_str = repr(pet)
    assert "Pet" in repr_str
    assert "Buddy" in repr_str
    assert "Dog" in repr_str
    assert "5" in repr_str
