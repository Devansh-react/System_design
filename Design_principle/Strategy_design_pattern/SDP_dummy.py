from abc import ABC , abstractmethod


class walkablerobot(ABC):
    @abstractmethod
    def walk(self)->None:
        pass
class talkablerobot(ABC):
    @abstractmethod
    def talk(self)->None:
        pass
class flayablerobot(ABC):
    def fly(self)->None:
        pass
    
class Normalwalkable(walkablerobot):
    def walk(self) -> None:
        print("walking normally")
class Notwalkable(walkablerobot):
    def walk(self)->None:
        print("cannot walk")
        
class Normaltalkable(talkablerobot):
    def talk(self)->None:
        print("talking normally")
class Nottalkable(talkablerobot):
    def talk(self)->None:
        print("cannot talk")
        
class Normalflayable(flayablerobot):
    def fly(self)->None:
        print("flying normally")
        
class Notflayable(flayablerobot):
    def fly(self)->None:
        print("cannot fly")
        
        
class Robot(ABC):
    def __init__(self,walkable:walkablerobot,talkable:talkablerobot,flyable:Normalflayable) -> None:
        self.walkable = walkable
        self.talkable = talkable
        self.flyable = flyable
    def walk(self):
        self.walkable.walk()
    def talk(self):
        self.talkable.talk()
    def fly(self):
        self.flyable.fly()
    @abstractmethod
    def projection(self)->None:
        pass

class companion(Robot):
    def projection(self)->None:
        print("displaying friendly companion features")
    
class workere(Robot):
    def projection(self)->None:
        print("displaying worker efficiency stats")
        

def main():
    robot1 = companion(Normalwalkable(),Normaltalkable(),Normalflayable())
    robot2 = workere(Notwalkable(),Normaltalkable(),Notflayable())
    print("-"*50)
    robot1.walk()
    robot1.talk()
    robot1.fly()
    robot1.projection()

    print("-"*50)

    robot2.walk()
    robot2.talk()
    robot2.fly()
    robot2.projection()
    
if __name__ == "__main__":
    main()
    

        
        
        
    
    