import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import json
from collections import defaultdict

class JsonViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.json_widgets = []
        self.line_tags = defaultdict(list)
        self.title("JSON Viewer")
        self.geometry("800x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        self.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        self.select_folder()

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    with open(os.path.join(folder_path, file_name)) as json_file:
                        data = json.load(json_file)
                        self.add_tab(file_name, data)

    def add_tab(self, title, data):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)

        text_widget = tk.Text(tab, wrap="word", state="disabled")
        text_widget.pack(expand=True, fill="both")

        text_widget.bind("<Button-1>", self.on_text_click)

        self.insert_json(text_widget, data)

        self.json_widgets.append(text_widget)

    def insert_json(self, text_widget, data):
        json_str = json.dumps(data, indent=4)

        text_widget.configure(state="normal")
        for i, line in enumerate(json_str.split("\n"), start=1):
            tag = f"line{i}"
            text_widget.insert("end", line + "\n", tag)
            self.line_tags[tag].append(text_widget)
        text_widget.configure(state="disabled")

    def on_text_click(self, event):
        widget = event.widget
        index = widget.index("@%s,%s" % (event.x, event.y))
        line = index.split(".")[0]
        tag = f"line{line}"

        self.clear_all_highlights()

        for widget in self.line_tags[tag]:
            widget.tag_config(tag, background="yellow")

    def clear_all_highlights(self):
        for tag in self.line_tags:
            for widget in self.line_tags[tag]:
                widget.tag_config(tag, background="")

    def on_tab_changed(self, event):
        self.clear_all_highlights()


if __name__ == "__main__":
    app = JsonViewer()
    app.mainloop()
