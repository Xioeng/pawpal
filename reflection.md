# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The initial UML design for the PawPal+ scheduler included some main clases: 'Pet', 'Task', 'Schedule'. The 'Pet' class had attributes like name, type, and preferences. 

- What classes did you include, and what responsibilities did you assign to each?

The 'Task' class included attributes such as description, duration, frequency, and priority. The 'Schedule' class was responsible for managing the list of tasks and generating a feasible schedule based on the pet's needs and available time. The 'Pet' class was responsible for storing information about the pet and its preferences. The 'Owner' class was responsible for managing the pet and its schedule.
Later, I added an enumerator for task priority, which helped to better organize and prioritize tasks in the scheduling process so the can be treated as numbers.

**b. Design changes**

- Did your design change during implementation?

Yes, substantially the design changed during implementation. Initially, I had a simpler design with multiple classes and relationships. However, as I started implementing the scheduler, I noticed that some pseudoclasses were needed like enumerators, so they have a clear role in the scheduling process. I also had to adjust the responsibilities of some classes to better fit the scheduling logic and to make the implementation more efficient.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers time, priority and preferences.Nonetheless, it mostly sorts the tasks by priority order and then by duration, so the most important and shorter tasks are scheduled first.
- How did you decide which constraints mattered most?

The constraints were decided based on the importance of the tasks for the pet's well-being and the owner's schedule. Time was a crucial constraint to ensure that tasks are scheduled within the available time slots. Yet, mainly the priority of the tasks was the most important constraint, as it ensures that the most critical tasks for the pet's health and happiness are scheduled first. Preferences were also considered to make sure that the schedule is tailored to the pet's needs and the owner's lifestyle.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
In order to ensure that the most important tasks are scheduled first, the scheduler may sometimes schedule shorter tasks before longer ones, even if the longer tasks are also important. This tradeoff allows for a more efficient use of time, understood as the numbers of tasks completed within the available time slots.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable for this scenario because it allows for a more efficient use of time while still prioritizing the most critical tasks for the pet's well-being. By doing this, the owner should be able to complete the biggest and most important tasks first.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
