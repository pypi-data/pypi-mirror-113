import tkinter as tk

from ..config import cfg
from core.reaction import Reaction


class ReactionModule(tk.Frame):
    cfg = {
        "label": {
            "row": 1,
            "column": 1,
            # "font": ("Helvetica", "12")
        },
        "entry": {
            "row": 2,
            "column": 1,
            "columnspan": 2,
        },
        "submit_label": {
            "row": 4,
            "column": 1,
        },
        "submit_btn": {
            "row": 4,
            "column": 2,
        },
        "error": {
            "row": 3,
            "column": 1,
            "columnspan": 2,
        }
    }

    def __init__(self, parent):
        # Parent concerns
        self.parent = parent
        self.parent.bind("<Control-Key-r>", self.submit)

        # Module frame
        self.frame = tk.LabelFrame(parent, text="Reaction Module")

        # Top label
        self.label_data = tk.StringVar()
        self.label = tk.Label(self.frame, textvariable=self.label_data)
        self.label.grid(**self.cfg["label"])

        # Main entry
        self.entry_data = tk.StringVar()
        self.entry = tk.Entry(
            self.frame, textvariable=self.entry_data)
        self.entry.grid(**self.cfg["entry"])

        # Submit
        self.submit_btn = tk.Button(
            self.frame, text="Submit", command=self.submit)
        self.submit_btn.grid(**self.cfg["submit_btn"])

        self.submit_label = tk.Label(
            self.frame, text="(Ctrl + R)")
        self.submit_label.grid(**self.cfg["submit_label"])

        # Error
        self.error_data = tk.StringVar()
        self.error_label = tk.Label(
            self.frame, textvariable=self.error_data, fg="red")
        self.error_label.grid(**self.cfg["error"])

        # For testing purposes
        self.testing_fixture()

    def calc(self):
        value = self.entry_data.get()

        try:
            self.reaction = Reaction(value)
            self.label_data.set(str(self.reaction))
        except ValueError as e:
            self.error_show(e)

    def entry_clear(self):
        self.entry_data.set('')

    def error_clear(self):
        self.error_data.set('')

    def error_show(self, msg):
        # change label_error colour
        self.error_data.set(msg)

    def label_clear(self):
        self.label_data.set('')

    def submit(self, _event=None):
        self.label_clear()
        self.error_clear()
        self.calc()
        self.entry_clear()

    def testing_fixture(self):
        if not cfg.production_mode:
            self.entry_data.set('H2 + O2 -> H2O')
