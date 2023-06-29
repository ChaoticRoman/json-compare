import json
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("JSON Viewer")
        self.geometry("800x600")

        self.button = tk.Button(self, text="Open Folder", command=self.load_json_files)
        self.button.pack()

        self.text_boxes = []
        self.folder_path = ''

    def load_json_files(self):
        self.folder_path = filedialog.askdirectory()

        for widget in self.text_boxes:
            widget.pack_forget()
        self.text_boxes = []

        for file in os.listdir(self.folder_path):
            if file.endswith(".json"):
                with open(os.path.join(self.folder_path, file), 'r') as json_file:
                    json_content = json.load(json_file)
                    json_content_pretty = json.dumps(json_content, indent=4)

                    st = scrolledtext.ScrolledText(self)
                    st.insert(tk.INSERT, json_content_pretty)
                    st.config(state=tk.DISABLED)
                    st.bind("<Button-1>", self.highlight_lines)
                    st.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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

app = Application()
app.mainloop()
