#Assignment tracker, it will ask the user for the assignment name, class subject, due date (time + date), and status (not started, in progress, done). 
#It will then organize assignments by due date, and the user can check off an assignment once it's done.
from datetime import datetime

from datetime import datetime

class Assignment:
    """Components of an assignment"""
    
    def __init__(self, name: str, subject: str, deadline: datetime, status: str = "not started"):
        self.HWname = name
        self.subject = subject
        self.deadline = deadline
        self.status = status


class AssignmentTracker:
    """Tracks and organizes assignments by due date"""
    
    def __init__(self):
        self.assignments = []
    
    def add_assignment(self, HWname: str, subject: str, deadline: datetime, status: str = "not started"):
        """Adds an assignment to the list."""
        new_assignment = Assignment(HWname, subject, deadline, status)
        self.assignments.append(new_assignment)

    def delete_assignment(self, HWname: str) -> bool:
        """Deletes an assignment."""
        for a in self.assignments:
            if a.HWname.lower() == HWname.lower():
                self.assignments.remove(a)
                return True
        return False

    
    def list_assignments(self):
        """Returns assignments sorted by deadline."""
        return sorted(self.assignments, key=lambda a: a.deadline)
    
    def in_progress(self, HWname: str):
        """Marks an assignment as in progress"""
        for a in self.assignments:
            if a.HWname.lower() == HWname.lower():
                a.status ="in progress"
                return True
        return False

    
    def mark_done(self, HWname: str): #Activated by a button in gui?
        """Marks an assignment as done"""
        for a in self.assignments:
            if a.HWname.lower() == HWname.lower():
                a.status = "done"
                return True
        return False