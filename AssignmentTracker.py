#Assignment tracker, it will ask the user for the assignment name, class subject, due date (time + date), and status (not started, in progress, done). 
#It will then organize assignments by due date, and the user can check off an assignment once it's done.
from datetime import datetime

from datetime import datetime

class Assignment:
    """Represents a single assignment."""
    
    def __init__(self, name: str, subject: str, deadline: datetime, status: str = "not started"):
        self.HWname = name
        self.subject = subject
        self.deadline = deadline
        self.status = status


class AssignmentTracker:
    """Tracks and organizes assignments by due date."""
    
    def __init__(self):
        self.assignments = []
    
    def add_assignment(self, HWname: str, subject: str, deadline: datetime, status: str = "not started"):
        new_assignment = Assignment(HWname, subject, deadline, status)
        self.assignments.append(new_assignment)
    
    def list_assignments(self):
        """Returns assignments sorted by deadline."""
        return sorted(self.assignments, key=lambda a: a.deadline)
    
    def mark_done(self, HWname: str): #Activated by a button in gui?
        """Marks an assignment as done by name."""
        for a in self.assignments:
            if a.HWname.lower() == HWname.lower():
                a.status = "done"
                return True
        return False

#Terminal output for testing, comment out/delete for final product
tracker = AssignmentTracker()

#Create deadlines
d1 = datetime(2025, 1, 10, 23, 59)
d2 = datetime(2025, 1, 5, 12, 00)

#Add assignments
tracker.add_assignment("Essay", "English", d1)
tracker.add_assignment("Program", "Python", d2)

#Mark one done
tracker.mark_done("Essay")

#Print sorted list
for a in tracker.list_assignments():
    print(a.HWname, "for", a.subject, "due", a.deadline, "\nStatus:", a.status, "\n")
