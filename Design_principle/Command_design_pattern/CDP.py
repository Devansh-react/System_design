from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class Light:
    def on(self):
        print("Light is ON")

    def off(self):
        print("Light is OFF")


class Fan:
    def on(self):
        print("Fan is ON")

    def off(self):
        print("Fan is OFF")


class LightCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


class FanCommand(Command):
    def __init__(self, fan):
        self.fan = fan

    def execute(self):
        self.fan.on()

    def undo(self):
        self.fan.off()


class RemoteController:
    def __init__(self):
        self.numButtons = 4
        self.buttons = [None] * self.numButtons
        self.buttonPressed = [False] * self.numButtons

    def setCommand(self, idx, cmd):
        if 0 <= idx < self.numButtons:
            self.buttons[idx] = cmd
            self.buttonPressed[idx] = False

    def pressButton(self, idx):
        if 0 <= idx < self.numButtons and self.buttons[idx] is not None:
            if not self.buttonPressed[idx]:
                self.buttons[idx].execute()
            else:
                self.buttons[idx].undo()
            self.buttonPressed[idx] = not self.buttonPressed[idx]
        else:
            print(f"No command assigned at button {idx}")


if __name__ == "__main__":
    livingRoomLight = Light()
    ceilingFan = Fan()

    remote = RemoteController()

    remote.setCommand(0, LightCommand(livingRoomLight))
    remote.setCommand(1, FanCommand(ceilingFan))

    print("--- Toggling Light Button 0 ---")
    remote.pressButton(0)
    remote.pressButton(0)

    print("--- Toggling Fan Button 1 ---")
    remote.pressButton(1)
    remote.pressButton(1)

    print("--- Pressing Unassigned Button 2 ---")
    remote.pressButton(2)