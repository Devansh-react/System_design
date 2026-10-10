from abc import ABC, abstractmethod
from typing import List
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass
    
    
class Light(ABC):
    def switch_on(self):
        print(f"the buld is ON")
        
    def switch_off(self):
        print(f"the buld is OFF")


class Fan(ABC):
    def switch_on(self):
        print(f"the fan is ON")
    def switch_off(self):
        print(f"the fan is OFF")
        
class Light_command(Command):
    def __init__(self,light) -> None:
        self.light = light
        
    def execute(self):
        return self.light.switch_on()
    def undo(self):
        return self.light.switch_off()
    
    
class Fan_command(Command):
    def __init__(self,fan) -> None:
        self.fan = fan
        
    def execute(self):
        return self.fan.switch_on()
    
    def undo(self):
        return self.fan.switch_off()
    
class Remote_Controller(ABC):
    def __init__(self) -> None:
        self.commands: List[Command] = []
        self.status: List[bool] = []
        
    def set_commands(self, id, cmd):
        while len(self.commands) <= id:
            self.commands.append(id)
            self.status.append(False)
        self.commands[id] = cmd
        self.status[id] = False
            
    def press_button(self,id):
        if 0 <= id < len(self.commands):
            if not self.status[id]:
                self.commands[id].execute()
                self.status[id]=True
            else:
                self.commands[id].undo()
                self.status[id]=False
        else:
            print(f"No Command assign on this {id}")
                
def main():
    Light_livin = Light()
    fan_livin = Fan()
    
    Remote_controller = Remote_Controller()
    
    Remote_controller.set_commands(0,Light_command(Light_livin))
    Remote_controller.set_commands(1,Fan_command(fan_livin))
    
    
    Remote_controller.press_button(0)
    Remote_controller.press_button(1)
    
    if __name__ == "__main__":
        main()