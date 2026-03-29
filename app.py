"""PawPal+ Streamlit Web Application"""

from datetime import date

import streamlit as st

from src.core.scheduler import Scheduler
from src.models.enums import Priority
from src.models.owner import Owner
from src.models.pet import Pet
from src.models.schedule import Schedule
from src.models.task import Task

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_species_emoji(species: str) -> str:
    """Return emoji for pet species"""
    emoji_map = {
        "Dog": "🐕",
        "Cat": "🐱",
        "Rabbit": "🐰",
        "Bird": "🦜",
        "Other": "🐾",
    }
    return emoji_map.get(species, "🐾")


def get_priority_badge(priority_str: str) -> str:
    """Return color-coded priority badge"""
    badge_map = {
        "HIGH": "🔴 HIGH",
        "MEDIUM": "🟠 MEDIUM",
        "LOW": "🟢 LOW",
    }
    return badge_map.get(priority_str, priority_str)


def get_time_color(remaining: int, total: int) -> str:
    """Return color indicator for remaining time"""
    percentage = (remaining / total * 100) if total > 0 else 0
    if percentage > 30:
        return "🟢"  # Green - plenty of time
    elif percentage > 10:
        return "🟠"  # Orange - getting tight
    else:
        return "🔴"  # Red - very limited


# Page configuration
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# Title and description
st.title("🐾 PawPal+ Scheduler")
st.markdown("An intelligent pet care planning assistant")

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pets" not in st.session_state:
    st.session_state.pets = {}
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "schedule" not in st.session_state:
    st.session_state.schedule = None

# ============================================================================
# SECTION 1: Owner Information
# ============================================================================
st.header("1️⃣ Owner Information")

with st.form(key="owner_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        owner_name = st.text_input("Owner Name", value="")
    with col2:
        owner_email = st.text_input("Email (optional)", value="")
    with col3:
        owner_phone = st.text_input("Phone (optional)", value="")

    daily_time = st.number_input(
        "Available Daily Time (minutes)",
        min_value=30,
        max_value=1440,
        value=200,
        help="How much time can you dedicate to pet care each day?",
    )

    if st.form_submit_button("Create Owner Profile"):
        if owner_name.strip():
            st.session_state.owner = Owner(
                owner_name, email=owner_email, phone=owner_phone
            )
            st.session_state.owner.set_preference("daily_time", daily_time)
            st.success(f"✅ Owner profile created: {owner_name}")
        else:
            st.error("Please enter an owner name")

# Display current owner
if st.session_state.owner:
    st.info(
        f"👤 **Current Owner:** {st.session_state.owner.name} | ⏱️ **Daily Time:** {st.session_state.owner.preferences.get('daily_time', 0)} mins"
    )


# ============================================================================
# SECTION 2: Add Pets and Attributes
# ============================================================================
st.header("2️⃣ Add Pets and Their Attributes")

if st.session_state.owner:
    with st.form(key="pet_form"):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pet_name = st.text_input("Pet Name", value="")
        with col2:
            species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Other"])
        with col3:
            age = st.number_input("Age (years)", min_value=0, max_value=50, value=1)
        with col4:
            breed = st.text_input("Breed (optional)", value="")

        col5, col6 = st.columns(2)
        with col5:
            weight = st.number_input("Weight (kg, optional)", min_value=0.0, value=0.0)
        with col6:
            special_needs = st.text_input(
                "Special Needs (comma-separated, optional)", value=""
            )

        medications = st.text_input("Medications (comma-separated, optional)", value="")
        allergies = st.text_input("Allergies (comma-separated, optional)", value="")

        if st.form_submit_button("Add Pet"):
            if pet_name.strip():
                new_pet = Pet(pet_name, species, age, breed=breed, weight=weight)

                # Add special needs
                if special_needs.strip():
                    for need in [n.strip() for n in special_needs.split(",")]:
                        if need:
                            new_pet.add_special_need(need)

                # Add medications
                if medications.strip():
                    for med in [m.strip() for m in medications.split(",")]:
                        if med:
                            new_pet.add_medication(med)

                # Add allergies
                if allergies.strip():
                    for allergy in [a.strip() for a in allergies.split(",")]:
                        if allergy:
                            new_pet.add_allergy(allergy)

                # Add to owner
                st.session_state.owner.add_pet(new_pet)
                st.session_state.pets[pet_name] = new_pet
                st.success(f"✅ Pet added: {pet_name}")
            else:
                st.error("Please enter a pet name")

    # Display added pets with delete buttons
    if st.session_state.owner.pets:
        st.subheader(f"Your Pets ({len(st.session_state.owner.pets)})")
        for pet_idx, pet in enumerate(st.session_state.owner.pets):
            col1, col2 = st.columns([0.9, 0.1])

            with col1:
                pet_emoji = get_species_emoji(pet.species)
                with st.expander(
                    f"{pet_emoji} {pet.name} ({pet.species}, {pet.age} y/o)"
                ):
                    st.text(pet.get_info())

            with col2:
                if st.button("🗑️", key=f"delete_pet_{pet_idx}", help="Delete this pet"):
                    # Remove pet from owner and tasks
                    st.session_state.owner.pets.remove(pet)
                    st.session_state.tasks = [
                        t for t in st.session_state.tasks if t.pet != pet
                    ]
                    st.success("✅ Pet deleted")
                    st.rerun()
    else:
        st.info("🐾 No pets yet? Add your first furry friend!")

else:
    st.warning("⚠️ Please create an owner profile first")

st.divider()

# ============================================================================
# SECTION 3: Create and Assign Tasks
# ============================================================================
st.header("3️⃣ Create and Assign Tasks")

if st.session_state.owner and st.session_state.owner.pets:
    with st.form(key="task_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            task_type = st.text_input(
                "Task Type", value="", placeholder="e.g., Feeding, Walking, Grooming"
            )
        with col2:
            pet_select = st.selectbox(
                "Assign to Pet", [p.name for p in st.session_state.owner.pets]
            )
        with col3:
            frequency = st.number_input(
                "Frequency (times/day)", min_value=1, max_value=10, value=1
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            duration = st.number_input(
                "Duration (minutes per instance)", min_value=1, max_value=240, value=30
            )
        with col5:
            priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH"], index=1)
        with col6:
            st.write("")  # Spacing

        if st.form_submit_button("Add Task"):
            if task_type.strip() and pet_select:
                # Find the pet object
                selected_pet = next(
                    (p for p in st.session_state.owner.pets if p.name == pet_select),
                    None,
                )

                if selected_pet:
                    # Convert priority string to enum
                    priority_enum = Priority.MEDIUM
                    if priority == "HIGH":
                        priority_enum = Priority.HIGH
                    elif priority == "LOW":
                        priority_enum = Priority.LOW

                    new_task = Task(
                        task_type, selected_pet, frequency, duration, priority_enum
                    )
                    st.session_state.tasks.append(new_task)
                    st.success(f"✅ Task created: {task_type} for {pet_select}")

    # Display tasks with delete buttons
    if st.session_state.tasks:
        st.subheader(f"Created Tasks ({len(st.session_state.tasks)})")

        # Task summary badge
        high_priority_count = sum(
            1 for task in st.session_state.tasks if task.priority == Priority.HIGH
        )
        total_task_time = sum(
            task.duration * task.frequency for task in st.session_state.tasks
        )
        st.markdown(
            f"📊 **Summary:** {len(st.session_state.tasks)} tasks total • {high_priority_count} HIGH priority • {total_task_time} mins required"
        )

        # Task list with individual delete buttons
        for idx, task in enumerate(st.session_state.tasks):
            col1, col2 = st.columns([0.9, 0.1])

            with col1:
                # Task card display with pet emoji and priority badge
                pet_emoji = get_species_emoji(task.pet.species)
                priority_badge = get_priority_badge(task.priority.value.upper())
                task_info = f"{pet_emoji} **{task.task_type}** • {task.pet.name} • {task.frequency}x/day • {task.duration} mins • {priority_badge}"
                st.markdown(task_info)

            with col2:
                # Delete button
                if st.button("🗑️", key=f"delete_task_{idx}", help="Delete this task"):
                    st.session_state.tasks.pop(idx)
                    st.success("✅ Task deleted")
                    st.rerun()

        # Summary table
        st.subheader("Task Summary Table")
        task_data = []
        for task in st.session_state.tasks:
            task_data.append(
                {
                    "Pet": f"{get_species_emoji(task.pet.species)} {task.pet.name}",
                    "Task": task.task_type,
                    "Frequency": f"{task.frequency}x/day",
                    "Duration": f"{task.duration} mins",
                    "Total Time": f"{task.duration * task.frequency} mins",
                    "Priority": get_priority_badge(task.priority.value.upper()),
                }
            )
        st.dataframe(task_data, use_container_width=True)

        # Clear all tasks button
        col1, col2 = st.columns([0.85, 0.15])
        with col2:
            if st.button("🗑️ Clear All", help="Delete all tasks"):
                st.session_state.tasks = []
                st.success("✅ All tasks cleared")
                st.rerun()

    else:
        st.info("📋 No tasks yet. Add one above to get started!")

else:
    st.warning("⚠️ Please add at least one pet first")

st.divider()

# ============================================================================
# SECTION 4: Schedule Constraints and Generation
# ============================================================================
st.header("4️⃣ Schedule Settings & Generate Plan")

if st.session_state.owner and st.session_state.tasks:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Summary")
        st.metric("Owner", st.session_state.owner.name)
        st.metric("Pets", len(st.session_state.owner.pets))
        st.metric("Tasks", len(st.session_state.tasks))
        available_time = st.session_state.owner.preferences.get("daily_time", 0)
        st.metric("Available Time", f"{available_time} mins")

    with col2:
        st.subheader("⚙️ Scheduling Options")
        schedule_date = st.date_input("Schedule Date", value=date.today())

        # Calculate total task time
        total_task_time = sum(
            task.duration * task.frequency for task in st.session_state.tasks
        )
        st.metric("Total Task Time", f"{total_task_time} mins")

        # Progress bar for time usage
        if available_time > 0:
            usage_percentage = min(total_task_time / available_time, 1.0)
            st.progress(
                usage_percentage,
                text=f"{total_task_time}/{available_time} mins ({usage_percentage * 100:.0f}%)",
            )

        if total_task_time > available_time:
            st.warning(
                f"⚠️ Total task time ({total_task_time} mins) exceeds available time ({available_time} mins). Some tasks will be deprioritized."
            )
        else:
            st.success(f"✅ All tasks fit within available time!")

    # Schedule button
    if st.button("📅 Generate Schedule", use_container_width=True, type="primary"):
        scheduler = Scheduler()
        available_time = st.session_state.owner.preferences.get("daily_time", 0)

        # Schedule the tasks
        scheduled_tasks, total_time = scheduler.schedule_tasks(
            st.session_state.tasks, available_time
        )

        # Create schedule
        st.session_state.schedule = Schedule(
            schedule_date, available_time, scheduled_tasks
        )

else:
    st.warning("⚠️ Please add owner, pets, and tasks first")

st.divider()

# ============================================================================
# SECTION 5: Display Generated Schedule
# ============================================================================
if st.session_state.schedule:
    st.header("5️⃣ Your Daily Plan")

    # Display plan in a nice container
    st.subheader("📅 Daily Schedule")
    plan = st.session_state.schedule.get_daily_plan()
    with st.container(border=True):
        st.text(plan)

    # Display scheduling explanation
    scheduler = Scheduler()
    available_time = st.session_state.owner.preferences.get("daily_time", 0)
    explanation = scheduler.explain_scheduling(
        st.session_state.schedule.scheduled_tasks,
        available_time,
        st.session_state.schedule.total_time_used,
    )

    with st.expander("📝 Scheduling Explanation"):
        st.text(explanation)

    # Scheduled tasks table
    st.subheader("Scheduled Tasks")
    if st.session_state.schedule.scheduled_tasks:
        scheduled_data = []
        for task in st.session_state.schedule.scheduled_tasks:
            scheduled_data.append(
                {
                    "Pet": f"{get_species_emoji(task.pet.species)} {task.pet.name}",
                    "Task": task.task_type,
                    "Frequency": f"{task.frequency}x/day",
                    "Duration": f"{task.duration} mins",
                    "Total Time": f"{task.duration * task.frequency} mins",
                    "Priority": get_priority_badge(task.priority.value.upper()),
                }
            )
        st.dataframe(scheduled_data, use_container_width=True)

    # Feasibility check with colored time remaining
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tasks Scheduled", len(st.session_state.schedule.scheduled_tasks))

    with col2:
        st.metric("Time Used", f"{st.session_state.schedule.total_time_used} mins")

    with col3:
        remaining = (
            st.session_state.owner.preferences.get("daily_time", 0)
            - st.session_state.schedule.total_time_used
        )
        time_color = get_time_color(
            remaining, st.session_state.owner.preferences.get("daily_time", 0)
        )
        st.metric(
            "Time Remaining",
            f"{remaining} mins",
            delta=None,
            delta_color="off",
            help=f"{time_color} Status indicator",
        )

    # Feasibility status
    if st.session_state.schedule.is_feasible():
        st.success(
            "✅ Schedule is feasible! All scheduled tasks fit within available time."
        )
    else:
        st.error("❌ Schedule exceeds available time. Please reduce task scope.")

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear Schedule", use_container_width=True):
            st.session_state.schedule = None
            st.rerun()

    with col2:
        if st.button("🔁 Edit Tasks", use_container_width=True):
            st.session_state.schedule = None
            st.toast("Schedule cleared. Edit your tasks above.")

st.divider()

# Footer
st.markdown("""
---
**PawPal+** helps you create achievable pet care schedules based on your available time and priorities.
Made with ❤️ for pet lovers.
""")
