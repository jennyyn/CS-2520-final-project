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
        self.root.geometry("1800x1000")
        self.root.configure(bg=COLOR_BG_MAIN)

        #initalize RewardSystem
        self.reward_system = RewardSystem()
        self.reward_system.load_image() #Load plant images

        #initalize AssignmentTracker
        self.tracker = AssignmentTracker()

        # initialize GPACalculator
        self.gpaCalc = GPACalculator()

        # Example assignments for testing
        self.tracker.add_assignment("Essay", "English", datetime(2025,1,10,23,59), points_possible=100)
        self.tracker.add_assignment("Program", "Python", datetime(2025,1,5,12,0), points_possible=150)
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

        assignments = [a for a in self.tracker.list_assignments()]
        compAssignments = [a for a in self.tracker.list_assignments() if a.status in ("done", "graded")]
        progAssignments = [a for a in self.tracker.list_assignments() if a.status not in ("done", "graded")]

        if not progAssignments:
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

            for a in progAssignments:
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
        done = sum(1 for a in compAssignments if a.status == "done" or "graded")
        prog = sum(1 for a in progAssignments if a.status == "in progress")

        self.lbl_assignments_overview.config(
            text=f"Assignments: {done} done, {prog} in progress, {total - done - prog} not started (Total: {total})"
        )

    def gpaCalculator(self):
        """GPA Calculator Window"""
        gpa_window = tk.Toplevel(self.root)
        gpa_window.title("GPA Calculator")
        gpa_window.geometry("600x700")
        gpa_window.configure(bg=COLOR_BG_MAIN)

        card = self.card_frame(gpa_window)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            card,
            text="GPA Calculator",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TITLE
        ).pack(pady=15)

        # Input Form
        form = tk.Frame(card, bg=COLOR_PANEL)
        form.pack(padx=10, pady=10)

        tk.Label(form, text="Course Name:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w")
        entry_course = tk.Entry(form, width=20)
        entry_course.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Credits:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w")
        entry_credits = tk.Entry(form, width=10)
        entry_credits.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Grade (Letter):", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w")
        
        entry_grade = tk.Entry(form, width=10)
        entry_grade.grid(row=2, column=1, padx=5, pady=5)

        # Labels for GPA display
        lbl_current_gpa = tk.Label(
            card, 
            text="Current GPA: 0.00", 
            font=("Helvetica", 16, "bold"), 
            bg=COLOR_PANEL, 
            fg=COLOR_TITLE
        )

        # Listbox
        list_frame = tk.Frame(card, bg=COLOR_PANEL)
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            list_frame, 
            height=8, 
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 12)
        )
        listbox.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        def update_display():
            # refresh listbox
            listbox.delete(0, tk.END)
            for c in self.gpaCalc.get_courses():
                listbox.insert(tk.END, str(c))
            
            # refresh GPA label
            gpa = self.gpaCalc.calculate_gpa()
            lbl_current_gpa.config(text=f"Current GPA: {gpa:.2f}")
            
            # Also refresh the main dashboard GPA if needed
            self.refresh_dashboard()

        def add_course_action():
            c_name = entry_course.get().strip()
            c_credits_str = entry_credits.get().strip()
            c_grade = entry_grade.get().strip()

            if not c_name or not c_credits_str or not c_grade:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                c_credits = float(c_credits_str)
            except ValueError:
                messagebox.showerror("Error", "Credits must be a number.")
                return

            new_course = Course(c_name, c_grade, c_credits)
            self.gpaCalc.add_course(new_course)
            
            # Clear inputs
            entry_course.delete(0, tk.END)
            entry_credits.delete(0, tk.END)
            entry_grade.delete(0, tk.END)
            
            update_display()

        btn_add = tk.Button(form, text="Add Course", command=add_course_action)
        self.style_button(btn_add)
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        lbl_current_gpa.pack(pady=10)

        # Initial Load
        update_display()


    def assignmentTracker(self):
        self.tracker_window = tk.Toplevel(self.root)
        self.tracker_window.title("Assignment Tracker")
        self.tracker_window.geometry("700x550")
        self.tracker_window.configure(bg=COLOR_BG_MAIN)

        card = self.card_frame(self.tracker_window)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label( card, text="Assignment Tracker", font=("Helvetica", 20, "bold"), bg=COLOR_PANEL, fg=COLOR_TITLE).pack(pady=15)

        # Assignment input GUI components
        form = tk.Frame(card, bg=COLOR_PANEL)
        form.pack(padx=10, pady=10)

        tk.Label(form, text="Assignment Name:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=0, column=0, sticky="w")
        entry_name = tk.Entry(form, width=25)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Course:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w")
        entry_subject = tk.Entry(form, width=25)
        entry_subject.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Deadline (YYYY-MM-DD HH:MM):", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w")
        entry_deadline = tk.Entry(form, width=25)
        entry_deadline.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form, text="Points Possible:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=3, column=0, sticky="w")
        entry_points = tk.Entry(form, width=25)
        entry_points.grid(row=3, column=1, padx=10, pady=5)

        # Add new assignment
        def add_assignment_gui():
            name = entry_name.get().strip()
            subject = entry_subject.get().strip()
            deadline_text = entry_deadline.get().strip()
            points_possible_text = entry_points.get().strip()

            if not name or not subject or not deadline_text:
                messagebox.showerror("Error", "All fields are required.")
                self.tracker_window.lift()
                self.tracker_window.focus_force()
                return

            try:
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d %H:%M")
            except:
                messagebox.showerror("Error", "Deadline must be in format YYYY-MM-DD HH:MM")
                self.tracker_window.lift()
                self.tracker_window.focus_force()
                return

            self.tracker.add_assignment(
                name,
                subject,
                deadline,
                points_possible=float(points_possible_text) if points_possible_text else None
            )
            refresh_list()
            self.refresh_dashboard()
            messagebox.showinfo("Success", "Assignment added!")
            self.tracker_window.lift()
            self.tracker_window.focus_force()

        # Delete assignment from list
        def delete_assignment_gui():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment to delete.")
                self.tracker_window.lift()
                self.tracker_window.focus_force()
                return

            index = selection[0]
            assignment = self.tracker.list_assignments()[index]

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete assignment '{assignment.HWname}'?"
            )

            if confirm:
                self.tracker.delete_assignment(assignment.HWname)
                refresh_list()
                self.refresh_dashboard()
                messagebox.showinfo("Deleted", "Assignment removed.")
                self.tracker_window.lift()
                self.tracker_window.focus_force()

        # Listbox for assignment display
        list_frame = tk.Frame(self.tracker_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(list_frame, width=60, height=15, yscrollcommand=scrollbar.set, bg="white", fg=COLOR_TEXT, font=("Helvetica", 12))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        def refresh_list():
            listbox.delete(0, tk.END)
            for a in self.tracker.list_assignments():
                # Show points only if graded
                if a.status.lower() == "graded":
                    points_str = f"{a.points_earned}/{a.points_possible}"
                    grade = a.points_earned/a.points_possible
                else:
                   points_str = ""
                   grade = None

                line = f"{a.HWname} | {a.subject} | Points Possible: {a.points_possible} | Due: {a.deadline.strftime('%Y-%m-%d %H:%M')} | Status: {a.status} {points_str}"
                # If graded, insert as green for passing and red for failing, standard otherwise
                if a.status == "graded" and grade >= .70:
                    listbox.insert(tk.END, line)
                    listbox.itemconfig(tk.END, fg="green")
                elif a.status == "graded" and grade < .70:
                    listbox.insert(tk.END, line)
                    listbox.itemconfig(tk.END, fg="red")
                else:
                    listbox.insert(tk.END, line)

        refresh_list()

        # Status buttons
        def mark_in_progress():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment.")
                self.tracker_window.lift()
                self.tracker_window.focus_force()
                return
            name = self.tracker.list_assignments()[selection[0]].HWname
            self.tracker.in_progress(name)
            refresh_list()
            self.refresh_dashboard()

        def mark_done():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment.")
                self.tracker_window.lift()
                self.tracker_window.focus_force()
                return
            name = self.tracker.list_assignments()[selection[0]].HWname
            self.tracker.mark_done(name)
            refresh_list()
            self.refresh_dashboard()

        def mark_graded():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select one", "You must select an assignment.")
                self.tracker_window.lift()
                self.tracker_window.focus_force()
                return
        
            assignment = self.tracker.list_assignments()[selection[0]]
            name = assignment.HWname

            popup = tk.Toplevel(self.tracker_window)
            popup.title(f"Grade Assignment: {name}")
            popup.geometry("300x150")
            popup.configure(bg=COLOR_BG_MAIN)

            tk.Label(popup, text=f"Enter points for '{name}':", font=("Helvetica", 12), bg=COLOR_BG_MAIN, fg=COLOR_TEXT).pack(pady=10)
            entry_earned = tk.Entry(popup, width=15)
            entry_earned.pack()

            def submit_grade():
                try:
                    points_earned = float(entry_earned.get())
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number for points earned.")
                    return

                if assignment.points_possible is None:
                    messagebox.showerror("Error", "This assignment has no 'points possible' set.")
                    return

                self.tracker.mark_graded(name, points_earned, assignment.points_possible)
                popup.destroy()
                refresh_list()
                self.refresh_dashboard()
                messagebox.showinfo("Success", "Assignment marked as graded.")
                self.tracker_window.lift()
                self.tracker_window.focus_force()

            submit_btn = tk.Button(popup, text="Submit Grade", command=submit_grade)
            self.style_button(submit_btn)
            submit_btn.pack(pady=10)

        # Buttons row
        btn_row = tk.Frame(card, bg=COLOR_PANEL)
        btn_row.pack(pady=10)

        btn_add = tk.Button(btn_row, text="Add Assignment", command=add_assignment_gui)
        self.style_button(btn_add)
        btn_add.grid(row=0, column=0, padx=10, pady=5)

        btn_del = tk.Button(btn_row, text="Delete Assignment", command=delete_assignment_gui)
        self.style_button(btn_del)
        btn_del.grid(row=0, column=1, padx=10, pady=5)

        btn_prog = tk.Button(btn_row, text="Mark In Progress", command=mark_in_progress)
        self.style_button(btn_prog)
        btn_prog.grid(row=1, column=0, padx=10)

        btn_done = tk.Button(btn_row, text="Mark Done", command=mark_done)
        self.style_button(btn_done)
        btn_done.grid(row=1, column=1, padx=10)

        btn_graded = tk.Button(btn_row, text="Mark Graded", command=mark_graded)
        self.style_button(btn_graded)
        btn_graded.grid(row=1, column=2, padx=10)



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
        tk.Label(form, text="Hypothetical Assignment Name:", bg=COLOR_PANEL, fg=COLOR_TEXT).grid(row=1, column=0, sticky="w")
        assignment_entry = tk.Entry(form, width=30)
        assignment_entry.grid(row=1, column=1, pady=5)

        # hypothetical grade
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
                    "course": course_entry.get().strip().lower(),
                    "assignment": assignment_entry.get().strip(),
                    "points_earned": float(points_earned_entry.get()),
                    "points_possible": float(max_points_entry.get())
                }
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for points.")
                return
            
            if not hypothetical["assignment"] or not hypothetical["course"]:
                messagebox.showerror("Error", "Course or Assignment Name cannot be empty.")
                return
            
            hypothetical_assignments.append(hypothetical)
            messagebox.showinfo("Added", f"Hypothetical assignment '{hypothetical['assignment']}' added for course '{hypothetical['course']}'.")

        def calculate_outcome():
            course_name = course_entry.get().strip().lower()

            # gather real graded assignments for chosen subject
            real_assignments = [
                a for a in self.tracker.assignments
                if a.subject.lower() == course_name
                and a.points_earned is not None
                and a.points_possible is not None
            ]

            # add hypothetical assignments
            for h in hypothetical_assignments:
                a = Assignment(
                    name=h["assignment"],
                    subject=h["course"],
                    deadline=datetime.now(),  # placeholder
                    points_possible=h["points_possible"]
                )
                a.points_earned = h["points_earned"]
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

