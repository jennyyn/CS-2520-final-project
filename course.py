class Course:
    """Represents a single course with a name, grade, and credits."""
    def __init__(self, name: str, grade: str, credits: float):
        self.name = name
        self.grade = grade.upper()
        self.credits = credits

    @property
    def grade_points(self) -> float:
        """Converts the letter grade to a point value."""
        grade_map = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }
        # If the grade is not in the map, default to 0.0
        return grade_map.get(self.grade, 0.0)

    def __str__(self):
        return f"{self.name}: {self.grade} ({self.credits} credits)"
