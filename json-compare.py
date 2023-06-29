#!/usr/bin/env python3
import json
import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="bottom", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

class Application(tk.Tk):
    def __init__(self, folder=None):
        tk.Tk.__init__(self)
        self.title("JSON Viewer")
        self.geometry("800x600")

        self.button = tk.Button(self, text="Open Folder", command=self.load_json_files)
        self.button.grid(row=0, column=0, sticky="new")

        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        self.text_boxes = []
        self.folder_path = folder if folder else ''

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        if self.folder_path:
            self.load_json_files()

    def load_json_files(self):
        self.folder_path = self.folder_path or filedialog.askdirectory()

        for widget in self.scroll_frame.scrollable_frame.winfo_children():
            widget.destroy()
        self.text_boxes = []

        for file in os.listdir(self.folder_path):
            if file.endswith(".json"):
                with open(os.path.join(self.folder_path, file), 'r') as json_file:
                    json_content = json.load(json_file)
                    json_content_pretty = json.dumps(json_content, indent=4)

                    frame = tk.Frame(self.scroll_frame.scrollable_frame)
                    frame.grid(row=0, column=len(self.text_boxes), sticky="nsew")

                    label = tk.Label(frame, text=file)
                    label.pack(side=tk.TOP, fill="x")

                    st = scrolledtext.ScrolledText(frame)
                    st.insert(tk.INSERT, json_content_pretty)
                    st.config(state=tk.DISABLED)
                    st.bind("<Button-1>", self.highlight_lines)
                    st.pack(fill="both", expand=True)

                    self.text_boxes.append(st)

    def highlight_lines(self, event):
        for text_box in self.text_boxes:
            text_box.tag_remove("highlight", 1.0, tk.END)

        clicked_text_box = event.widget
        line, column = clicked_text_box.index(tk.INSERT).split('.')
        line_start = f'{line}.0'
        line_end = f'{line}.end'

        for text_box in self.text_boxes:
            text_box.tag_add("highlight", line_start, line_end)
            text_box.tag_config("highlight", background="yellow")

folder_path = sys.argv[1] if len(sys.argv) > 1 else None
app = Application(folder_path)
app.mainloop()
