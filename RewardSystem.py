import tkinter as tk
from PIL import Image, ImageTk
from AssignmentTracker import AssignmentTracker

class RewardSystem:
    """Rewards of Assignment"""
    def __init__(self):
        self.empty = ImageTk.PhotoImage(Image.open("emptyPlant.png"))
        self.half = ImageTk.PhotoImage(Image.open("growingPlant.png"))

        self.full_plants = [
            ImageTk.PhotoImage(Image.open("flower1.png")),
            ImageTk.PhotoImage(Image.open("flower2.png")),
            ImageTk.PhotoImage(Image.open("flower3.png")),
            ImageTk.PhotoImage(Image.open("flower4.png"))
        ]

