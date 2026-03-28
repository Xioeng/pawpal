# PawPal Class Structure

```mermaid
classDiagram
    class Priority {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
    }

    class Pet {
        -name: str
        -species: str
        -age: int
        -special_needs: list
        +add_special_need(need: str): void
        +get_info(): str
    }

    class Owner {
        -name: str
        -email: str
        -phone: str
        -pets: list[Pet]
        -preferences: dict
        +add_pet(pet: Pet): void
        +remove_pet(pet: Pet): void
        +set_preference(key: str, value): void
        +get_info(): str
    }

    class Task {
        -task_type: str
        -pet: Pet
        -frequency: int
        -duration: int
        -priority: Priority
        -preferred_times: list
        +is_urgent(): bool
        +get_task_info(): str
    }

    class Schedule {
        -date: date
        -available_time: int
        -scheduled_tasks: list[Task]
        -total_time_used: int
        +add_task_to_schedule(task: Task): bool
        +is_feasible(): bool
        +get_daily_plan(): str
        +explain_reasoning(): str
    }

    class PetCareTracker {
        -owner_name: str
        -available_time: int
        -pets: list[Pet]
        -tasks: list[Task]
        +add_pet(pet: Pet): void
        +add_task(task: Task): void
        +create_daily_schedule(date_: date): Schedule
        +get_summary(): str
    }

    Owner "1" --> "*" Pet
    Task "many" --> "1" Pet
    Task "*" --> "1" Priority
    PetCareTracker "1" --> "*" Pet
    PetCareTracker "1" --> "*" Task
    Schedule "1" --> "*" Task
```

## Relationships

- **Owner** has many **Pets**
- **Task** belongs to a **Pet** and uses **Priority** enum
- **PetCareTracker** manages multiple **Pets** and **Tasks**, creates **Schedules**
- **Schedule** contains multiple **Tasks**
