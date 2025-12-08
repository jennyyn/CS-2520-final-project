import tkinter as tk
from tkinter import messagebox
from datetime import datetime #JUST FOR TESTING

from HWHelperInterface import HWHelperInterface
from RewardSystem import RewardSystem
from AssignmentTracker import AssignmentTracker, Assignment
from gpa_calculator import GPACalculator
from course import Course

# COLOR PALLETTE
COLOR_BG_MAIN = "#F6F7FB"   # soft white background
COLOR_PANEL = "#A6B3FF"     # pastel periwinkle panels
COLOR_TITLE = "#3E2DBB"     # deep blue-purple title
COLOR_BUTTON = "#4A5DF7"    # bright blue buttons
COLOR_BUTTON_HOVER = "#3E2DBB"
COLOR_TEXT = "#1E1E2F"      # dark neutral text

COLOR_SUCCESS = "#7CF3D0"   # mint
COLOR_SUCCESS_ALT = "#3AE8A9"



class HomeworkHelperGUI(HWHelperInterface):
    def __init__(self):

        # create main window
        self.root = tk.Tk()
        self.root.title("Homework Helper")
        self.root.geometry("900x600")
        self.root.configure(bg=COLOR_BG_MAIN)

        #initalize RewardSystem
        self.reward_system = RewardSystem()
        self.reward_system.load_image() #Load plant images

        #initalize AssignmentTracker
        self.tracker = AssignmentTracker()

        # initialize GPACalculator
        self.gpaCalc = GPACalculator()

        # Example assignments for testing
        self.tracker.add_assignment("Essay", "English", datetime(2025,1,10,23,59))
        self.tracker.add_assignment("Program", "Python", datetime(2025,1,5,12,0))
        self.tracker.mark_done("Essay")
        self.tracker.in_progress("Program")

        # GUI components
        self.build_header()
        self.build_nav()
        self.build_dashboard()

        self.refresh_dashboard()
        self.root.mainloop()


    # Styling helpers
    def style_button(self, btn: tk.Button):
        btn.configure(
            bg=COLOR_BUTTON,
            fg="white",
            activebackground=COLOR_BUTTON_HOVER,
            activeforeground="white",
            font=("Helvetica", 12, "bold"),
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2"
        )

        def on_enter(e):
            btn.configure(bg=COLOR_BUTTON_HOVER)

        def on_leave(e):
            btn.configure(bg=COLOR_BUTTON)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def card_frame(self, parent):
        frame = tk.Frame(parent, bg=COLOR_PANEL, bd=1, relief="solid")
        return frame
    

    # Top header
    def build_header(self):
        header = tk.Frame(self.root, bg=COLOR_BG_MAIN)
        header.pack(fill="x", pady=(10, 5))

        tk.Label(
            header,
            text="Homework Helper Dashboard",
            font=("Helvetica", 26, "bold"),
            fg = COLOR_TITLE,
            bg = COLOR_BG_MAIN
        ).pack(side="left", padx=20)

        
    # Navigation panel
    def build_nav(self):
        nav = tk.Frame(self.root, bg=COLOR_BG_MAIN)
        nav.pack(fill="x", pady=(0, 10))

        # buttons across top
        nav_buttons = [
            ("GPA Calculator", self.gpaCalculator),
            ("Assignment Tracker", self.assignmentTracker),
            ("What If... Tool", self.whatIf),
            ("Rewards Garden", self.rewardSystem)
        ]

        for text, command in nav_buttons:
            btn = tk.Button(nav, text=text, command=command)
            self.style_button(btn)
            btn.pack(side="left", padx=10)


    # Dashboard Layout
    def build_dashboard(self):
        self.dashboard = tk.Frame(self.root, bg=COLOR_BG_MAIN)
        self.dashboard.pack(fill="both", expand=True, padx=20, pady=10)

        self.dashboard.columnconfigure(0, weight=3)
        self.dashboard.columnconfigure(1, weight=2)
        self.dashboard.rowconfigure(0, weight=1)

        # Left: Upcoming Assignments
        self.card_upcoming = self.card_frame(self.dashboard)
        self.card_upcoming.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=5)

        tk.Label(
            self.card_upcoming,
            text="Upcoming Assignments",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TITLE
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.upcoming_list_frame = tk.Frame(self.card_upcoming, bg=COLOR_PANEL)
        self.upcoming_list_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Right: Overview
        self.card_overview = self.card_frame(self.dashboard)
        self.card_overview.grid(row=0, column=1, sticky="nsew", padx=(10,0), pady=5)

        tk.Label(
            self.card_overview,
            text="Overview",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TITLE
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.lbl_gpa_overview = tk.Label(
            self.card_overview
            , text="GPA: --"
            , font=("Helvetica", 14)
            , bg=COLOR_PANEL
            , fg=COLOR_TEXT
        )
        self.lbl_gpa_overview.pack(anchor="w", padx=15, pady=5)

        self.lbl_assignments_overview = tk.Label(
            self.card_overview
            , text="Assignments: --"
            , font=("Helvetica", 14)
            , bg=COLOR_PANEL
            , fg=COLOR_TEXT
        )
        self.lbl_assignments_overview.pack(anchor="w", padx=15, pady=5)

    # Refresh upcoming assignments and GPA
    def refresh_dashboard(self):
        
        # clear upcoming list
        for widget in self.upcoming_list_frame.winfo_children():
            widget.destroy()

        assignments = self.tracker.list_assignments()

        if not assignments:
            tk.Label(
                self.upcoming_list_frame,
                text="No upcoming assignments!",
                font=("Helvetica", 12),
                bg=COLOR_PANEL,
                fg=COLOR_TEXT
            ).pack(anchor="w", pady=5)

        else:
            # sort by deadline
            assignments.sort(key=lambda a: a.deadline)

            for a in assignments:
                frame = tk.Frame(self.upcoming_list_frame, bg=COLOR_PANEL)
                frame.pack(fill="x", pady=2)

                lbl_name = tk.Label(
                    frame,
                    text=a.HWname,
                    font=("Helvetica", 12, "bold"),
                    bg=COLOR_PANEL,
                    fg=COLOR_TEXT
                )
                lbl_name.pack(side="left")

                lbl_deadline = tk.Label(
                    frame,
                    text=a.deadline.strftime("%Y-%m-%d %H:%M"),
                    font=("Helvetica", 12),
                    bg=COLOR_PANEL,
                    fg=COLOR_TEXT
                )
                lbl_deadline.pack(side="right")

         # GPA Overview
        gpa = self.gpaCalc.calculate_gpa()
        if self.gpaCalc.get_courses():
            self.lbl_gpa_overview.config(text=f"GPA: {gpa:.2f}")
        else:
            self.lbl_gpa_overview.config(text="GPA: --")

        # Assignment Stats
        total = len(assignments)
        done = sum(1 for a in assignments if a.status == "done")
        prog = sum(1 for a in assignments if a.status == "in progress")

        self.lbl_assignments_overview.config(
            text=f"Assignments: {done} done, {prog} in progress, {total - done - prog} not started (Total: {total})"
        )

    def gpaCalculator(self):
        messagebox.showinfo("GPA Calculator", "This feature will calculate your GPA based on your grades.")

    def assignmentTracker(self):
        tracker_window = tk.Toplevel(self.root)
        tracker_window.title("Assignment Tracker")
        tracker_window.geometry("700x550")
        tracker_window.configure(bg=COLOR_BG_MAIN)

        card = self.card_frame(tracker_window)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            card,
            text="Assignment Tracker",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TITLE
        ).pack(pady=15)

        
        # Assignment input gui components
        form = tk.Frame(card, bg=COLOR_PANEL)
        form.pack(padx=10, pady=10)

        tk.Label(form, text="Assignment Name:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w")
        entry_name = tk.Entry(form, width=25)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Course:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w")
        entry_subject = tk.Entry(form, width=25)
        entry_subject.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Deadline (YYYY-MM-DD HH:MM):", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=2, column=0)
        entry_deadline = tk.Entry(form, width=25)
        entry_deadline.grid(row=2, column=1, padx=10, pady=5)

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
            self.refresh_dashboard()
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

        # Add and Delete Assignment buttons
        btn_row = tk.Frame(card, bg=COLOR_PANEL)
        btn_row.pack(pady=5)

        btn_add = tk.Button(btn_row, text="Add Assignment", command=add_assignment_gui)
        self.style_button(btn_add)
        btn_add.grid(row=0, column=0, padx=10)

        btn_del = tk.Button(btn_row, text="Delete Assignment", command=delete_assignment_gui)
        self.style_button(btn_del)
        btn_del.grid(row=0, column=1, padx=10)


        # Listbox for assignment display
        list_frame = tk.Frame(tracker_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(list_frame, width=60, height=15, yscrollcommand=scrollbar.set, bg="white", fg=COLOR_TEXT, font=("Helvetica", 12))
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
            self.refresh_dashboard()

        def mark_done():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment.")
                return
            name = self.tracker.list_assignments()[selection[0]].HWname
            self.tracker.mark_done(name)
            refresh_list()
            self.refresh_dashboard()

        btn_frame = tk.Frame(card, bg=COLOR_PANEL)
        btn_frame.pack(pady=10)

        btn_prog = tk.Button(btn_frame, text="Mark In Progress", command=mark_in_progress)
        self.style_button(btn_prog)
        btn_prog.grid(row=1, column=0, padx=10)

        btn_done = tk.Button(btn_frame, text="Mark Done", command=mark_done)
        self.style_button(btn_done)
        btn_done.grid(row=1, column=1, padx=10)


    def whatIf(self):
        """What If... Tool", "This feature will allow you to see how hypothetical grades affect your grade for the course."""

        win = tk.Toplevel(self.root)
        win.title("What If Assignment Grade Simulator")
        win.geometry("500x500")
        win.configure(bg=COLOR_BG_MAIN)

        card = self.card_frame(win)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            card, 
            text="What-If Assignment Simulator", 
            font=("Helvetica", 18, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TITLE
            ).pack(pady=15)
        
        form = tk.Frame(card, bg=COLOR_PANEL)
        form.pack(padx=10, pady=10)
        
        # course name
        tk.Label(form, text="Course / Subject:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w")
        course_entry = tk.Entry(form, width=30)
        course_entry.grid(row=0, column=1, pady=5)

        # assignment name
        tk.Label(form, text="Assignment Name:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w")
        assignment_entry = tk.Entry(form, width=30)
        assignment_entry.grid(row=1, column=1, pady=5)

        # hypothetical grade
        tk.Label(win, text="Hypothetical Grade: ").pack(pady=5)
        tk.Label(form, text="Points Earned:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w")
        points_earned_entry = tk.Entry(form, width=15)
        points_earned_entry.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Points Possible:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=3, column=0, sticky="w")
        max_points_entry = tk.Entry(form, width=15)
        max_points_entry.grid(row=3, column=1, pady=5)

        hypothetical_assignments = []

        def add_hypothetical():
            try:
                hypothetical = {
                    "course": course_entry.get().strip(),
                    "assignment": assignment_entry.get().strip(),
                    "points_earned": float(points_earned_entry.get()),
                    "points_possible": float(max_points_entry.get())
                }
                hypothetical_assignments.append(hypothetical)
                messagebox.showinfo("Success", "Hypothetical assignment added!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for points.")

        def calculate_outcome():
            # gather real assignments for chosen subject
            real_assignments = [
                a for a in self.tracker.assignments
                if a.subject.lower() == course_entry.get().lower()
            ]
            
            # convert them to point totals
            for a in real_assignments:
                if a.pointsEarned is None and a.maxPoints is None:
                    # skip ungraded assignmnents
                    pass

            # add hypothetical assignments
            for h in hypothetical_assignments:
                a = Assignment(
                    name=h["assignment"],
                    subject=h["course"],
                    deadline=datetime.now(),  # placeholder
                    pointsEarned=h["points_earned"],
                    maxPoints=h["points_possible"]
                )
                real_assignments.append(a)

            # calculate new grade
            new_grade = GPACalculator.calc_course_grade(real_assignments)
            if new_grade is not None:
                messagebox.showinfo("What-If Result", f"New calculated grade for {course_entry.get()}: {new_grade:.2f}%")
            else:
                messagebox.showinfo("What-If Result", f"No graded assignments to calculate grade for {course_entry.get()}.")

        btn_add = tk.Button(win, text="Add Hypothetical Assignment", command=add_hypothetical)
        self.style_button(btn_add)
        btn_add.pack(pady=10)

        btn_calc = tk.Button(win, text="Calculate What-If Outcome", command=calculate_outcome)
        self.style_button(btn_calc)
        btn_calc.pack(pady=5)

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

