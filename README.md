# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Schedule for A Today:
================================
Daily plan:
  08:00 — Feeding (10 min) [priority: high]
  08:10 — Walk in Morning (30 min) [priority: high]
  08:40 — Litter change (15 min) [priority: medium]
  08:55 — Play time (20 min) [priority: low]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

  #The tests check if a task is completed, if adding a task increases the task count, if the task list is returned in chronological order, if a daily/weekly task is automatically added when it is completed, and if two tasks scheduled at the same time are detected. 

# Run with coverage:
pytest --cov
```

Sample test output:

platform darwin -- Python 3.11.4, pytest-7.4.0, pluggy-1.0.0
rootdir: /Users/fahmad/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 5 items                                                                                          

tests/test_pawpal.py .....                                                                           [100%]

============================================ 5 passed in 0.01s =============================================

```
# Confidence Level: 4/5 ⭐⭐⭐⭐
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | Scheduler.sort_by_time() | e.g., sort taks by their start time |
| Filtering behavior | Scheduler.filter_tasks() | e.g., filter tasks by name of pet or completion status |
| Conflict detection handling | Scheduler.detect_conflicts() | e.g., gives warning if two tasks are happening at the same time |
| Recurring task logic | Task.next_occurance() | e.g., automatically adds daily/weekly task to list when completed |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
