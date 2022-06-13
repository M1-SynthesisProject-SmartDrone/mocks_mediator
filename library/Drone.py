from dataclasses import dataclass
import math


class Drone:
    """This class contains all data related to the drone
    """

    def __init__(self) -> None:
        self.armed: bool = False
        self.recording: bool = False
        self.battery_remaining: int = 50
        self.lat: int = 0
        self.lon: int = 0
        self.alt: int = 500
        self.relative_alt: int = 0
        self.vx: int = 0
        self.vy: int = 0
        self.vz: int = 0
        self.yaw_rotation: int = 0

    def move(self, x=0.0, y=0.0, z=0.0, r=0.0):
        if x != 0.0:
            self.lat += 1 if x > 0.0 else -1
            self.vx = 22 if x > 0.0 else -22
        else:
            self.vx = 0

        if y != 0.0:
            self.lon += 1 if y > 0.0 else -1
            self.vy = 23 if y > 0.0 else -23
        else:
            self.vy = 0

        if z != 0.0:
            mvmnt = 1 if z > 0.0 else -1
            self.alt += mvmnt
            self.relative_alt += mvmnt
            self.vz = 23 if z > 0.0 else -23
        else:
            self.vz = 0
        
        if r != 0.0:
            self.yaw_rotation += 1 if r > 0.0 else -1
            if self.yaw_rotation > 364:
                self.yaw_rotation = 0
            elif self.yaw_rotation < 0:
                self.yaw_rotation = 664

    