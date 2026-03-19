"""Task management via a strictly manual singly linked list."""

if __package__ in (None, ""):
    from node import Node
else:
    from src.node import Node


class TaskManager:
    """Manage tasks using pointer-only traversal and rewiring."""

    def __init__(self) -> None:
        self.head = None

    def add_task(self, task: str, priority: int) -> None:
        """Insert a new task at the head in O(1)."""
        cleaned_task = self._validate_task(task)
        validated_priority = self._validate_priority(priority)
        new_node = Node(cleaned_task, validated_priority)

        # Save the old head before rewiring.
        temp = self.head
        new_node.next = temp
        self.head = new_node

    def remove_task(self, task_name: str) -> None:
        """Find a task by name and unlink its node."""
        if not self.head:
            raise ValueError("Task list is empty.")

        if self.head.task == task_name:
            temp = self.head.next  # Save next before detaching the head.
            self.head.next = None
            self.head = temp
            return

        previous = self.head
        current = self.head.next
        while current and current.task != task_name:
            previous = current
            current = current.next

        if not current:
            raise ValueError("Task not found.")

        temp = current.next  # Preserve the remaining chain.
        previous.next = temp
        current.next = None

    def update_task(self, old_task: str, new_task: str, new_priority: int) -> None:
        """Replace the task data for the matching node."""
        node = self._find_node(old_task)
        if not node:
            raise ValueError("Task not found.")

        node.task = self._validate_task(new_task)
        node.priority = self._validate_priority(new_priority)

    def complete_task(self, task_name: str) -> None:
        """Mark a task as completed in its display text."""
        node = self._find_node(task_name)
        if not node:
            raise ValueError("Task not found.")

        if "(done)" not in node.task:
            node.task = f"{node.task} (done)"

    def move_to_top(self, task_name: str) -> None:
        """Move the matching node to the head by rewiring pointers."""
        if not self.head or self.head.task == task_name:
            return

        previous = self.head
        current = self.head.next
        while current and current.task != task_name:
            previous = current
            current = current.next

        if not current:
            raise ValueError("Task not found.")

        temp = current.next
        previous.next = temp
        current.next = self.head
        self.head = current

    def display_tasks(self) -> str:
        """Return a formatted string with every task."""
        if not self.head:
            return "No tasks available."

        current = self.head
        lines = ""
        number = 1
        while current:
            line = f"{number}. {current.task} (Priority: {current.priority})"
            lines = line if lines == "" else f"{lines}\n{line}"
            current = current.next
            number += 1
        return lines

    def _find_node(self, task_name: str) -> Node | None:
        """Traverse the chain and return the matching node."""
        current = self.head
        while current:
            if current.task == task_name:
                return current
            current = current.next
        return None

    @staticmethod
    def _validate_task(task: str) -> str:
        cleaned = task.strip()
        if not cleaned:
            raise ValueError("Task description cannot be empty.")
        return cleaned

    @staticmethod
    def _validate_priority(priority: int | str) -> int:
        try:
            value = int(priority)
        except (TypeError, ValueError) as exc:
            raise ValueError("Priority must be an integer 1-5.") from exc

        if value < 1 or value > 5:
            raise ValueError("Priority must be between 1 and 5.")
        return value
