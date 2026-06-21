from abc import ABC , abstractmethod

class oned_figure:
    @abstractmethod
    def area(self)-> float:
        raise NotImplementedError

class twoD_figure(oned_figure):
    @abstractmethod
    def volume(self)-> float:
        raise NotImplementedError
    
    
class square(oned_figure):
    def __init__(self,length: float) -> None:
        self.length = length
        
    def area(self)-> float:
        return self.length**2
    
class reactangle(oned_figure):
    def __init__(self,length: float,breath: float) -> None:
        self.length = length
        self.breath=breath
        
    def area(self)-> float:
        return self.length*self.breath
    
class cube(twoD_figure):
    def __init__(self,length: float) -> None:
        self.length = length
    def volume(self)-> float:
        return self.length**3
    def area(self)-> float:
        return self.length**2

def main()->None:
    Square:oned_figure() = square(10)
    Reactangle = reactangle(6,4)
    Cube = cube(5)
    Square.area();
    Reactangle.area();
    Cube.area();
    Cube.volume();
if __name__=="__main__":
    main();

       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    