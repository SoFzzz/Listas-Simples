"""Node definition for the singly linked task list."""


class Node:
    """Single node in the linked list."""

    def __init__(self, task: str, priority: int) -> None:
        self.task = task
        self.priority = priority
        self.next = None  # Pointer to the next node
