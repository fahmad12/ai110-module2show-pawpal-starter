import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Keep one Owner in session state so pets/tasks survive re-runs.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

# --- Add a pet -------------------------------------------------------------
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species))
    st.success(f"Added {pet_name} ({species}).")

if owner.pets:
    st.write("Current pets:", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task to a pet ---------------------------------------------------
st.subheader("Add a Task")
if not owner.pets:
    st.info("Add a pet first, then you can add tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        which_pet = st.selectbox("Pet", pet_names)
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col5, col6 = st.columns(2)
    with col5:
        start_time = st.text_input("Start time (HH:MM, optional)", value="08:00")
    with col6:
        frequency = st.selectbox("Repeats", ["once", "daily", "weekly"])

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == which_pet)
        pet.add_task(
            Task(task_title, int(duration), priority,
                 time=start_time.strip(), frequency=frequency)
        )
        st.success(f"Added '{task_title}' to {which_pet}.")

    # Show each pet's current tasks.
    for p in owner.pets:
        tasks = p.list_tasks()
        if tasks:
            st.write(f"**{p.name}**")
            st.table(
                [
                    {"title": t.title, "time": t.time or "—",
                     "duration (min)": t.duration_minutes, "priority": t.priority,
                     "repeats": t.frequency,
                     "done": "✓" if t.completed else ""}
                    for t in tasks
                ]
            )

st.divider()

# --- Today's timeline: sorting + conflict detection ------------------------
st.subheader("Today's Timeline")
if not owner.all_tasks():
    st.info("Add a pet and some tasks to see the timeline.")
else:
    timeline = Scheduler.from_owner(owner, 0)

    # Warn the owner about any double-booked times first — this is the most
    # actionable thing they can fix, so it goes at the top and stays visible.
    conflicts = timeline.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
        st.caption("Two tasks share a start time — consider moving one.")
    else:
        st.success("No scheduling conflicts. 🎉")

    # Show every task in chronological order.
    ordered = timeline.sort_by_time()
    st.table(
        [
            {"time": t.time or "—", "task": t.title,
             "duration (min)": t.duration_minutes, "priority": t.priority}
            for t in ordered
        ]
    )

st.divider()

# --- Filter tasks ----------------------------------------------------------
st.subheader("Find Tasks")
if not owner.all_tasks():
    st.info("Add tasks to filter them.")
else:
    finder = Scheduler.from_owner(owner, 0)
    col_a, col_b = st.columns(2)
    with col_a:
        status = st.selectbox("Status", ["all", "pending", "completed"])
    with col_b:
        name_query = st.text_input("Title contains", value="")

    completed_filter = {"all": None, "pending": False, "completed": True}[status]
    matches = finder.filter_tasks(
        completed=completed_filter,
        pet_name=name_query.strip() or None,
    )
    if matches:
        st.table(
            [
                {"task": t.title, "time": t.time or "—",
                 "priority": t.priority, "done": "✓" if t.completed else ""}
                for t in matches
            ]
        )
    else:
        st.info("No tasks match those filters.")

st.divider()

# --- Build the schedule ----------------------------------------------------
st.subheader("Build Schedule")
available_minutes = st.number_input(
    "Time available today (minutes)", min_value=1, max_value=1440, value=90
)

if st.button("Generate schedule"):
    if not owner.all_tasks():
        st.warning("No tasks to schedule yet. Add a pet and some tasks first.")
    else:
        plan = Scheduler.from_owner(owner, int(available_minutes)).build_plan()

        st.success(
            f"Planned {len(plan.entries)} task(s) using "
            f"{plan.total_time()} of {int(available_minutes)} min."
        )
        if plan.entries:
            st.table(
                [
                    {"task": t.title, "duration (min)": t.duration_minutes,
                     "priority": t.priority}
                    for t in plan.entries
                ]
            )
        if plan.skipped:
            st.warning(
                "Not enough time for: "
                + ", ".join(t.title for t in plan.skipped)
            )
        # Keep the timestamped text version too, for the "why/when" detail.
        with st.expander("See timed plan"):
            st.text(plan.to_text())
