"""Basic tests for PawPal+ core classes."""

import os
import sys

# Make the project root importable so `pawpal_system` is found from tests/.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pawpal_system import Pet, Task


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
