# 🐾 PawPal+ - Pet Care Scheduler

> An intelligent Streamlit web application that helps pet owners create achievable daily schedules based on available time and care priorities.

## 🎯 About the App

**PawPal+** is a smart pet care planning assistant designed for busy pet owners. It uses priority-based scheduling algorithms to help you manage multiple pets' care needs efficiently while respecting time constraints.

### ✨ Key Features

- 👤 **Owner Profiles**: Track owner information and preferences (email, phone, daily available time)
- 🐕 **Pet Management**: Add and manage multiple pets with detailed health information
  - Species, age, breed, weight tracking
  - Special needs, medications, and allergies
- 📋 **Task Planning**: Create pet care tasks with customizable parameters
  - Task type, frequency, duration, and priority levels
- 🔄 **Smart Scheduling**: Intelligent algorithm that prioritizes high-priority tasks
  - Greedy scheduling based on priority (HIGH → MEDIUM → LOW)
  - Respects available time constraints
  - Prevents overcommitting
- 📊 **Visual Feedback**: Interactive daily plan display
  - Task summaries with emojis and badges
  - Time usage metrics and progress bars
  - Feasibility indicators
- 📝 **Scheduling Explanation**: Detailed reasoning for scheduling decisions

## 🏗️ Architecture

### Class Documentation

#### Core Models

**`Owner`** (`src/models/owner.py`)
- Represents a pet owner with contact information and preferences
- **Attributes**: `name`, `email`, `phone`, `pets` (list), `preferences` (dict)
- **Methods**:
  - `add_pet(pet)`: Add a pet to owner's collection
  - `remove_pet(pet)`: Remove a pet from collection
  - `set_preference(key, value)`: Store owner preferences (e.g., daily available time)
  - `get_info()`: Get formatted owner information string

**`Pet`** (`src/models/pet.py`)
- Represents a pet with detailed health and care information
- **Attributes**: `name`, `species`, `age`, `breed`, `weight`, `owner_name`, `special_needs`, `medications`, `allergies`
- **Methods**:
  - `add_special_need(need)`: Add a special need (arthritis, anxiety, etc.)
  - `remove_special_need(need)`: Remove a special need
  - `add_medication(medication)`: Add a medication
  - `add_allergy(allergy)`: Add an allergy
  - `get_info()`: Get formatted pet information string

**`Task`** (`src/models/task.py`)
- Represents a single pet care task
- **Attributes**: `task_type`, `pet`, `frequency` (times/day), `duration` (minutes), `priority`, `preferred_times`
- **Methods**:
  - `is_urgent()`: Check if task is high priority
  - `get_task_info()`: Get formatted task information

**`Schedule`** (`src/models/schedule.py`)
- Represents a finalized daily schedule
- **Attributes**: `date`, `available_time`, `scheduled_tasks`, `total_time_used`
- **Methods**:
  - `is_feasible()`: Check if schedule fits within available time
  - `get_daily_plan()`: Get formatted daily plan string

**`Priority`** (`src/models/enums.py`)
- Enum for task priority levels
- **Values**: `HIGH` (value="high"), `MEDIUM` (value="medium"), `LOW` (value="low")
- **Behavior**: Supports comparison operators for sorting (HIGH < MEDIUM < LOW)

#### Core Logic

**`Scheduler`** (`src/core/scheduler.py`)
- Implements the scheduling algorithm and logic
- **Methods**:
  - `schedule_tasks(tasks, available_time)`: Schedule tasks using greedy priority-based algorithm
    - Returns: `(scheduled_tasks: List[Task], total_time_used: int)`
  - `is_feasible(tasks, available_time)`: Check if all tasks can fit within time constraint
  - `explain_scheduling(scheduled_tasks, available_time, total_time_used)`: Generate explanation of scheduling decisions

### Scheduling Algorithm

The scheduler uses a **greedy priority-based approach**:

1. **Sort** all tasks by priority (HIGH → MEDIUM → LOW)
2. **Iterate** through sorted tasks in order
3. **Add** each task if total time + task time ≤ available time
4. **Skip** task if it exceeds remaining time
5. **Return** scheduled tasks and total time used

**Time Calculation**: `task_time = duration × frequency`
- Example: Feeding 2x/day × 30 mins = 60 mins total

## 🚀 Getting Started

### Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📊 How to Use

### Step 1: Create Owner Profile
- Enter your name, email (optional), phone (optional)
- Set available daily time for pet care (e.g., 200 minutes)
- Click "Create Owner Profile"

### Step 2: Add Pets
- Enter pet name, species, age, and breed
- Add weight, special needs, medications, and allergies
- Click "Add Pet"
- View and manage your pet collection

### Step 3: Create Tasks
- Select task type (Feeding, Walking, Grooming, etc.)
- Choose which pet the task is for
- Set frequency (times per day) and duration (minutes)
- Set priority level (LOW, MEDIUM, HIGH)
- Click "Add Task"

### Step 4: Generate Schedule
- Review your task summary
- Check if all tasks fit within available time
- Click "Generate Schedule" to create your daily plan

### Step 5: Review Your Plan
- View your daily schedule in a formatted plan
- See time usage metrics and remaining time
- Check feasibility status
- Read the scheduling explanation

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Test Structure

- **`tests/test_models/`**: Unit tests for model classes
  - `test_task.py`: Task model tests
  - `test_pet.py`: Pet model tests
  - `test_owner.py`: Owner model tests
  - `test_schedule.py`: Schedule model tests
  - `test_enums.py`: Priority enum tests
- **`tests/test_core/`**: Scheduler algorithm tests
  - `test_scheduler.py`: Comprehensive scheduler tests
- **`tests/test_integration.py`**: Integration tests with realistic owner scenarios

### Test Coverage

- Owner profile creation and pet management
- Pet health information (meds, allergies, special needs)
- Task creation with various parameters
- Priority-based scheduling algorithm
- Feasibility checking
- Edge cases (empty lists, exact fit, exceeds time, etc.)

## 📁 Project Structure

```
pawpal/
├── app.py                          # Streamlit web interface
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── scheduler.py           # Scheduling algorithm
│   └── models/
│       ├── __init__.py
│       ├── enums.py               # Priority enum
│       ├── owner.py               # Owner class
│       ├── pet.py                 # Pet class
│       ├── task.py                # Task class
│       └── schedule.py            # Schedule class
└── tests/
    ├── test_models/
    │   ├── test_task.py
    │   ├── test_pet.py
    │   ├── test_owner.py
    │   ├── test_schedule.py
    │   └── test_enums.py
    ├── test_core/
    │   └── test_scheduler.py
    └── test_integration.py
```

## 🔧 Technology Stack

- **Framework**: Streamlit (interactive UI)
- **Language**: Python 3.8+
- **Testing**: pytest
- **Data Classes**: Python dataclasses / custom classes

## 📈 Example Workflow

1. **Owner**: Sarah, 120 mins/day available
2. **Pets**: 
   - Max (Dog, 7 y/o) with hip dysplasia, needs medications
   - Whiskers (Cat, 4 y/o) with fish allergy
3. **Tasks**:
   - Max: Walk (HIGH, 1x/day, 30 mins)
   - Max: Feeding (HIGH, 2x/day, 15 mins)
   - Max: Medication (HIGH, 1x/day, 10 mins)
   - Whiskers: Feeding (HIGH, 2x/day, 10 mins)
   - Whiskers: Grooming (MEDIUM, 1x/day, 45 mins)

**Result**: Scheduler prioritizes all HIGH priority tasks (75 mins), then fits MEDIUM tasks if space allows. Sarah gets a realistic daily plan respecting her 120-minute constraint.

## 💡 Key Design Decisions

- **Priority-Based Scheduling**: Ensures critical care (medications, essential feeding) always gets scheduled
- **Session State**: Streamlit's session state persists data across user interactions
- **Modular Architecture**: Separate models and scheduling logic for testability
- **Greedy Algorithm**: Simple, efficient, and predictable for users to understand
- **Time Validation**: Prevents unrealistic schedules with feasibility checking

## 🎓 Learning Outcomes

This project demonstrates:
- Object-oriented design (classes, inheritance, methods)
- Algorithm design (greedy scheduling)
- Test-driven development (unit and integration tests)
- Data persistence and state management
- Interactive UI development with Streamlit
- Priority optimization under constraints
