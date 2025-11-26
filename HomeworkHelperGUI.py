import tkinter as tk
from tkinter import messagebox
from HWHelperInterface import HWHelperInterface

class HomeworkHelperGUI(HWHelperInterface):
    def __init__(self):

        # create main window
        self.root = tk.Tk()
        self.root.title("Homework Helper")
        self.root.geometry("400x300")

        # label
        title = tk.Label(self.root, text="Homework Helper", font=("Helvetica", 18))
        title.pack(pady=15)
        
        # buttons
        gpa = tk.Button(self.root, text="GPA Calculator", command=self.gpaCalculator)
        gpa.pack(pady=20)

        assignments = tk.Button(self.root, text="Assignment Tracker", command=self.assignmentTracker)
        assignments.pack(pady=20)

        whatIfs = tk.Button(self.root, text="What If... Tool", command=self.whatIf)
        whatIfs.pack(pady=20)

        rewards = tk.Button(self.root, text="Rewards", command=self.rewardSystem)
        rewards.pack(pady=20)

        # start GUI loop
        self.root.mainloop()

    def gpaCalculator(self):
        messagebox.showinfo("GPA Calculator", "This feature will calculate your GPA based on your grades.")

    def assignmentTracker(self):
        messagebox.showinfo("Assignment Tracker", "This feature will help you track your assignments.")

    def whatIf(self):
        messagebox.showinfo("What If... Tool", "This feature will allow you to see how hypothetical grades affect your GPA.")

    def rewardSystem(self):
        messagebox.showinfo("Rewards", "This feature will implement a reward system for completing assignments and achieving GPA milestones.")

if __name__ == "__main__":
    HomeworkHelperGUI()

