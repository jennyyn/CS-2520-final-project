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
        self.root.geometry("500x400")


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
        tracker_window = tk.Toplevel(self.root)
        tracker_window.title("Assignment Tracker")
        tracker_window.geometry("600x500")

        # Title
        tk.Label(tracker_window, text="Assignment Tracker", font=("Helvetica", 16)).pack(pady=10)

        # Assignment input gui components
        form = tk.Frame(tracker_window)
        form.pack(pady=10)

        tk.Label(form, text="Assignment Name:").grid(row=0, column=0)
        entry_name = tk.Entry(form)
        entry_name.grid(row=0, column=1)

        tk.Label(form, text="Subject:").grid(row=1, column=0)
        entry_subject = tk.Entry(form)
        entry_subject.grid(row=1, column=1)

        tk.Label(form, text="Deadline (YYYY-MM-DD HH:MM):").grid(row=2, column=0)
        entry_deadline = tk.Entry(form)
        entry_deadline.grid(row=2, column=1)

        # Add new assignment
        def add_assignment_gui():
            name = entry_name.get().strip()
            subject = entry_subject.get().strip()
            deadline_text = entry_deadline.get().strip()

            if not name or not subject or not deadline_text:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d %H:%M")
            except:
                messagebox.showerror("Error", "Deadline must be in format YYYY-MM-DD HH:MM")
                return

            self.tracker.add_assignment(name, subject, deadline)
            refresh_list()
            messagebox.showinfo("Success", "Assignment added!")

        # Delete assignment from list
        def delete_assignment_gui():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment to delete.")
                return

            index = selection[0]
            assignment = self.tracker.list_assignments()[index]

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete assignment '{assignment.HWname}'?"
            )
            if confirm:
                # Remove from internal list
                self.tracker.assignments.remove(assignment)
                refresh_list()
                messagebox.showinfo("Deleted", "Assignment removed.")

        # Add/Delete buttons beside each other
        tk.Button(form, text="Add Assignment", command=add_assignment_gui).grid(row=3, column=0, pady=10)
        tk.Button(form, text="Delete Assignment", command=delete_assignment_gui).grid(row=3, column=1, pady=10)

        # Listbox for assignment display
        list_frame = tk.Frame(tracker_window)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(list_frame, width=60, height=15, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Update the listbox in gui
        def refresh_list():
            listbox.delete(0, tk.END)
            for a in self.tracker.list_assignments():
                line = f"{a.HWname} | {a.subject} | Due: {a.deadline.strftime('%Y-%m-%d %H:%M')} | Status: {a.status}"
                listbox.insert(tk.END, line)

        refresh_list()

        # Status buttons
        def mark_in_progress():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment.")
                return
            name = self.tracker.list_assignments()[selection[0]].HWname
            self.tracker.in_progress(name)
            refresh_list()

        def mark_done():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment.")
                return
            name = self.tracker.list_assignments()[selection[0]].HWname
            self.tracker.mark_done(name)
            refresh_list()

        btn_frame = tk.Frame(tracker_window)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Mark In Progress", command=mark_in_progress).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Mark Done", command=mark_done).grid(row=0, column=1, padx=10)


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

