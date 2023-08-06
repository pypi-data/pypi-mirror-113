from .command import *


class CommandPSD4(Command):
    def __init__(self, type):
        super().__init__(type)
        self.resolution_mode = 0

    def setSyringeMode(self, mode: int):
        cmd = super().setSyringeMode(mode)

        if mode == 0:
            self.resolution_mode = mode
            self.steps = 3000

        if mode == 1:
            self.resolution_mode = mode
            self.steps = 24000
        print("set syringe mode for PSD 4")
        return cmd

    def absolutePosition(self, value: int):
        # absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        bResult = False
        cmd: str = 'A'

        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 absolute position command!")
            cmd = 'cmdError'
        return cmd

    def absolutePositionWithReadyStatus(self, value: int):
        # absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'a'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 absolute position with ready status command!")
            cmd = 'cmdError'
        return cmd

    def relativePickup(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'P'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 relative pickup command!")
            cmd = 'cmdError'
        return cmd

    def relativePickupWithReadyStatus(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'p'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 relative pickup with ready status command!")
            cmd = 'cmdError'
        return cmd

    def relativeDispense(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'D'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 relative dispense command!")
            cmd = 'cmdError'
        return cmd

    def relativeDispenseWithReadyStatus(self, value: int):
        # number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'd'
        if self.checkValueInInterval(value, 3000, 24000):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 relative dispense with ready status command!")
            cmd = 'cmdError'
        return cmd

    def returnSteps(self, value: int):
        # Return Steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
        cmd: str = 'K'
        if self.checkValueInInterval(value, 100, 800):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 return steps command!")
            cmd = 'cmdError'
        return cmd

    def backoffSteps(self, value: int):
        # Back-off Steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000
        cmd: str = 'k'
        if self.checkValueInInterval(value, 200, 1600):
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 backoff steps command!")
            cmd = 'cmdError'
        return cmd

    """
        Motor Commands
    """
    def standardHighResolutionSelection(self, mode: int):
        # x=0 for standard resolution mode
        # x=1 for high resolution mode
        cmd: str = 'N'
        if mode == 0 or mode == 1:
            cmd += str(mode)
            self.resolution_mode = mode
            print("Resolution mode set on: " + str(mode) + " using PSD4 st/hg resolution selection")
        else:
            cmd = 'cmdError'
            print("Wrong parameter value for standard/high resolution selection command!")
        return cmd

    def setStartVelocity(self, value: int):
        cmd: str = 'v'
        if 50 <= value <= 1000:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 start velocity command!")
            cmd = 'cmdError'
        return cmd

    def setMaximumVelocity(self, value: int):
        cmd: str = 'V'
        if 2 <= value <= 5800:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 set maximum velocity command!")
            cmd = 'cmdError'
        return cmd

    def stopVelocity(self, value: int):
        cmd: str = 'c'
        if 50 <= value <= 2700:
            cmd += str(value)
        else:
            print("Invalid value " + str(value) + " for PSD4 stop velocity command!")
            cmd = 'cmdError'
        return cmd

    def syringeHomeSensorStatusQuery(self):
        return QueryCommandsEnumeration.SYRINGE_HOME_SENSOR_STATUS.value