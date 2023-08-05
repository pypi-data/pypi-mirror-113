import tkinter as tk
import tkinter.font as tkFont


class Config:

    # Production state disables all testing fixture
    production_mode = True

    def __init__(self):

        #self.fonts =  {}

        self.subs_row = 1
        self.subs_col = 2
        self.react_row = 2
        self.react_col = 2
        self.widgets_col = 1
        self.label_row = 1
        self.entry_row = self.label_row + 1,
        self.submit_row = self.label_row + 2
        self.shortcut_label_row = self.label_row + 3
        self.label_error_row = self.label_row + 4

        self.padx = 20
        self.pady = 20

        self.ipadx = 8
        self.ipady = 8

        # Main Window

       # self.fontSettings()


def fontSettings(fontsize=12):
    default_font = tkFont.nametofont("TkDefaultFont")
    text_font = tkFont.nametofont("TkTextFont")
    fixed_font = tkFont.nametofont("TkFixedFont")
    text_font = tkFont.Font(family="Helvetica", size=36, weight="bold")
    heading_font = tkFont.nametofont("TkHeadingFont")

    default_font.configure(size=fontsize)
    text_font.configure(size=fontsize)
    fixed_font.configure(size=fontsize)
    heading_font.configure(size=20)


cfg = Config()
