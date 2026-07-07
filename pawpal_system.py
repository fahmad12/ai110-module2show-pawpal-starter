"""PawPal+ — pet care planning system (logic layer)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

PRIORITY_SCORES = {"low": 1, "medium": 2, "high": 3}
START_TIME = time(8, 0)


@dataclass
class Task:
    """A single pet care activity (e.g. a walk, feeding, meds)."""

    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    completed: bool = False

    def priority_score(self) -> int:
        """Return the priority as a sortable number (higher = more important)."""
        return PRIORITY_SCORES.get(self.priority.lower(), 0)

    def fits_in(self, remaining_minutes: int) -> bool:
        """Return True if this task fits within the remaining time."""
        return self.duration_minutes <= remaining_minutes

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the care tasks that belong to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.list_tasks()]


class Scheduler:
    """Builds a daily plan from a set of tasks and a time budget."""

    def __init__(self, tasks: list[Task], available_minutes: int) -> None:
        self.tasks = tasks
        self.available_minutes = available_minutes

    @classmethod
    def from_pet(cls, pet: Pet, available_minutes: int) -> "Scheduler":
        """Build a Scheduler from a single pet's tasks."""
        return cls(pet.list_tasks(), available_minutes)

    @classmethod
    def from_owner(cls, owner: "Owner", available_minutes: int) -> "Scheduler":
        """Build a Scheduler from all of an owner's pets' tasks."""
        return cls(owner.all_tasks(), available_minutes)

    def build_plan(self) -> "DailyPlan":
        """Fit tasks by priority (high first), then shortest first."""
        ordered = sorted(
            self.tasks, key=lambda t: (-t.priority_score(), t.duration_minutes)
        )
        entries: list[Task] = []
        skipped: list[Task] = []
        remaining = self.available_minutes
        for task in ordered:
            if task.fits_in(remaining):
                entries.append(task)
                remaining -= task.duration_minutes
            else:
                skipped.append(task)
        return DailyPlan(entries, skipped)


class DailyPlan:
    """The generated schedule: chosen tasks plus any that didn't fit."""

    def __init__(
        self,
        entries: list[Task] | None = None,
        skipped: list[Task] | None = None,
    ) -> None:
        self.entries = entries or []
        self.skipped = skipped or []

    def total_time(self) -> int:
        """Return the total scheduled minutes across all entries."""
        return sum(t.duration_minutes for t in self.entries)

    def to_text(self) -> str:
        """Return a human-readable, time-stamped version of the plan."""
        if not self.entries and not self.skipped:
            return "No tasks to schedule."
        clock = datetime.combine(date.min, START_TIME)
        lines = ["Daily plan:"]
        for t in self.entries:
            lines.append(
                f"  {clock.time().strftime('%H:%M')} — {t.title} "
                f"({t.duration_minutes} min) [priority: {t.priority}]"
            )
            clock += timedelta(minutes=t.duration_minutes)
        if self.skipped:
            lines.append("Skipped (not enough time): " +
                         ", ".join(t.title for t in self.skipped))
        return "\n".join(lines)
