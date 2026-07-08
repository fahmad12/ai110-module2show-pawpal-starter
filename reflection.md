# PawPal+ Project Reflection

## 1. System Design

    Three Core Actions: A user should be able enter basic pet and owner information, add and edit tasks (at minimum, their duration and priority), and track pet care tasks.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    In my initial UML design, I included four main classes: Task (responsibilities include priority and duration), Pet (responsibilities include name and species), Scheduler (responsibilities include reading tasks), and finally DailyPlan (responsibilities include total time and skipped tasks).

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    Yes, my design changed during implementation. One change I made was that I had added, and then removed, the ScheduledTask class, which I then removed because it was overcomplicating the code.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

    One tradeoff was that I decided have the knapsack keep track of all the tasks as it went along, as composed to compiling the list at the very end. While it was slower, it was done to make the code easier to read.

- Why is that tradeoff reasonable for this scenario?

    This tradeoff is reasonable for this scenario because it makes it easier for a person to read, as opposed to running a little bit faster.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    I used AI tools to help brainstorm test plans, debug code and features, and asked what changes were needed in my files. Specific prompts and questions were most helpful because they included more details as to what to fix and what the expected output should look like.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    One moment I did not accept an AI suggestion was when I had asked it something about the README file, and it wanted to change my answers for one of the questions. However, I did not ask it to change the answers nor did I want it to do that because I liked what i had written. I verfiied what AI suggested by running tests/debugging sessions.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

    I tested the core behavior that the code should be running properly. These tests are important because they allow for the app to run as it is intended to.

**b. Confidence**

- How confident are you that your scheduler works correctly?

    On a scale of 5, my confidence level is a 4.

- What edge cases would you test next if you had more time?

    If I had more time, I would probably test what would happen if time constraints wasn't an issue and if the pet didn't have any tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I am most satisfied with how the main component/functions are working properly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    If I had anothe iteration, I would improve this by putting the tasks for both pets in the same line if they happen at the same time just to make it look less repetitive.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    One thing I learned about working with AI is to always debug and ask it to expalin the code it generates.