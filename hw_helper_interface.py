from abc import ABC, abstractmethod

class HWHelperInterface(ABC):
    @abstractmethod
    def gpaCalculator(self):
        """This method should calculate the GPA given the grades of each class."""
        pass

    @abstractmethod
    def assignmentTracker(self):
        """This method should track each class's assignments, their weight and points, the due dates, and whether or not they are completed."""
        pass

    @abstractmethod
    def whatIf(self):
        """This method should allow the user to input hypothetical grades and assignments for their classes and see how it would affect their overall GPA."""
        pass

    @abstractmethod
    def rewardSystem(self):
        """This method should implement a reward system for completing assignments and achieving certain GPA milestones."""
        pass