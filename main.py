"""PawPal+ Scheduler - Main entry point with three different owner scenarios"""

from datetime import date

import src as pawpal


def busy_owner_scenario():
    """Scenario 1: Busy professional owner with limited time (120 minutes/day)"""
    print("\n" + "=" * 80)
    print("SCENARIO 1: BUSY PROFESSIONAL OWNER (Sarah - 120 minutes/day)")
    print("=" * 80)

    owner = pawpal.Owner("Sarah", email="sarah@work.com", phone="555-0101")
    owner.set_preference("daily_time", 120)
    owner.set_preference("schedule_type", "strict")

    # Sarah has a dog and a cat - both need care but she's busy
    dog = pawpal.Pet("Max", "Dog", 7, breed="Labrador", weight=35.0)
    dog.add_special_need("hip dysplasia")
    dog.add_medication("Joint supplements")

    cat = pawpal.Pet("Whiskers", "Cat", 4, breed="Persian", weight=5.5)
    cat.add_allergy("fish")

    owner.add_pet(dog)
    owner.add_pet(cat)

    print(f"\n{owner.get_info()}")

    # Create realistic tasks for busy owner
    tasks = [
        pawpal.Task("Morning walk", dog, 1, 25, pawpal.Priority.HIGH),
        pawpal.Task("Feeding", dog, 2, 15, pawpal.Priority.HIGH),
        pawpal.Task("Medication", dog, 1, 10, pawpal.Priority.HIGH),
        pawpal.Task("Evening walk", dog, 1, 20, pawpal.Priority.MEDIUM),
        pawpal.Task("Playtime", dog, 1, 15, pawpal.Priority.LOW),
        pawpal.Task("Feeding", cat, 2, 10, pawpal.Priority.HIGH),
        pawpal.Task("Litter box", cat, 2, 5, pawpal.Priority.HIGH),
        pawpal.Task("Grooming", cat, 1, 15, pawpal.Priority.MEDIUM),
        pawpal.Task("Play session", cat, 1, 10, pawpal.Priority.LOW),
    ]

    scheduler = pawpal.Scheduler()
    available_time = owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(tasks, available_time)

    schedule = pawpal.Schedule(date.today(), available_time, scheduled)
    print(schedule.get_daily_plan())
    print(scheduler.explain_scheduling(scheduled, available_time, total_time))


def moderate_owner_scenario():
    """Scenario 2: Moderate-schedule owner with balanced time (200 minutes/day)"""
    print("\n" + "=" * 80)
    print("SCENARIO 2: MODERATE OWNER (James - 200 minutes/day)")
    print("=" * 80)

    owner = pawpal.Owner("James", email="james@home.com", phone="555-0202")
    owner.set_preference("daily_time", 200)
    owner.set_preference("schedule_type", "balanced")

    # James has multiple pets with varying needs
    dog = pawpal.Pet("Buddy", "Dog", 5, breed="Golden Retriever", weight=30.0)
    dog.add_medication("Allergy medication")

    rabbit = pawpal.Pet("Hoppy", "Rabbit", 3)
    rabbit.add_special_need("requires daily exercise")

    bird = pawpal.Pet("Tweety", "Parrot", 8)

    owner.add_pet(dog)
    owner.add_pet(rabbit)
    owner.add_pet(bird)

    print(f"\n{owner.get_info()}")

    # Create balanced task schedule
    tasks = [
        # Dog care
        pawpal.Task("Morning walk", dog, 1, 20, pawpal.Priority.HIGH),
        pawpal.Task("Feeding", dog, 2, 15, pawpal.Priority.HIGH),
        pawpal.Task("Medication", dog, 1, 5, pawpal.Priority.HIGH),
        pawpal.Task("Evening walk", dog, 1, 20, pawpal.Priority.MEDIUM),
        pawpal.Task("Playtime", dog, 1, 30, pawpal.Priority.MEDIUM),
        # Rabbit care
        pawpal.Task("Feeding", rabbit, 2, 10, pawpal.Priority.HIGH),
        pawpal.Task("Exercise", rabbit, 1, 30, pawpal.Priority.HIGH),
        pawpal.Task("Cleaning", rabbit, 1, 20, pawpal.Priority.MEDIUM),
        # Bird care
        pawpal.Task("Feeding", bird, 1, 10, pawpal.Priority.HIGH),
        pawpal.Task("Interaction", bird, 1, 20, pawpal.Priority.MEDIUM),
        pawpal.Task("Cage cleaning", bird, 1, 30, pawpal.Priority.MEDIUM),
        # General
        # pawpal.Task("Supplies shopping", None, 1, 15, pawpal.Priority.LOW),
    ]

    scheduler = pawpal.Scheduler()
    available_time = owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(tasks, available_time)

    schedule = pawpal.Schedule(date.today(), available_time, scheduled)
    print(schedule.get_daily_plan())
    print(scheduler.explain_scheduling(scheduled, available_time, total_time))


def flexible_owner_scenario():
    """Scenario 3: Flexible/retired owner with ample time (350 minutes/day)"""
    print("\n" + "=" * 80)
    print("SCENARIO 3: FLEXIBLE/RETIRED OWNER (Margaret - 350 minutes/day)")
    print("=" * 80)

    owner = pawpal.Owner("Margaret", email="margaret@retired.com", phone="555-0303")
    owner.set_preference("daily_time", 350)
    owner.set_preference("schedule_type", "flexible")

    # Margaret has rescue pets and special situations
    dogs = [
        pawpal.Pet("Buddy", "Dog", 2, breed="Mixed"),
        pawpal.Pet("Scout", "Dog", 8, breed="Beagle"),
        pawpal.Pet("Luna", "Dog", 3, breed="Husky"),
    ]

    dogs[1].add_special_need("senior dog - requires frequent breaks")
    dogs[1].add_medication("Heart medication")
    dogs[1].add_medication("Arthritis medication")

    dogs[2].add_special_need("high energy - needs lots of exercise")

    cats = [
        pawpal.Pet("Mittens", "Cat", 5),
        pawpal.Pet("Shadow", "Cat", 10),
        pawpal.Pet("Patches", "Cat", 2),
    ]

    cats[1].add_medication("Kidney medication")

    for dog in dogs:
        owner.add_pet(dog)
    for cat in cats:
        owner.add_pet(cat)

    print(f"\n{owner.get_info()}")

    # Create comprehensive task schedule
    tasks = []

    # Dog tasks - differentiate by senior status
    for dog in dogs:
        if dog.age >= 8:  # Senior dog
            tasks.extend(
                [
                    pawpal.Task(
                        f"Morning walk - {dog.name}", dog, 1, 20, pawpal.Priority.HIGH
                    ),
                    pawpal.Task(
                        f"Medication - {dog.name}", dog, 2, 10, pawpal.Priority.HIGH
                    ),
                    pawpal.Task(
                        f"Feeding - {dog.name}", dog, 2, 20, pawpal.Priority.HIGH
                    ),
                    pawpal.Task(
                        f"Afternoon rest break - {dog.name}",
                        dog,
                        1,
                        15,
                        pawpal.Priority.HIGH,
                    ),
                    pawpal.Task(
                        f"Evening walk - {dog.name}", dog, 1, 15, pawpal.Priority.MEDIUM
                    ),
                ]
            )
        else:
            tasks.extend(
                [
                    pawpal.Task(
                        f"Morning walk - {dog.name}", dog, 1, 30, pawpal.Priority.HIGH
                    ),
                    pawpal.Task(
                        f"Feeding - {dog.name}", dog, 2, 15, pawpal.Priority.HIGH
                    ),
                    pawpal.Task(
                        f"Playtime - {dog.name}", dog, 1, 40, pawpal.Priority.MEDIUM
                    ),
                    pawpal.Task(
                        f"Evening walk - {dog.name}", dog, 1, 30, pawpal.Priority.MEDIUM
                    ),
                ]
            )

    # Cat tasks - differentiate by senior status
    for cat in cats:
        cat_tasks = [
            pawpal.Task(f"Feeding - {cat.name}", cat, 2, 10, pawpal.Priority.HIGH),
            pawpal.Task(f"Litter box - {cat.name}", cat, 2, 5, pawpal.Priority.HIGH),
            pawpal.Task(
                f"Interactive play - {cat.name}", cat, 1, 20, pawpal.Priority.MEDIUM
            ),
        ]

        if cat.age >= 10:  # Senior cat
            cat_tasks.append(
                pawpal.Task(f"Medication - {cat.name}", cat, 1, 5, pawpal.Priority.HIGH)
            )

        tasks.extend(cat_tasks)

    scheduler = pawpal.Scheduler()
    available_time = owner.preferences["daily_time"]
    scheduled, total_time = scheduler.schedule_tasks(tasks, available_time)

    schedule = pawpal.Schedule(date.today(), available_time, scheduled)
    print(schedule.get_daily_plan())
    print(scheduler.explain_scheduling(scheduled, available_time, total_time))


def main():
    """Run all three owner scenarios"""
    print("\n" + "=" * 80)
    print("PawPal+ Scheduler - Multi-Owner Scenario Demonstration")
    print("=" * 80)

    # Run all three scenarios
    busy_owner_scenario()
    moderate_owner_scenario()
    flexible_owner_scenario()

    print("\n" + "=" * 80)
    print("All scenarios completed successfully!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
