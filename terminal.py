# terminal_app.py
import webbrowser
import tkinter as tk
from tkinter import PhotoImage
import subprocess
import os
import glob


class TerminalApp:
    def __init__(self, root):
        self.root = root
        root.title("NovaX Terminal")

        self.current_directory = r"C:\Users\hedia\PycharmProjects\Terminal"
        self.prompt = f"{self.current_directory}> "
        self.command_history = []
        self.history_index = -1


        self.output_text = tk.Text(root, wrap=tk.WORD, height=20)
        self.output_text.pack()
        self.output_text.tag_configure("path_highlighted", foreground="#ff79c6", background="#44475a")
        # Create a frame to hold the buttons on the left
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.LEFT)

        # Create buttons for various actions
        self.help_icon = PhotoImage(file=r"C:\Users\hedia\PycharmProjects\Terminal\help.png")  # Replace with actual path
        self.help_icon = self.help_icon.subsample(2, 2)  # Make the icon half the original size
        self.help_button = tk.Button(button_frame, image=self.help_icon, command=self.show_help,
                                     width=15, height=15, bd=0)
        self.help_button.image = self.help_icon
        self.help_button.grid(row=0, column=0, padx=5, pady=5)

        self.list_icon = PhotoImage(file=r"C:\Users\hedia\PycharmProjects\Terminal\file.png")  # Replace with actual path
        self.list_icon = self.list_icon.subsample(2, 2)  # Make the icon half the original size
        self.list_dir_button = tk.Button(button_frame, image=self.list_icon, command=self.list_directory,
                                         width=15, height=15, bd=0)
        self.list_dir_button.image = self.list_icon
        self.list_dir_button.grid(row=0, column=1, padx=5, pady=5)

        self.run_icon = PhotoImage(file=r"C:\Users\hedia\PycharmProjects\Terminal\code-.png")  # Replace with actual path
        self.run_icon = self.run_icon.subsample(2, 2)  # Make the icon half the original size
        self.run_script_button = tk.Button(button_frame, image=self.run_icon, command=self.run_script,
                                           width=15, height=15, bd=0)
        self.run_script_button.image = self.run_icon
        self.run_script_button.grid(row=0, column=2, padx=5, pady=5)
        # Display welcome message in the terminal output
        welcome_message = "Welcome to NovaX Terminal"
        self.display_output(f"{welcome_message}\n")
        self.input_entry = tk.Entry(root, width=70)
        self.input_entry.pack()
        self.input_entry.bind("<Return>", self.execute_command)
        self.input_entry.bind("<Up>", self.navigate_history)
        self.input_entry.bind("<Down>", self.navigate_history)
        self.input_entry.bind("<Control-d>", self.close_terminal)
        self.input_entry.bind("<Tab>", self.on_tab)  # Bind the tab key to the on_tab method

        self.input_entry.focus_set()  # Set focus on the input entry field
        # Set a custom icon for the application window

        custom_icon_path = r"C:\Users\hedia\OneDrive\Desktop\IT-Projects\Terminal\terminal.ico"# Replace with the actual path to your icon file
        root.iconbitmap(custom_icon_path)

        # Apply the Dracula color scheme with adjustments
        self.output_text.config(bg="#282a36", fg="#f8f8f2",
                                insertbackground="#f8f8f2")  # Background, text, and cursor color
        self.input_entry.config(bg="#f8f8f2", fg="#282a36")  # Input field color

        # Bind Ctrl + Up Arrow and Ctrl + Down Arrow for scrolling
        self.input_entry.bind("<Control-Up>", self.scroll_up)
        self.input_entry.bind("<Control-Down>", self.scroll_down)

    def on_tab(self, event):
        current_text = self.input_entry.get()
        parts = current_text.split()  # Split the text into parts separated by spaces
        last_part = parts[-1] if parts else ""  # Get the last part (current word)

        if last_part.startswith("open") or last_part.startswith("goto"):
            directory_path = os.path.dirname(last_part[5:])  # Extract directory from 'open' or 'goto' argument
            pattern = os.path.join(directory_path, "*") if directory_path else "*"

            matching_items = glob.glob(pattern)
            matching_files = [item for item in matching_items if os.path.isfile(item)]
            matching_dirs = [item for item in matching_items if os.path.isdir(item)]

            suggestions = matching_files + matching_dirs
            if len(suggestions) == 1:
                suggestion = suggestions[0]
                parts[-1] = suggestion
                new_text = " ".join(parts)
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, new_text)
            elif len(suggestions) > 1:
                self.display_output("\n".join(suggestions) + "\n")

    def execute_command(self, event=None):
        command = self.input_entry.get()
        self.display_output(f"{self.prompt}{command}\n", "command")  # Apply "command" tag to entered command
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.input_entry.delete(0, tk.END)
        self.display_output(f"{self.prompt}{command}\n")
        self.input_entry.bind("<Return>", self.execute_command)

        if command == "scrap":
            self.clear_terminal()
        elif command.startswith("cd "):
            self.change_directory(command[3:])
        elif command == "ls":
            self.list_directory()
        elif command == "end":
            self.close_terminal()
        elif command.endswith(".py"):
            self.run_python_script(command)
        elif command.startswith("goto "):
            self.goto_directory(command[5:])
        elif command == "back":
            self.back_directory()
        elif command == "location":
            self.display_output(f"Current directory: {self.current_directory}\n")
        elif command.startswith("open "):
            self.run_command(command[5:])
        elif command == "past":
            self.display_history()
        elif command == "user":  # Handle custom "user" command
            self.display_output("Hedi\n")
        elif command.startswith("run-html "):
            file_path = command.split(" ")[1]
            webbrowser.open(file_path, new=2)
        else:
            self.run_system_command(command)
        self.input_entry.delete(0, tk.END)
    # Add a new method to handle the "open" command
    def run_command(self, filename):
        try:
            result = subprocess.run([filename], shell=True, capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            self.display_output(output)
        except subprocess.TimeoutExpired:
            self.display_output("Execution timed out.\n")
        except Exception as e:
            self.display_output(f"An error occurred: {e}\n")

    def navigate_history(self, event):
        if event.keysym == "Up":
            if self.history_index > 0:
                self.history_index -= 1
        elif event.keysym == "Down":
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1

        if self.history_index >= 0 and self.history_index < len(self.command_history):
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])

    def display_output(self, output, tag=None):
        self.output_text.config(state=tk.NORMAL)
        if tag:
            self.output_text.insert(tk.END, output, tag)
        else:
            output_lines = output.split("\n")
            for line in output_lines:
                if line.startswith(self.current_directory):
                    self.output_text.insert(tk.END, line + "\n", "path_highlighted")
                else:
                    self.output_text.insert(tk.END, line + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def clear_terminal(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

    def change_directory(self, new_directory):
        try:
            os.chdir(new_directory)
            self.current_directory = os.getcwd()
            self.prompt = f"{self.current_directory}> "
        except FileNotFoundError:
            self.display_output(f"Directory not found: {new_directory}\n")

    def list_directory(self):
        directory_contents = os.listdir(self.current_directory)
        self.display_output("\n".join(directory_contents) + "\n")

    def run_python_script(self, script_name):
        try:
            result = subprocess.run(["python", script_name], capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            self.display_output(output)
        except subprocess.TimeoutExpired:
            self.display_output("Execution timed out.\n")
        except Exception as e:
            self.display_output(f"An error occurred: {e}\n")

    def run_system_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            self.display_output(output)
        except subprocess.TimeoutExpired:
            self.display_output("Execution timed out.\n")
        except Exception as e:
            self.display_output(f"An error occurred: {e}\n")

    def close_terminal(self, event=None):
        goodbye_message = "Goodbye"
        self.display_output(f"{goodbye_message}\n")
        self.root.destroy()

    def scroll_up(self, event):
        self.output_text.yview_scroll(-1, "units")
        self.input_entry.focus_set()

    def scroll_down(self, event):
        self.output_text.yview_scroll(1, "units")
        self.input_entry.focus_set()

    def goto_directory(self, new_directory):
        try:
            os.chdir(new_directory)
            self.current_directory = os.getcwd()
            self.prompt = f"{self.current_directory}> "
        except FileNotFoundError:
            self.display_output(f"Directory not found: {new_directory}\n")

    def back_directory(self):
        try:
            os.chdir("..")
            self.current_directory = os.getcwd()
            self.prompt = f"{self.current_directory}> "
        except FileNotFoundError:
            self.display_output("Cannot go back. You are already at the root directory.\n")

    def display_history(self):
        history_output = "\n".join(self.command_history)
        self.display_output(history_output + "\n")

    def show_help(self):
            help_text = """
            Available Commands:
            - help: Display help for the terminal commands.
            - ls: List contents of the current directory.
            - run <script.py>: Run a Python script in the terminal.
            - run-html <file_path> - Run an HTML file in the default web browser
            """
            self.display_output(help_text)

    def list_directory(self):
        directory_contents = os.listdir(self.current_directory)
        self.display_output("\n".join(directory_contents) + "\n")

    def run_script(self):
        script_path = self.input_entry.get()
        if script_path.endswith(".py"):
            self.run_python_script(script_path)
        else:
            self.display_output("Please provide a valid Python script path.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_terminal)
    root.mainloop()
