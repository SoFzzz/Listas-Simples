"""Application bootstrap for LinkedTaskManager."""

import os
import sys
import tkinter as tk


if __package__ in (None, ""):
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    if CURRENT_DIR not in sys.path:
        sys.path.insert(0, CURRENT_DIR)
    from gui import LinkedTaskManagerApp
else:
    from src.gui import LinkedTaskManagerApp


def main() -> None:
    """Start the Tkinter application."""
    root = tk.Tk()
    LinkedTaskManagerApp(root)
    root.mainloop()
