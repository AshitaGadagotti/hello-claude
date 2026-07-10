#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with open(TASKS_FILE) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: {TASKS_FILE} is not valid JSON ({e}).")
        print("Fix the file by hand or delete it to start fresh.")
        sys.exit(1)

    if not isinstance(data, list):
        print(f"Error: {TASKS_FILE} should contain a JSON array of tasks, "
              f"but found a {type(data).__name__} instead.")
        sys.exit(1)

    for i, t in enumerate(data):
        if not isinstance(t, dict) or not {"id", "text", "done"} <= t.keys():
            print(f"Error: task at position {i} in {TASKS_FILE} is missing "
                  f"required fields (id, text, done).")
            sys.exit(1)
        if not isinstance(t["id"], int):
            print(f"Error: task at position {i} has a non-integer id: {t['id']!r}.")
            sys.exit(1)
        if not isinstance(t["done"], bool):
            print(f"Error: task at position {i} has a non-boolean done value: {t['done']!r}.")
            sys.exit(1)

    return data


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(text):
    tasks = load_tasks()
    next_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": next_id, "text": text, "done": False})
    save_tasks(tasks)
    print(f"Added task {next_id}: {text}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    for t in tasks:
        mark = "x" if t["done"] else " "
        print(f"[{mark}] {t['id']}: {t['text']}")


def done_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Marked task {task_id} as done.")
            return
    print(f"No task with id {task_id}.")
    sys.exit(1)


def delete_task(task_id):
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"Deleted task {task_id}.")
            return
    print(f"No task with id {task_id}.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Simple command-line to-do list")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", nargs="+", help="Task description")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task id to mark done")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task id to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_task(" ".join(args.text))
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        done_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)


if __name__ == "__main__":
    main()
