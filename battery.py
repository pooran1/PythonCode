class Battery():
    def __init__(self,manuf, cells,amp):
        self.manuf =manuf
        self.cells =cells
        self.amp =amp
        
    def outPut(self):
        print(f"{self.amp}")
    
    def describeBattery(self):
        print(f"""
        Manufacturer: {self.manuf}
        Number of Cells: {self.cells}
        """)


