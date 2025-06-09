import tkinter as tk
from view.main_view import MainView
from model.banco import Banco
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from banco_dados import criar_banco

if __name__ == "__main__":
    criar_banco()
    root = tk.Tk()
    app = MainView(root)
    root.mainloop()