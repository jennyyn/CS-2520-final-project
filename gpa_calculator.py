from typing import List
from course import Course
from AssignmentTracker import Assignment

class GPACalculator:
    """Manages a list of courses and calculates the GPA."""
    def __init__(self):
        self.courses: List[Course] = []

    def add_course(self, course: Course):
        """Adds a course to the list."""
        self.courses.append(course)

    def calculate_gpa(self) -> float:
        """
        Calculates the GPA based on the added courses.
        Returns 0.0 if no courses have been added.
        """
        total_points = 0.0
        total_credits = 0.0

        for course in self.courses:
            points = course.grade_points
            total_points += points * course.credits
            total_credits += course.credits

        if total_credits == 0:
            return 0.0
        
        return total_points / total_credits

    def get_courses(self) -> List[Course]:
        """Returns the list of added courses."""
        return self.courses
    
    def calc_course_grade(assigments: List[Assignment]) -> float:
        """Calculates the overall grade for a course based on its assignments."""
        earned = 0.0
        possible = 0.0

        for a in assigments:
            if a.points_earned is not None and a.points_possible is not None:
                earned += a.points_earned
                possible += a.points_possible

        if possible == 0:
            return None # no graded assignments
        
        return (earned / possible) * 100
