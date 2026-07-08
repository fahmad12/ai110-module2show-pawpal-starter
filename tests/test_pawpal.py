"""Basic tests for PawPal+ core classes."""

import os
import sys
from datetime import date, timedelta

# Make the project root importable so `pawpal_system` is found from tests/.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pawpal_system import Pet, Scheduler, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip the task to completed."""
    task = Task("Morning walk", 30, "high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task count by one."""
    pet = Pet("Biscuit", "dog")
    assert len(pet.list_tasks()) == 0

    pet.add_task(Task("Feeding", 10, "high"))

    assert len(pet.list_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should return tasks ordered by their HH:MM start time."""
    # Build tasks out of order on purpose so the sort has real work to do.
    afternoon = Task("Afternoon walk", 30, "medium", time="14:00")
    morning = Task("Morning feed", 10, "high", time="08:00")
    midday = Task("Midday meds", 5, "low", time="12:30")
    scheduler = Scheduler([afternoon, morning, midday], available_minutes=120)

    ordered = scheduler.sort_by_time()

    # Compare the resulting order by time string — should be earliest first.
    assert [t.time for t in ordered] == ["08:00", "12:30", "14:00"]


def test_mark_daily_task_complete_creates_next_day_occurrence():
    """Completing a daily task should auto-add a fresh copy due the next day."""
    pet = Pet("Rex", "dog")
    today = date(2026, 7, 7)
    walk = Task("Walk Rex", 20, "high", frequency="daily", due_date=today)
    pet.add_task(walk)

    follow_up = pet.mark_task_complete(walk)

    # The original is now complete, and exactly one follow-up was added.
    assert walk.completed is True
    assert len(pet.list_tasks()) == 2
    # The follow-up is a fresh, uncompleted task due one day later.
    assert follow_up is not None
    assert follow_up.completed is False
    assert follow_up.due_date == today + timedelta(days=1)


def test_detect_conflicts_flags_tasks_at_same_time():
    """detect_conflicts() should warn when two tasks share a start time."""
    clash_a = Task("Feed cat", 10, "high", time="09:00")
    clash_b = Task("Walk dog", 30, "medium", time="09:00")
    clear = Task("Evening play", 15, "low", time="18:00")
    scheduler = Scheduler([clash_a, clash_b, clear], available_minutes=120)

    warnings = scheduler.detect_conflicts()

    # Exactly one conflict (the 09:00 pair); the 18:00 task is not flagged.
    assert len(warnings) == 1
    assert "09:00" in warnings[0]
    assert "Feed cat" in warnings[0]
    assert "Walk dog" in warnings[0]
