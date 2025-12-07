import tkinter as tk
from tkinter import messagebox
from HWHelperInterface import HWHelperInterface
from RewardSystem import RewardSystem
from AssignmentTracker import AssignmentTracker
from datetime import datetime #JUST FOR TESTING

class HomeworkHelperGUI(HWHelperInterface):
    def __init__(self):

        # create main window
        self.root = tk.Tk()

        #initalize RewardSystem
        self.reward_system = RewardSystem()
        self.reward_system.load_image() #Load plant images

        #initalize AssignmentTracker
        self.tracker = AssignmentTracker()
        # Example assignments for testing
        self.tracker.add_assignment("Essay", "English", datetime(2025,1,10,23,59))
        self.tracker.add_assignment("Program", "Python", datetime(2025,1,5,12,0))
        self.tracker.mark_done("Essay")
        self.tracker.in_progress("Program")


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
        """Display rewards window with plant images based on assignment status in a scrollable grid"""
        reward_window = tk.Toplevel(self.root)
        reward_window.title("Rewards")
        reward_window.geometry("800x600")

        # Outer frame to hold canvas and scrollbar
        frame = tk.Frame(reward_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        v_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas inside frame
        canvas = tk.Canvas(frame, bg="white", yscrollcommand=v_scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Connect scrollbar to canvas
        v_scroll.config(command=canvas.yview)

        # Inner frame inside canvas to hold assignment boxes
        inner_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Keep references to images
        reward_window.images = []

        # Get assignments and map status
        assignments = self.tracker.list_assignments()
        status_map = {
            "not started": "not started",
            "in progress": "in progress",
            "done": "complete"
        }

        # Configuration
        columns = 5  # Number of boxes per row
        box_width = 160
        box_height = 200
        padding_x = 20
        padding_y = 20

        # Create boxes in grid
        for idx, assignment in enumerate(assignments):
            row = idx // columns
            col = idx % columns

            # Frame for each assignment
            box = tk.Frame(inner_frame, width=box_width, height=box_height, bg="lightblue", bd=2, relief="solid")
            box.grid(row=row*2, column=col, padx=padding_x, pady=(padding_y, 5))  # row*2 to leave space for label below

            # Plant image
            plant_status = status_map.get(assignment.status.lower(), "not started")
            plant_img = self.reward_system.get_plant_for_status(plant_status)
            reward_window.images.append(plant_img)  # keep reference

            lbl_img = tk.Label(box, image=plant_img, bg="lightblue")
            lbl_img.pack(expand=True)

            # Assignment name below box
            lbl_name = tk.Label(inner_frame, text=assignment.HWname, bg="white", font=("Chalkboard", 10))
            lbl_name.grid(row=row*2 + 1, column=col, pady=(0, padding_y))

        # Update scrollregion
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        #messagebox.showinfo("Rewards", "This feature will implement a reward system for completing assignments and achieving GPA milestones.")

if __name__ == "__main__":
    HomeworkHelperGUI()

