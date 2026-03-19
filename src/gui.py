"""Tkinter GUI for the LinkedTaskManager application."""

import tkinter as tk
from tkinter import messagebox, ttk

if __package__ in (None, ""):
    from task_manager import TaskManager
else:
    from src.task_manager import TaskManager


class LinkedTaskManagerApp:
    """Tkinter front-end wired to the linked-list task manager."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.manager = TaskManager()
        self.status_var = tk.StringVar(value="Ready")
        self.bg_color = "#0b0b0b"
        self.panel_color = "#151515"
        self.input_color = "#1d1d1d"
        self.accent_color = "#f57c00"
        self.accent_hover = "#ff9800"
        self.text_color = "#ffffff"
        self._build_ui()
        self._refresh_listbox()

    def _build_ui(self) -> None:
        self.root.title("LinkedTaskManager")
        self.root.geometry("680x420")
        self.root.minsize(620, 380)
        self.root.configure(bg=self.bg_color)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Dark.TFrame", background=self.bg_color)
        style.configure("DarkPanel.TFrame", background=self.panel_color)
        style.configure(
            "Title.TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Dark.TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Dark.TLabelframe",
            background=self.bg_color,
            foreground=self.text_color,
            bordercolor=self.accent_color,
        )
        style.configure(
            "Dark.TLabelframe.Label",
            background=self.bg_color,
            foreground=self.text_color,
        )
        style.configure(
            "Orange.TButton",
            background=self.accent_color,
            foreground=self.text_color,
            borderwidth=0,
            focusthickness=0,
            padding=(10, 8),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Orange.TButton",
            background=[("active", self.accent_hover), ("pressed", self.accent_hover)],
            foreground=[("active", self.text_color), ("pressed", self.text_color)],
        )
        style.configure(
            "Dark.TEntry",
            fieldbackground=self.input_color,
            foreground=self.text_color,
            insertcolor=self.text_color,
        )
        style.configure(
            "Dark.TSpinbox",
            fieldbackground=self.input_color,
            foreground=self.text_color,
            insertcolor=self.text_color,
            arrowsize=14,
        )

        main = ttk.Frame(self.root, padding=12, style="Dark.TFrame")
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        title = ttk.Label(main, text="LinkedTaskManager", style="Title.TLabel")
        subtitle = ttk.Label(
            main,
            text="Strict singly linked list - no Python list helpers, pointer-only traversal.",
            style="Subtitle.TLabel",
        )
        title.grid(row=0, column=0, columnspan=3, sticky="w")
        subtitle.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 12))

        ttk.Label(main, text="Task:", style="Dark.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 6)
        )
        self.task_entry = ttk.Entry(main, style="Dark.TEntry")
        self.task_entry.grid(row=2, column=1, sticky="ew", padx=(0, 6))

        ttk.Label(main, text="Priority (1-5):", style="Dark.TLabel").grid(
            row=2, column=2, sticky="e"
        )
        self.priority_spin = ttk.Spinbox(main, from_=1, to=5, width=5, style="Dark.TSpinbox")
        self.priority_spin.set("1")
        self.priority_spin.grid(row=2, column=3, sticky="e", padx=(6, 0))

        button_row = ttk.Frame(main, style="Dark.TFrame")
        button_row.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(12, 12))
        for column in range(6):
            button_row.columnconfigure(column, weight=1)

        ttk.Button(button_row, text="Add", command=self._on_add, style="Orange.TButton").grid(
            row=0, column=0, sticky="ew", padx=3
        )
        ttk.Button(button_row, text="Remove", command=self._on_remove, style="Orange.TButton").grid(
            row=0, column=1, sticky="ew", padx=3
        )
        ttk.Button(button_row, text="Update", command=self._on_update, style="Orange.TButton").grid(
            row=0, column=2, sticky="ew", padx=3
        )
        ttk.Button(button_row, text="Complete", command=self._on_complete, style="Orange.TButton").grid(
            row=0, column=3, sticky="ew", padx=3
        )
        ttk.Button(button_row, text="Move to Top", command=self._on_move_top, style="Orange.TButton").grid(
            row=0, column=4, sticky="ew", padx=3
        )
        ttk.Button(button_row, text="Show All", command=self._refresh_listbox, style="Orange.TButton").grid(
            row=0, column=5, sticky="ew", padx=3
        )

        list_frame = ttk.LabelFrame(main, text="Tasks", padding=8, style="Dark.TLabelframe")
        list_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        main.rowconfigure(4, weight=1)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox = tk.Listbox(
            list_frame,
            activestyle="none",
            exportselection=False,
            font=("Consolas", 11),
            bg=self.panel_color,
            fg=self.text_color,
            selectbackground=self.accent_color,
            selectforeground=self.text_color,
            highlightbackground=self.accent_color,
            highlightcolor=self.accent_color,
            relief="flat",
            yscrollcommand=scrollbar.set,
        )
        self.listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.listbox.yview)

        status = ttk.Label(main, textvariable=self.status_var, style="Dark.TLabel")
        status.grid(row=5, column=0, columnspan=4, sticky="w", pady=(10, 0))

    def _on_add(self) -> None:
        try:
            self.manager.add_task(self.task_entry.get(), self.priority_spin.get())
            self._set_status("Added task at head.")
            self._refresh_listbox()
            self._clear_inputs()
        except ValueError as exc:
            self._error(str(exc))

    def _on_remove(self) -> None:
        task = self._selected_task_name()
        if not task:
            return

        try:
            self.manager.remove_task(task)
            self._set_status(f"Removed '{task}'.")
            self._refresh_listbox()
            self._clear_inputs()
        except ValueError as exc:
            self._error(str(exc))

    def _on_update(self) -> None:
        task = self._selected_task_name()
        if not task:
            return

        try:
            self.manager.update_task(task, self.task_entry.get(), self.priority_spin.get())
            self._set_status(f"Updated '{task}'.")
            self._refresh_listbox()
        except ValueError as exc:
            self._error(str(exc))

    def _on_complete(self) -> None:
        task = self._selected_task_name()
        if not task:
            return

        try:
            self.manager.complete_task(task)
            self._set_status(f"Completed '{task}'.")
            self._refresh_listbox()
        except ValueError as exc:
            self._error(str(exc))

    def _on_move_top(self) -> None:
        task = self._selected_task_name()
        if not task:
            return

        try:
            self.manager.move_to_top(task)
            self._set_status(f"Moved '{task}' to head.")
            self._refresh_listbox()
        except ValueError as exc:
            self._error(str(exc))

    def _selected_task_name(self) -> str | None:
        selection = self.listbox.curselection()
        if not selection:
            self._error("Select a task first.")
            return None

        item_text = self.listbox.get(selection[0])
        split_point = item_text.rfind(" (Priority:")
        return item_text[3:split_point] if split_point != -1 else item_text

    def _refresh_listbox(self) -> None:
        self.listbox.delete(0, tk.END)
        tasks_text = self.manager.display_tasks()

        if tasks_text == "No tasks available.":
            self.listbox.insert(tk.END, tasks_text)
            return

        start = 0
        while True:
            newline_index = tasks_text.find("\n", start)
            if newline_index == -1:
                self.listbox.insert(tk.END, tasks_text[start:])
                break
            self.listbox.insert(tk.END, tasks_text[start:newline_index])
            start = newline_index + 1

    def _clear_inputs(self) -> None:
        self.task_entry.delete(0, tk.END)
        self.priority_spin.set("1")

    def _set_status(self, message: str) -> None:
        self.status_var.set(f"Status: {message}")

    def _error(self, message: str) -> None:
        self.status_var.set(f"Error: {message}")
        messagebox.showerror("LinkedTaskManager", message)
