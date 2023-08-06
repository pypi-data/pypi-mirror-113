import tkinter as tk
import tkinter.font as tkFont

from .config import cfg, fontSettings
from .modules.reaction import ReactionModule
from .modules.substance import SubstanceModule


class MainApplication(tk.Frame):

    cfg = {
        "label": {
            'row': 1,
            'column': 1,
            'sticky': tk.N
        },
        "substance_module": {
            'row': 2,
            'column': 1,
            'padx':  cfg.padx,
            'pady': cfg.pady,
            'ipadx':  20,
            'ipady': 10,
            'columnspan': 2,
        },
        "react_module": {
            'row': 3,
            'column': 1,
            'padx':  cfg.padx,
            'pady': cfg.pady,
            'ipadx':  cfg.ipadx,
            'ipady': cfg.ipady,
            'columnspan': 2
        },
        "close_btn": {
            'row': 4,
            'column': 2,
            'sticky': tk.N
        }
    }

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Parent concerns
        self.parent = parent
        self.parent.bind("<Escape>", self.close)

        self.label = tk.Label(
            text="Chemical calculators", font=("Helvetica", "20"))
        self.label.grid(**self.cfg['label'])

        substance_module = SubstanceModule(parent)
        substance_module.frame.grid(**self.cfg['substance_module'])

        reaction_module = ReactionModule(parent)
        reaction_module.frame.grid(**self.cfg['react_module'])

        self.close_button = tk.Button(parent, text="Close", command=self.close)
        self.close_button.grid(**self.cfg['close_btn'])

    def close(self, _event=None):
        self.parent.quit()


def start_gui():
    root = tk.Tk()
    fontSettings()
    MainApplication(root)
    root.mainloop()
