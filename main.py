# main.py
import tkinter as tk
from terminal import TerminalApp  # Change the import statement to match your file name

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()
