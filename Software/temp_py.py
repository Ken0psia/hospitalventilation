



class Thing:
    VARIABLE = 6
    def __init__(self, x):
        self.x = x

    def get(self):
        y = self.x + self.VARIABLE
        return y
    

thing = Thing(x=10)

value = thing.get()
print(value)
