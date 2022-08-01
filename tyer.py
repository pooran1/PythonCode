class Tyre():
    def __init__(self,manuf,color:"Black" ,size):
        self.manuf =manuf
        self.color =color
        self.size=size
        
    def run_forward(self):
        print(f"{self.amp} move forward")
    def run_backward(self):
        print(f"{self.amp} move backward")
    
    def describeTyer(self):
        print(f"""
        Manufacturer: {self.manuf}
        Car Color: {self.color}
        car Size:{self.size}
        """)

