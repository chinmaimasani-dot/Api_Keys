"""A simple command-line task manager with JSON-file storage."""

def show_tasks(tasks, status_filter="All"):
    """Display tasks, optionally filtering by Pending or Completed."""
    visible_tasks = [
        task for task in tasks
        if status_filter == "All" or task["status"] == status_filter
    ]

    print(f"\n{status_filter} tasks")
    print("-" * 40)
    if not visible_tasks:
        print("No tasks to show.")
        return

    for task in visible_tasks:
        print(f'{task["id"]}. [{task["status"]}] {task["title"]}')


def next_task_id(tasks):
    """Return an unused task number."""
    return max((task["id"] for task in tasks), default=0) + 1


def find_task(tasks, task_id):
    """Find a task by its number."""
    return next((task for task in tasks if task["id"] == task_id), None)


def read_task_id(prompt):
    """Ask for a task number and handle non-numeric input."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a whole number.")
        return None


def main():
    # Tasks are kept in memory and reset when the program exits.
    tasks = []

    while True:
        print("\n=== Task Manager ===")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. Mark a task as completed")
        print("4. Delete a task")
        print("5. Filter tasks by status")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            title = input("Enter the task: ").strip()
            if not title:
                print("A task cannot be empty.")
                continue
            task = {"id": next_task_id(tasks), "title": title, "status": "Pending"}
            tasks.append(task)
            print("Task added.")

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            show_tasks(tasks)
            task_id = read_task_id("Enter the task number to complete: ")
            task = find_task(tasks, task_id) if task_id is not None else None
            if task is None:
                print("Task not found.")
            elif task["status"] == "Completed":
                print("That task is already completed.")
            else:
                task["status"] = "Completed"
                print("Task marked as completed.")

        elif choice == "4":
            show_tasks(tasks)
            task_id = read_task_id("Enter the task number to delete: ")
            task = find_task(tasks, task_id) if task_id is not None else None
            if task is None:
                print("Task not found.")
            else:
                tasks.remove(task)
                print("Task deleted.")

        elif choice == "5":
            print("1. All   2. Pending   3. Completed")
            filter_choice = input("Choose a filter (1-3): ").strip()
            filters = {"1": "All", "2": "Pending", "3": "Completed"}
            if filter_choice in filters:
                show_tasks(tasks, filters[filter_choice])
            else:
                print("Please choose 1, 2, or 3.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
