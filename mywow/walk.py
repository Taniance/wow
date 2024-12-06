# walk.py
from combat import Combat
from targeting import Targeting
from pynput.keyboard import Controller

class walk:
    def __init__(self, points, region):
        self.points = points
        self.region = region
        self.keyboard = Controller()
        self.screen_recorder = ScreenRecorder()
        self.movement = Movement(points, region, self.keyboard, self.screen_recorder)
        self.combat = Combat(self.keyboard, self.screen_recorder)
        self.targeting = Targeting(self.screen_recorder)

    def execute(self):
        """执行任务"""
        self.movement.walk_smoothly()
        self.combat.fight()
