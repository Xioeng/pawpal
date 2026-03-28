"""Pet model class"""

from typing import List


class Pet:
    """Represents a pet with basic information and special needs."""

    def __init__(
        self,
        name: str,
        species: str,
        age: int,
        breed: str = "",
        weight: float = 0.0,
    ):
        """
        Initialize a Pet.

        Args:
            name: Pet's name
            species: Type of pet (e.g., 'dog', 'cat', 'rabbit')
            age: Pet's age in years
            breed: Pet's breed (optional)
            weight: Pet's weight in kg (optional)
        """
        self.name = name
        self.species = species
        self.age = age
        self.breed = breed
        self.weight = weight
        self.owner_name: str = ""
        self.special_needs: List[str] = []
        self.medications: List[str] = []
        self.allergies: List[str] = []

    def add_special_need(self, need: str) -> None:
        """
        Add a special need for the pet.

        Args:
            need: Description of special need (e.g., 'arthritis', 'anxiety')
        """
        if need not in self.special_needs:
            self.special_needs.append(need)

    def remove_special_need(self, need: str) -> None:
        """Remove a special need."""
        if need in self.special_needs:
            self.special_needs.remove(need)

    def add_medication(self, medication: str) -> None:
        """Add a medication the pet takes."""
        if medication not in self.medications:
            self.medications.append(medication)

    def add_allergy(self, allergy: str) -> None:
        """Add an allergy the pet has."""
        if allergy not in self.allergies:
            self.allergies.append(allergy)

    def get_info(self) -> str:
        """
        Get a summary of pet information.

        Returns:
            String with pet details
        """
        info = f"{self.name} ({self.species}"
        if self.breed:
            info += f", {self.breed}"
        info += f", {self.age} years old)"

        if self.weight > 0:
            info += f"\nWeight: {self.weight} kg"

        if self.special_needs:
            info += f"\nSpecial needs: {', '.join(self.special_needs)}"

        if self.medications:
            info += f"\nMedications: {', '.join(self.medications)}"

        if self.allergies:
            info += f"\nAllergies: {', '.join(self.allergies)}"

        return info

    def __str__(self) -> str:
        """String representation of pet."""
        return self.name

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Pet(name='{self.name}', species='{self.species}', age={self.age})"
