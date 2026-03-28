"""Owner model class"""

from typing import List

from .pet import Pet


class Owner:
    """Represents a pet owner."""

    def __init__(self, name: str, email: str = "", phone: str = ""):
        """
        Initialize an Owner.

        Args:
            name: Owner's name
            email: Owner's email (optional)
            phone: Owner's phone number (optional)
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: List[Pet] = []
        self.preferences = {}

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        pet.owner_name = self.name
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)

    def set_preference(self, key: str, value) -> None:
        """Set a preference for the owner."""
        self.preferences[key] = value

    def get_info(self) -> str:
        """Get owner information as a string."""
        info = f"Owner: {self.name}\n"
        if self.email:
            info += f"Email: {self.email}\n"
        if self.phone:
            info += f"Phone: {self.phone}\n"
        info += f"Pets: {len(self.pets)}\n"
        for pet in self.pets:
            info += f"  - {pet.get_info()}\n"
        return info
