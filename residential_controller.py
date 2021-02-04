actualCapacity = 0
sensorDoor = False

class Column:
    def __init__(self, _ID, _status, _amountOfFloors, _amountOfElevators):
        self.ID = _ID
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorsList = []
        self.callButtonsList = []
        self.createElevator(_amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    
    def createElevator(self, _amountOfElevators):
        for i in range(_amountOfElevators):
            elevator = Elevator (i + 1, "idle", self.amountOfFloors, 1)
            self.elevatorsList.append(elevator)
        

    def createCallButtons(self, _amountOfFloors):
        callButtonID = 1
        for buttonFloor in range(_amountOfFloors):
            if buttonFloor + 1 < _amountOfFloors:
                callButton = CallButton (callButtonID, "OFF", buttonFloor + 1, "up")
                self.callButtonsList.append(callButton)
                callButtonID += 1            
            elif buttonFloor + 1 > 1:
                callButton = CallButton (callButtonID, "OFF", buttonFloor + 1, "down")
                self.callButtonsList.append(callButton)
                callButtonID += 1


    def requestElevator(self, _floor, _direction):
        elevator = self.findBestElevator(_floor, _direction)
        print("Chosen elevator: " + str(elevator.ID))
        elevator.floorRequestList.append(_floor)
        elevator.sortFloorList()
        elevator.capacityCalculate()
        elevator.movElev(_floor, _direction)

        return elevator 
        


    def findBestElevator(self, _floor, _direction):

        bestElevatorInfo = type('obj', (object,),{'bestElevator': None, 'bestScore': 5, 'referanceGap': 10000000})

        for elevator in self.elevatorsList:
            if _floor == elevator.currentFloor and elevator.status == "stopped" and _direction == elevator.direction:
                bestElevatorInfo = self.checkIfElevatorISBetter(1, elevator, bestElevatorInfo, _floor)            

            elif _floor > elevator.currentFloor  and elevator.direction == "up" and  elevator.direction == _direction:
                bestElevatorInfo = self.checkIfElevatorISBetter(2, elevator, bestElevatorInfo, _floor)
            
            elif _floor < elevator.currentFloor and elevator.direction == "down" and  elevator.direction == _direction:
                bestElevatorInfo = self.checkIfElevatorISBetter(2, elevator, bestElevatorInfo, _floor)
            
            elif elevator.status == "idle":
                bestElevatorInfo = self.checkIfElevatorISBetter(3, elevator, bestElevatorInfo, _floor)
            
            else:
                bestElevatorInfo = self.checkIfElevatorISBetter(4, elevator, bestElevatorInfo, _floor)
            
        
        return bestElevatorInfo.bestElevator

     
    def checkIfElevatorISBetter(self, scoreToCheck, newElevator, bestElevatorInfo, floor):
        if scoreToCheck < bestElevatorInfo.bestScore:
            bestElevatorInfo.bestScore = scoreToCheck
            bestElevatorInfo.bestElevator = newElevator
            bestElevatorInfo.referanceGap = abs(newElevator.currentFloor - floor) 
        elif bestElevatorInfo.bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if bestElevatorInfo.referanceGap > gap:
                bestElevatorInfo.bestScore = scoreToCheck
                bestElevatorInfo.bestElevator = newElevator
                bestElevatorInfo.referanceGap = gap
            
        return bestElevatorInfo

class Elevator:
    def __init__(self, _ID, _status, _amountOfFloors, _currentFloor):
        self.ID = _ID
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.direction = None
        self.currentFloor = _currentFloor
        self.door = Door(_ID, None)
        self.floorRequestButtonsList = []
        self.floorRequestList = []
        self.capacityStatus = None
        self.maxCapacity = 1500
        self.displayCapacity = None
        self.createFloorRequestButton(_amountOfFloors)
        self.sortFloorList()


    def createFloorRequestButton(self, _amountOfFloors):
        floorRequestButtonID = 1
        for buttonFloor in range(_amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonID, "OFF", buttonFloor + 1)
            self.floorRequestButtonsList.append(floorRequestButton)
            floorRequestButtonID += 1


    def requestFloor(self, _floor):
        self.floorRequestList.append(_floor)
        self.sortFloorList()

        destination = self.floorRequestList[0]
        _direction = None
        if self.currentFloor < destination:
            _direction = "up"
        elif self.currentFloor > destination:
            _direction = "down"        

        self.capacityCalculate()
        self.movElev(_floor, _direction)


    def movElev(self, _floor, _direction):
        while self.capacityStatus != "operating":
            self.capacityCalculate()
        
        while len(self.floorRequestList) != 0:
            self.operateDoors("closed")
            if self.door.status == "closed":
                print("Door without obstruction\n")
                print("Status door:" + str(self.door.status) + "\n")
                self.status = "moving"
                if self.currentFloor > _floor:
                    self.direction = "down"
                else:
                    self.direction = "up"
                
                while self.currentFloor != _floor:
                    if self.direction == "up":
                        print("Elevator current floor: " + str(self.currentFloor) + "   ||     Status: " + self.status)
                        self.currentFloor += 1
                    elif self.direction == "down":
                        print("Elevator current floor: " + str(self.currentFloor) + "   ||     Status: " + self.status)
                        self.currentFloor -= 1
                    
                
                print("Elevator current floor: " + str(self.currentFloor) + "   ||     Status: " + self.status + "\n")
                self.status = "stopped"
                self.operateDoors("opened")
                print("Status door:" + str(self.door.status) + "\n")
            
            self.floorRequestList.pop(0)
        
        self.status = "idle"
    

    def sortFloorList(self):
        if self.direction == "up":
            self.floorRequestList = sorted(self.floorRequestList)
        else:
            self.floorRequestList = sorted(self.floorRequestList, reverse = True)


    def capacityCalculate(self):
        if actualCapacity <= self.maxCapacity:
            self.capacityStatus = "operating"
            self.displayCapacity = actualCapacity
            print("\nCapacity display: Safe")

        else:
            self.capacityStatus = "overloaded"
            self.displayCapacity = "Exceeded weight, authorized weight is" + self.maxCapacity + "lbs"
            print(self.displayCapacity)
        
    
    def operateDoors(self, _command):
        if sensorDoor == False:
            self.door.status = _command
        else:
            print("Blocked door")
                    
class CallButton:
    def __init__(self, _ID, _status, _floor, _direction):
        self.ID = _ID
        self.status = _status
        self.floor = _floor
        self.direction = _direction

class FloorRequestButton:
    def __init__(self, _ID, _status, _floor):
        self.ID = _ID
        self.status = _status
        self.floor = _floor

class Door:
    def __init__(self, _ID, _status):
        self.ID = _ID
        self.status = _status


#//=========== initiation ===============\\

def createTest():
    print('Column creation:')
    global column1 
    column1 = Column (1, "running", 10, 2)

    print("New column: ID = " + str(column1.ID) + "  ||  " 
                + "Status: " + column1.status + "  ||  "
                + "Number of Floors: " + str(column1.amountOfFloors) + "  ||  " 
                + "Number of Elevators: " + str(column1.amountOfElevators) + "\n")

    print('Elevators created:')

    print("\nTotal elevators= " + str(len(column1.elevatorsList)))

    
    print("ID = " + str(column1.elevatorsList[0].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[0].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[0].currentFloor) + "  ||  " 
                + "Direction: " + str(column1.elevatorsList[0].direction) + "\n" 
                + "ID = " + str(column1.elevatorsList[1].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[1].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[1].currentFloor) + "  ||  " 
                + "Direction: " + str(column1.elevatorsList[1].direction) + "\n")


#//=========== scenario1 ===============\\

def scenario1():
    createTest()
    print('Scenario 1: ')
    print('Elevator A is idle at floor 2' + '\n' 
            + 'Elevator B is idle at floor 6.' +'\n')

    column1.elevatorsList[0].currentFloor = 2
    column1.elevatorsList[0].status = "idle"

    column1.elevatorsList[1].currentFloor = 6
    column1.elevatorsList[1].status = "idle"

    print("ID = " + str(column1.elevatorsList[0].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[0].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[0].currentFloor) + "\n" 
                + "ID = " + str(column1.elevatorsList[1].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[1].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[1].currentFloor) + "\n")


    print("Request Elevator from floor: 3 and direction: up")

    elevatorSelected = column1.requestElevator(3, "up")

    print("Request Floor: 7")
    elevatorSelected.requestFloor(7)


#//=========== scenario2 ===============\\

def scenario2():
    createTest()
    print('Scenario 2: ')
    print('Elevator A is idle at floor 10' + '\n' 
            + 'Elevator B is idle at floor 3.' + '\n')

    column1.elevatorsList[0].currentFloor = 10
    column1.elevatorsList[0].status = "idle"

    column1.elevatorsList[1].currentFloor = 3
    column1.elevatorsList[1].status = "idle"

    print("ID = " + str(column1.elevatorsList[0].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[0].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[0].currentFloor) + "\n" 
                + "ID = " + str(column1.elevatorsList[1].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[1].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[1].currentFloor) + "\n")


    print("Request Elevator from floor: 1 and direction: up")
    Person1 = column1.requestElevator(1, "up")
    print("Request Floor: 6")
    Person1.requestFloor(6)

    print("2 minutes later, request Elevator from floor: 3 and direction: up")
    Person2 = column1.requestElevator(3, "up")
    print("Request Floor: 5")
    Person2.requestFloor(5)

    print("Finally, request Elevator from floor: 9 and direction: down")
    Person3 = column1.requestElevator(9, "down")
    print("Request Floor: 2")
    Person3.requestFloor(2)


#//=========== scenario3 ===============\\

def scenario3():
    createTest()
    print('Scenario 3: ')
    print("Elevator A is idle at floor 10" + "\n" 
            + "Elevator B is moving from floor 3 to floor 6." + "\n")

    column1.elevatorsList[0].currentFloor = 10
    column1.elevatorsList[0].status = "idle"

    column1.elevatorsList[1].currentFloor = 3
    column1.elevatorsList[1].status = "moving"

    print("ID = " + str(column1.elevatorsList[0].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[0].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[0].currentFloor) + "\n" 
                + "ID = " + str(column1.elevatorsList[1].ID) + "  ||  " 
                + "Status: " + column1.elevatorsList[1].status + "  ||  " 
                + "Current Floor: " + str(column1.elevatorsList[1].currentFloor) + "\n")


    print("Request Elevator from floor: 3 and direction: down")
    Person1 = column1.requestElevator(3, "down")
    print("Request Floor: 2")
    Person1.requestFloor(2)

    column1.elevatorsList[1].currentFloor = 6
    column1.elevatorsList[1].status = "idle"
    column1.elevatorsList[1].direction = "up"

    print("ID = " + str(column1.elevatorsList[1].ID) + "  ||  " 
            + "Status: " + column1.elevatorsList[1].status + "  ||  " 
            + "Current Floor: " + str(column1.elevatorsList[1].currentFloor) + "\n")

    print("5 minutes later, request Elevator from floor: 10 and direction: down")
    Person2 = column1.requestElevator(10, "down")
    print("Request Floor: 3")
    Person2.requestFloor(3)

#scenario1()
#scenario2()
scenario3()