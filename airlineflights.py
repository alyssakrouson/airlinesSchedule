#Alyssa Krouson
#CSC 110 - Fall 2021
#Programing Project
#Dec 13, 2021

#Airline Flight Scheduling
# Allow user to ask various questions about the results
def openFile():
    goodFile = False
    while goodFile == False:
        fname = input("Please enter a file name: ")
        try:
            dataFile = open(fname, 'r')
            goodFile = True
        except IOError:
            print("Invalid file name try again ...")
    return dataFile

#remove dollar sign from the price
def removeDollar(price):
    newPrice = ""
    for i in range(1,len(price)):
        newPrice = newPrice + price[i]
    return newPrice

#gets all the info from the file and puts everything into lists
def getInfo():
    dataFile = openFile()
    
    airlineList = []
    flightNumList = []
    depTimeList = []
    arrTimeList = []
    priceList = []


    line = dataFile.readline()
    line = line.strip()
    while line != '':
        lines,flightnum,deptime,arrtime,price = line.split(',')
        airlineList.append(lines)
        flightNumList.append(flightnum)
        depTimeList.append(deptime)
        arrTimeList.append(arrtime)
        priceList.append(price)
        line = dataFile.readline()
        line = line.strip()
    dataFile.close()
    
    newPriceList = []
    for i in range(len(priceList)):
        newPriceList.append(removeDollar(priceList[i]))
    
    return airlineList,flightNumList,depTimeList,arrTimeList,newPriceList

#finds the flight
def findFlight(airlineList,flightNumList):
    #checks if the flight airline name is in the list
    goodName = False
    while goodName == False:
        flightName = input("Enter airline name: ")
        for i in range(len(airlineList)):
            if flightName == airlineList[i]:
                goodName = True
        if goodName == False:
            print("Invalid input -- try again")
    

    #checks if the input is a number
    goodNum = False
    while goodNum == False:
        try:
            flightNum = int(input("Enter flight number: "))
            goodNum = True
        except ValueError:
            print("Invalid input -- try again")

    #finds the index of the flight number and returns it
    flightNum = str(flightNum)
    flightIndex = -1
    for i in range(len(flightNumList)):
        if flightNum == flightNumList[i]:
            flightIndex = i

    return flightIndex

#calculates the time between the departure and arrive time
def timeCalc(start,end):
    #takes either the first num or first 2 nums
    hours = start[0]
    if start[1] != ":":
        hours = hours + start[1]
    #takes the last 2 nums
    mins = start[-2]+start[-1]
    if mins == "00":
        mins ="0"

    #makes the hours and mins into integers
    hours = int(hours)
    mins = int(mins)

    #same for arrive time
    hours2 = end[0]
    if end[1] != ":":
        hours2 = hours2 + end[1]
    mins2 = end[-2]+end[-1]
    if mins2 == "00":
        mins2 ="0"
    hours2 = int(hours2)
    mins2 = int(mins2)

    #calcs the difference in time
    diff = 60 - mins
    hDiff = (hours2 - hours - 1)*60

    time = hDiff + diff + mins2

    return time

#asks the user for a flight duration and resturns a list of flights less than that duration
def findShorter(depTimeList,arrTimeList):
    shortIndexList = []
    #checks input is num
    goodMin = False
    while goodMin == False:
        try:
            flightTime = int(input("Enter maximum duration (in minutes): "))
            goodMin = True
        except ValueError:
            print("Entry must be a number")

    #calcs time for for each flight and adds to list if less than given mins
    for i in range(len(depTimeList)):
        if timeCalc(depTimeList[i],arrTimeList[i]) < flightTime:
            shortIndexList.append(i)
    
    return shortIndexList


#asks a user for a price threshold and returns a list of flights under the price
def cheapFlights(airlineList,priceList):
    goodName = False
    while goodName == False:
        flightName = input("Enter airline name: ")
        for i in range(len(airlineList)):
            if flightName == airlineList[i]:
                goodName = True
        if goodName == False:
            print("Invalid input -- try again")
            
    cheapestIndex = 0
    #removes $ from string
    cheapest = int(priceList[0])
    #searches list for cheapest amount under the given airline
    for i in range(len(priceList)):
        if int(priceList[i]) < cheapest and airlineList[i] == flightName:
            cheapestIndex = i
    
    return cheapestIndex

#Compares the given time to the depart times in the list
def checkTime(time,departTime):
    goodTime = False

    #converts given time to integers
    timeHours = int(time[0])
    if time[1] != ":":
        timeHours = int(time[0] + time[1])
    timeMins = int(time[-2] + time[-1])

    #converts depart time to integers
    departTimeHours = int(departTime[0])
    if departTime[1] != ":":
        departTimeHours = int(departTime[0] + departTime[1])
    departTimeMins = int(departTime[-2] + departTime[-1])

    #if the depart time is later than given time it returns true
    if timeHours < departTimeHours:
        goodTime = True
    elif timeHours == departTimeHours and timeMins < departTimeMins:
        goodTime = True
        
    return goodTime

#asks the user for a flight time and returns a list of flights after a certain time
def flightTime(depTimeList):
    flightTimesIndexList = []
    time = input("Enter earliest departure time: ")

    #checks if a time is entered
    goodMin = False
    while goodMin == False:
        try:
            timeHours = int(time[0])
            timeHours = int(time[1])
            timeHours = int(time[0]+ time[1])
            timeMins = int(time[-2] + time[-1])
            goodMin = True
            if time[1] == ":":
                goodMin = False
        except ValueError:
            time = input("Invalid time - Try again ")

    #compares all the times in the list to the given time and saves the indexes
    for i in range(len(depTimeList)):
        if checkTime(time,depTimeList[i]) == True:
            flightTimesIndexList.append(i)
            
    return flightTimesIndexList

#Finds the average price of all flights for a given time
def flightAvg(priceList):
    average = 0
    #removes $ and adds up each price
    for i in range(len(priceList)):
        priceList[i] = int(priceList[i])
        average = average + priceList[i]
    #calcs average
    average = round(average/len(priceList),2)
        
    return average

#converts time to total minutes
def convertMins(time):
    mins = 0
    #converts given time to integers
    timeHours = int(time[0])
    if time[1] != ":":
        timeHours = int(time[0] + time[1])
    timeMins = int(time[-2] + time[-1])

    mins = timeHours * 60 + timeMins
        
    return  mins

#sorts by departure time (called later)
def dualSort(minList,airlineList,flightNumList,depTimeList,arrTimeList,priceList):
    for i in range(1, len(depTimeList)):
        save = minList[i]
        save2 = depTimeList[i]
        save3 = airlineList[i]
        save4 = flightNumList[i]
        save5 = arrTimeList[i]
        save6 = priceList[i]
        j = i
        #compares the values but if swapped moves all lists positions according to list 1
        while j > 0 and minList[j - 1] > save:
            # comparison
            minList[j] = minList[j - 1]
            depTimeList[j] = depTimeList[j - 1]
            airlineList[j] = airlineList[j - 1]
            flightNumList[j] = flightNumList[j - 1]
            arrTimeList[j] = arrTimeList[j - 1]
            priceList[j] = priceList[j - 1]
            j = j - 1
	    # swap
        minList[j] = save
        depTimeList[j] = save2
        airlineList[j] = save3
        flightNumList[j] = save4
        arrTimeList[j] = save5
        priceList[j] = save6
        
    return airlineList,flightNumList,depTimeList,arrTimeList,priceList

def sortFlights(airlineList,flightNumList,depTimeList,arrTimeList,priceList):
    #calculates the time as minutes in the day to compare
    minsList = []
    for i in range(len(depTimeList)):
        minsList.append(convertMins(depTimeList[i]))

    #sorts by depature time and shifts others lists
    aLineList,numList,depList,arrList,prices = dualSort(minsList,airlineList,flightNumList,depTimeList,arrTimeList,priceList)

    #sorts info into file
    outName = "time-sorted-flights.csv"
    outFile = open(outName,'w')
    for i in range(len(depList)):
        outFile.write(str(aLineList[i]) + ", " + str(numList[i]) + ", " + str(depList[i]) + ", " + str(arrList[i]) + ", " + "$" + str(prices[i]) + '\n')
    
    return

def getChoice():
    # This function displays the menu of choices for the user
    # It reads in the user's choice and returns it as an integer
    print("")
    print("Please choose one of the following options:")
    print("1 -- Find flight information by airline and flight number")
    print("2 -- Find flights shorter than a specified duration")
    print("3 -- Find the cheapest flight by a given airline")
    print("4 -- Find flight departing after a specified time")
    print("5 -- Find the average price of all flights")
    print("6 -- Write a file with flights sorted by departure time")
    print("7 -- Quit")
    goodChoice = False
    #checks if the input is a number and is between 1 and 7
    while goodChoice == False:
        try:
            choice = int(input("Choice ==> "))
            goodChoice = True
            if choice > 7 or choice < 1:
                print("Entry must be between 1 and 7")
                goodChoice = False
        except ValueError:
            print("Entry must be a number")
        
    return choice

def main():
    # Call the function to get the data from the data file and store the results in three lists
    lineList,fnumList,depTime,arrTime,price = getInfo()
    choice = getChoice()
    #choice = int(choice)
    while choice != 7:
        if choice == 1:
            print("")
            #finds the flight info from the airline and flight #
            flightIndex = findFlight(lineList,fnumList)
            if flightIndex < 0:
                print("Flight not found")
            else:
                print("")
                print("The flight that meets your criteria is:")
                print("")
                print("AIRLINE".ljust(8),"FLT#".ljust(6),"DEPART".rjust(7),"ARRIVE".rjust(7),"PRICE".rjust(3))
                print(lineList[flightIndex].ljust(8), fnumList[flightIndex].ljust(6), depTime[flightIndex].rjust(7),arrTime[flightIndex].rjust(7),"$",str(price[flightIndex]).rjust(3))
            choice = getChoice()
        elif choice == 2:
            print("")
            #Looks through the times and finds the flights less than the given mins
            shortListIndex = findShorter(depTime,arrTime)
            if shortListIndex == []:
                print("")
                print("No flights meet your criteria")
            else:
                #prints all flights that meet cirteria
                print("")
                print("The flights that meet your criteria are:")
                print("")
                print("AIRLINE".ljust(8),"FLT#".ljust(6),"DEPART".rjust(7),"ARRIVE".rjust(7),"PRICE".rjust(3))
                for i in range(len(shortListIndex)):
                    print(lineList[shortListIndex[i]].ljust(8), fnumList[shortListIndex[i]].rjust(6), depTime[shortListIndex[i]].rjust(7), arrTime[shortListIndex[i]].rjust(7), "$", str(price[shortListIndex[i]]).rjust(3))
            choice = getChoice()
        elif choice == 3:
            print("")
            #finds the cheapest flights in an airline
            cheapIndex = cheapFlights(lineList,price)
            print("")
            print("The flight that meets your criteria is:")
            print("")
            print("AIRLINE".ljust(8),"FLT#".ljust(6),"DEPART".rjust(7),"ARRIVE".rjust(7),"PRICE".rjust(3))
            print(lineList[cheapIndex].ljust(8), fnumList[cheapIndex].ljust(6), depTime[cheapIndex].rjust(7), arrTime[cheapIndex].rjust(7), "$", str(price[cheapIndex]).rjust(3))
            choice = getChoice()
        elif choice == 4:
            #Finds flights taking over after specified time
            print("")
            timesIndex = flightTime(depTime)
            if timesIndex == []:
                print("")
                print("No flights meet your criteria")
            else:
                print("")
                print("The flights that meet your criteria are:")
                print("")
                print("AIRLINE".ljust(8),"FLT#".ljust(6),"DEPART".rjust(7),"ARRIVE".rjust(7),"PRICE".rjust(3))
                for i in range(len(timesIndex)):
                    print(lineList[timesIndex[i]].ljust(8), fnumList[timesIndex[i]].ljust(6), depTime[timesIndex[i]].rjust(7), arrTime[timesIndex[i]].rjust(7), "$", str(price[timesIndex[i]]).rjust(3))
            choice = getChoice()
        elif choice == 5:
            #calculates the price of all flights
            print("")
            average = flightAvg(price)
            print("The average price is $", average)
            choice = getChoice()
        elif choice == 6:
            #sorts all flights by departure time
            print("")
            sortFlights(lineList,fnumList,depTime,arrTime,price)
            print("Sorted data has been written to file: time-sorted-flights.csv")
            choice = getChoice()

    print("")
    print ("Thank you for flying with us")
            
    