import random
import tkinter as tk
from PIL import Image, ImageTk
from AssignmentTracker import AssignmentTracker

class RewardSystem:
    """Contains Rewards"""
    def __init__(self):
        self.empty = None
        self.half = None
        self.full_plants = []

    def load_image(self):
        self.empty = ImageTk.PhotoImage(Image.open("images/emptyPlant.png").resize((80,120)))
        self.half = ImageTk.PhotoImage(Image.open("images/growingPlant.png").resize((80,120)))
        self.full_plants = [
            ImageTk.PhotoImage(Image.open("images/flower1.png").resize((80,120))),
            ImageTk.PhotoImage(Image.open("images/flower2.png").resize((80,120))),
            ImageTk.PhotoImage(Image.open("images/flower3.png").resize((80,120))),
            ImageTk.PhotoImage(Image.open("images/flower4.png").resize((80,120)))
        ]

    def get_plant_for_status(self, status):
        """Return the appropriate PhotoImage based on assignment status."""
        if status == "not started":
            return self.empty
        elif status == "in progress":
            return self.half
        elif status == "complete" or "graded":
            return random.choice(self.full_plants)
        else:
            return self.empty  # default fallback

