from gui import TaskHero
from tkinter import Tk

def main():
    root = Tk()
    app = TaskHero(root)
    root.geometry('400x420')
    root.mainloop()

if __name__ == "__main__":
    main()
