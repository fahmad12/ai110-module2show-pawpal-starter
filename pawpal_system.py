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
    time: str = ""  # scheduled start time in "HH:MM" (24-hour) format
    completed: bool = False
    frequency: str = "once"  # "once" | "daily" | "weekly"
    due_date: date | None = None

    def priority_score(self) -> int:
        """Return the priority as a sortable number (higher = more important)."""
        return PRIORITY_SCORES.get(self.priority.lower(), 0)

    def fits_in(self, remaining_minutes: int) -> bool:
        """Return True if this task fits within the remaining time."""
        return self.duration_minutes <= remaining_minutes

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Return a fresh, uncompleted copy for the next occurrence.

        Daily tasks advance the due date by one day, weekly by seven days,
        using timedelta so month/year rollovers are handled correctly. A
        one-off task ("once") has no next occurrence and returns None.
        """
        steps = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        step = steps.get(self.frequency.lower())
        if step is None:
            return None
        base = self.due_date or date.today()
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            time=self.time,
            completed=False,
            frequency=self.frequency,
            due_date=base + step,
        )


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

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete and, if it recurs, auto-add its next occurrence.

        Returns the newly created follow-up task (or None for one-off tasks).
        """
        task.mark_complete()
        upcoming = task.next_occurrence()
        if upcoming is not None:
            self.add_task(upcoming)
        return upcoming


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
        """Pick the set of tasks that fits the time budget while maximizing
        total priority (a 0/1 knapsack), then order the chosen tasks for
        display by priority (high first), then shortest first."""
        # Only unfinished tasks compete for the day's time budget.
        pending = [t for t in self.tasks if not t.completed]

        chosen = self._best_selection(pending)
        entries = sorted(
            chosen, key=lambda t: (-t.priority_score(), t.duration_minutes)
        )
        skipped = [t for t in pending if t not in chosen]
        return DailyPlan(entries, skipped, self.available_minutes)

    def sort_by_time(self) -> list[Task]:
        """Return the tasks sorted by their "HH:MM" start time.

        Zero-padded "HH:MM" strings sort correctly as plain strings, so a
        simple lambda key on `time` is enough. Tasks with no time ("") sort
        first; use a fallback so they don't crash the comparison.
        """
        return sorted(self.tasks, key=lambda t: t.time or "")

    def filter_tasks(
        self, completed: bool | None = None, pet_name: str | None = None
    ) -> list[Task]:
        """Return tasks matching the given filters.

        - completed: keep only tasks whose completed status matches (True/False).
        - pet_name: keep only tasks whose title mentions the pet name.
        Passing None for a filter means "don't filter on that field".
        """
        result = self.tasks
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if pet_name is not None:
            result = [t for t in result if pet_name.lower() in t.title.lower()]
        return result

    def detect_conflicts(self) -> list[str]:
        """Return a warning for each start time shared by two or more tasks.

        Lightweight: groups tasks by their "HH:MM" time and flags any time
        with more than one task. Tasks without a time ("") are ignored.
        Returns an empty list when there are no conflicts — it never raises.
        """
        by_time: dict[str, list[Task]] = {}
        for task in self.tasks:
            if task.time:
                by_time.setdefault(task.time, []).append(task)

        warnings: list[str] = []
        for start, clashing in sorted(by_time.items()):
            if len(clashing) > 1:
                titles = ", ".join(t.title for t in clashing)
                warnings.append(f"⚠ Conflict at {start}: {titles}")
        return warnings

    def _best_selection(self, tasks: list[Task]) -> list[Task]:
        """0/1 knapsack: choose tasks maximizing summed priority score without
        exceeding available_minutes; ties broken toward using less time."""
        cap = self.available_minutes
        # best[m] = (total_score, minutes_used, [tasks]) reachable in <= m minutes
        best: list[tuple[int, int, list[Task]]] = [(0, 0, []) for _ in range(cap + 1)]
        for task in tasks:
            d, v = task.duration_minutes, task.priority_score()
            if d <= 0 or d > cap:
                continue
            for m in range(cap, d - 1, -1):
                score, used, picked = best[m - d]
                cand = (score + v, used + d, picked + [task])
                cur = best[m]
                # Higher score wins; on a tie prefer the plan using fewer minutes.
                if cand[0] > cur[0] or (cand[0] == cur[0] and cand[1] < cur[1]):
                    best[m] = cand
        return best[cap][2]


class DailyPlan:
    """The generated schedule: chosen tasks plus any that didn't fit."""

    def __init__(
        self,
        entries: list[Task] | None = None,
        skipped: list[Task] | None = None,
        available_minutes: int | None = None,
    ) -> None:
        self.entries = entries or []
        self.skipped = skipped or []
        self.available_minutes = available_minutes

    def total_time(self) -> int:
        """Return the total scheduled minutes across all entries."""
        return sum(t.duration_minutes for t in self.entries)

    def unused_time(self) -> int | None:
        """Return leftover minutes in the budget, or None if unknown."""
        if self.available_minutes is None:
            return None
        return self.available_minutes - self.total_time()

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
        free = self.unused_time()
        if free:
            lines.append(f"Free time: {free} min")
        return "\n".join(lines)
