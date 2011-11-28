#Disparador

class Barr:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 100
        self.w = 10
        
    def move(self, x):
        newx = x - (x + 100 - x)/2
        if newx > 20 and newx < 780 - (x + 100 - x):
            self.x = newx
    
    def getPos(self):
        return [self.x, self.y]