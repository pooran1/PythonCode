from car import Car
from battery import Battery
from tyer import Tyre
class ElectricCar(Car):
    def __init__(self, make, model, year):
 
        super().__init__(make, model, year)
        #super()takes you to the parent class initializer
        self.battery = Battery("Exide",27,200)
        self.tyer=Tyre("service","black_gray","16")
        
        
    def describe_battery(self):
         print("This car has a " + str(self.battery_size) + "-kWh battery.")
    
    def fill_gas_tank(self):
        print("This car doesn't need a gas tank!")