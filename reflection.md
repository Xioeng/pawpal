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

I used the AI tools to help the design, aid the implementation and debug the code. I was always checking the AI's suggestions and implementations and I directed the design and implementation course. I think the most useful prompts were those that asked about specific implementation. I had the trouble of having circular imports, since some of my classes should be initialized in certain order. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Some scheme for the testing files, I usually do not agree with using classes to interface with pytest when they are not necessary or they do not add any value to the testing process. I prefer to write simple test functions that directly test the functionality of the code without the need for additional layers of abstraction.
- How did you evaluate or verify what the AI suggested?

I usually evaluated the AI's suggestions by checking if they aligned with my design goals and if they were efficient and effective in solving the problem at hand. By general rule, I like going by simple design principles, sometimes I had to ask the AI to simplify its suggestions or to make them more efficient. I also tested the AI's suggestions by implementing them and seeing if they worked as expected in the context of the project.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

For the CLI tests, I tested the basic functionality of the command-line interface, such as adding tasks, viewing the schedule, and ensuring that the commands work as expected. For the scheduler tests, I focused on testing the scheduling logic, including how tasks are prioritized and scheduled based on their attributes (like duration and priority). I also tested edge cases, such as when there are more tasks than available time or when tasks have the same priority. These can be seen in the `main.py` file, where I added print statements to verify the scheduling process and the output of the schedule.

- Why were these tests important?

THey ensure that the core functionality of the scheduler and the CLI is working correctly before moving one, compartmentilizing the testing process and making it more efficient taking care of one problem at the time. For example, testing the scheduling logic separately allows me to verify that the tasks are being scheduled correctly based on their attributes, while testing the CLI ensures that the user interface is functioning as intended. This approach helps to identify and fix issues early in the development process, leading to a more robust and reliable application. And the classes by themselves. In the end, connecting everything with streamlit was about the page design and the user experience instead of coming back and checking that the entire pipeline was working correctly.

**b. Confidence**

- How confident are you that your scheduler works correctly?

The scheduler works with a greedy algorithm, essentially it respects the owner's priorities and tries to maximize the number of tasks executed within the available time. Certainly, if I had more time I'd like to consider more complex scheduling algorithms that could potentially yield better results. For example, so far the most important task takes place at the same time if they repeat. Certainly, it is not quite realistic to feed Fedo twice in a row.
- What edge cases would you test next if you had more time?
If I had more time, I would test edge cases such as when there are conflicting tasks that cannot be scheduled together, or when there are tasks with very long durations that may not fit within the available time slots. I would also test scenarios where the pet has specific preferences that may affect the scheduling, such as avoiding certain times of the day or prioritizing certain types of activities. Additionally, I would test how the scheduler handles changes in the schedule, such as adding or removing tasks after the initial schedule has been generated.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I would say that the class drafting and the scheduling logic are the parts of the project that I am most satisfied with. But also I found quite useful the app integration. I don't know much about streamlit, so it was a good opportunity to learn how to use it and to create a simple user interface for the scheduler. I think the app integration adds a nice touch to the project and makes it more user-friendly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the scheduling algorithm to consider more complex constraints and to optimize the schedule more effectively. For example, I would consider implementing a more sophisticated algorithm that can handle conflicting tasks and optimize the schedule based on multiple criteria, such as minimizing idle time or maximizing the number of tasks completed. Additionally, I would redesign the user interface to make it more intuitive and visually appealing, perhaps by adding features like drag-and-drop scheduling or visual representations of the schedule, maybe considering more standard approaches such as HTML/CSS/JS instead of streamlit, which is not really designed for this kind of applications.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I would say that being critic is important, although AI han do the heavy lifting, it is crucial to evaluate its suggestions critically and to ensure that they align with the overall design goals and principles of the project. Mainly is like having a conversation with a peer in which you can share ideas and suggestions, but at the end of the day, you are the one who has to make the final decisions and to ensure that the project is coherent and well-designed. AI can be a powerful tool for generating ideas and providing suggestions, but it is ultimately up to the human designer to evaluate those suggestions and to make informed decisions about how to implement them in a way that best serves the goals of the project.