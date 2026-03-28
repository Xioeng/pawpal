"""Tests for Enums"""

import pytest
from src.models.enums import Priority


class TestPriorityEnum:
    """Test Priority enum"""

    def test_priority_values(self):
        """Test priority enum values"""
        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"

    def test_priority_comparison_high_less_than_medium(self):
        """Test that HIGH < MEDIUM"""
        assert Priority.HIGH < Priority.MEDIUM

    def test_priority_comparison_medium_less_than_low(self):
        """Test that MEDIUM < LOW"""
        assert Priority.MEDIUM < Priority.LOW

    def test_priority_comparison_high_less_than_low(self):
        """Test that HIGH < LOW"""
        assert Priority.HIGH < Priority.LOW

    def test_priority_comparison_not_greater_than(self):
        """Test that comparison is consistent"""
        assert not (Priority.MEDIUM < Priority.HIGH)
        assert not (Priority.LOW < Priority.MEDIUM)
        assert not (Priority.LOW < Priority.HIGH)

    def test_priority_sorting(self):
        """Test sorting priorities"""
        priorities = [Priority.LOW, Priority.HIGH, Priority.MEDIUM]
        sorted_priorities = sorted(priorities)
        
        assert sorted_priorities[0] == Priority.HIGH
        assert sorted_priorities[1] == Priority.MEDIUM
        assert sorted_priorities[2] == Priority.LOW

    def test_priority_comparison_with_self(self):
        """Test self comparisons"""
        # High is not less than itself
        assert not (Priority.HIGH < Priority.HIGH)
        assert not (Priority.MEDIUM < Priority.MEDIUM)
        assert not (Priority.LOW < Priority.LOW)

    def test_priority_enum_membership(self):
        """Test enum membership"""
        assert Priority.HIGH in Priority
        assert Priority.MEDIUM in Priority
        assert Priority.LOW in Priority

    def test_priority_enum_all_members(self):
        """Test all enum members"""
        members = list(Priority)
        assert len(members) == 3
        assert Priority.HIGH in members
        assert Priority.MEDIUM in members
        assert Priority.LOW in members
