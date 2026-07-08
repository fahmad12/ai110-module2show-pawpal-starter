from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("A")

petA = Pet("Pet A", "dog")
petB = Pet("Pet B", "cat")
owner.add_pet(petA)
owner.add_pet(petB)

# Tasks are added out of chronological order on purpose, so we can see
# sort_by_time() put them back in order below.
petA.add_task(Task("Pet A - Walk in Morning", 30, "high", time="08:00"))
petA.add_task(Task("Pet A - Evening Walk", 30, "medium", time="18:30"))
petB.add_task(Task("Pet B - Litter change", 15, "medium", time="12:15",
                   completed=True, frequency="weekly"))
# Same time as Pet A's morning walk (08:00) to demonstrate conflict detection.
petB.add_task(Task("Pet B - Play time", 20, "low", time="08:00"))
petA.add_task(Task("Pet A - Feeding", 10, "high", time="07:30", frequency="daily"))

scheduler = Scheduler.from_owner(owner, available_minutes=120)

# --- Daily plan (priority-based packing) ---
plan = scheduler.build_plan()
print(f"Schedule for {owner.name} Today: ")
print("=" * 32)
print(plan.to_text())

# --- Conflict detection: tasks scheduled at the same time ---
print("\nSchedule conflicts:")
print("=" * 32)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  None found.")

# --- Sorting: tasks in chronological order by their "HH:MM" time ---
print("\nAll tasks sorted by time:")
print("=" * 32)
for t in scheduler.sort_by_time():
    print(f"  {t.time or '--:--'} — {t.title}")

# --- Filtering: by completion status ---
print("\nStill to do (not completed):")
print("=" * 32)
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.time or '--:--'} — {t.title}")

# --- Filtering: by pet name ---
print("\nTasks for Pet A:")
print("=" * 32)
for t in scheduler.filter_tasks(pet_name="Pet A"):
    print(f"  {t.time or '--:--'} — {t.title}")

# --- Recurrence: completing a recurring task auto-creates the next one ---
print("\nCompleting the daily 'Feeding' task:")
print("=" * 32)
feeding = petA.tasks[-1]  # the daily feeding task added above
follow_up = petA.mark_task_complete(feeding)
print(f"  Completed: {feeding.title} (completed={feeding.completed})")
if follow_up is not None:
    print(f"  Auto-created next occurrence due {follow_up.due_date} "
          f"({follow_up.frequency})")

