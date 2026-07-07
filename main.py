from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("A")

petA = Pet("Pet A", "dog")
petB = Pet("Pet B", "cat")
owner.add_pet(petA)
owner.add_pet(petB)

petA.add_task(Task("Walk in Morning", 30, "high"))
petA.add_task(Task("Feeding", 10, "high"))
petB.add_task(Task("Litter change", 15, "medium"))
petB.add_task(Task("Play time", 20, "low"))

plan = Scheduler.from_owner(owner, available_minutes=90).build_plan()

print(f"Schedule for {owner.name} Today: ")
print("=" * 32)
print(plan.to_text())
