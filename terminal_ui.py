import tkinter as tk
from tkinter.font import Font  # Import Font class from tkinter.font
from tkinter import PhotoImage

class TerminalUI:
    def __init__(self, root):
        self.root = root
        root.title("My Terminal")

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        self.create_output_text()
        self.create_input_entry()
        self.create_buttons()

    def create_output_text(self):
        self.output_text = tk.Text(self.root, wrap=tk.WORD, height=20, bg="#282a36", fg="#f8f8f2",
                                   insertbackground="#f8f8f2")
        self.output_text.tag_configure("path_highlighted", foreground="#ff79c6", background="#44475a")

    def create_input_entry(self):
        bold_font = Font(weight="bold")
        self.input_entry = tk.Entry(self.root, width=70, font=bold_font, bg="#282a36", fg="#f8f8f2")

    def create_buttons(self):
        self.help_icon = PhotoImage(file= r"C:\Users\hedia\PycharmProjects\Terminal\help.png")
        self.list_icon = PhotoImage(file=r"C:\Users\hedia\PycharmProjects\Terminal\file.png")
        self.run_icon = PhotoImage(file=r"C:\Users\hedia\PycharmProjects\Terminal\code-.png")

        self.help_button = self.create_button(self.help_icon, self.show_help)
        self.list_dir_button = self.create_button(self.list_icon, self.list_directory)
        self.run_script_button = self.create_button(self.run_icon, self.run_script)

    def create_button(self, icon, command):
        return tk.Button(self.root, image=icon, command=command, width=30, height=30,
                         bg="#282a36", highlightbackground="#282a36")

    def setup_layout(self):
        self.output_text.pack()
        self.input_entry.pack()

        self.help_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.list_dir_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.run_script_button.pack(side=tk.LEFT, padx=5, pady=5)

    def show_help(self):
        self.display_output("Help button clicked.\n")

    def list_directory(self):
        self.display_output("List Directory button clicked.\n")

    def run_script(self):
        self.display_output("Run Script button clicked.\n")

    def display_output(self, output):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, output)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalUI(root)
    root.mainloop()
