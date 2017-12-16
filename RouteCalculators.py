import random
from threading import Thread
import numbers

class routeCalculator:

    def __init__(self,dictionary,values,impValues,importance):
        #Keeps the track of best route, fare and duration of travel for different uber services
        self.best=999999
        self.bestAuto=999999
        self.bestX=999999
        self.bestMini=999999
        self.travellingDuration=0
        self.travellingDurationAuto=0
        self.travellingDurationX=0
        self.travellingDurationMini=0
        self.bestRoute=[]
        self.bestRouteAuto=[]
        self.bestRouteX=[]
        self.bestRouteMini=[]
        #values supplied to the class
        self.values=values
        self.impValues=impValues
        self.importance=importance
        #Dictionary keeping record of fare prices and other uber related data for each link
        self.dictionary=dictionary
        #population of different orders
        self.population=[]
        #list of fitness values of the current population
        self.fitness=[]
        self.permutations=0
        #this is to check whether a threaded function is running
        self.threadRunning=False

#a function that runs in the background, so that every combination is checked in case genetic algorithm is invoked      
    def runThread(self):
        t1=Thread(target=self.checkEveryCombination)
        t1.setDaemon(True)
        t1.start()
        print("Thread Started")
        self.threadRunning=True

#arrange the important hop destinations according to the "*" supplied with the address
    def arrangePriorities(self):
        levels=0
        levelList=[]
        levelListImp=[]
        dictLevels={}
        i=0
        for x in self.impValues:
            importanceLevel=self.importance[x]
            if importanceLevel not in dictLevels:
                dictLevels[importanceLevel]=True
                levels=levels+1
            levelListImp.append(importanceLevel)
            levelList.append(x)
            for p in range(i):
                if levelListImp[i]>levelListImp[p]:
                    tempImp=levelListImp[i]
                    levelListImp[i]=levelListImp[p]
                    levelListImp[p]=tempImp
                    temp=levelList[i]
                    levelList[i]=levelList[p]
                    levelList[p]=temp
                elif levelListImp[i]==levelListImp[p]:
                    if levelList[i]<levelList[p]:
                        tempImp=levelListImp[i]
                        levelListImp[i]=levelListImp[p]
                        levelListImp[p]=tempImp
                        temp=levelList[i]
                        levelList[i]=levelList[p]
                        levelList[p]=temp
            i=i+1
        self.impValues=levelList
        return levels,levelListImp

# Generates a reverse order of list of lists to implement certain order of hops hierarchy
    def GenerateListOfLists(self,levelListImp):
        reverseLevels=[]
        d={}
        index1=-1
        r=0
        for h in levelListImp:
            if h not in d:
                index1=index1+1
                reverseLevels.append([])
                d[h]=1
                reverseLevels[index1].append(self.impValues[r])
                r=r+1
            else:
                reverseLevels[index1].append(self.impValues[r])
                r=r+1
        reverseLevels=reverseLevels[::-1]
        return reverseLevels

#this function checks every available route data and also implements the certain order of hops hierarchy
    def checkEveryCombination(self):
        levels,levelListImp=self.arrangePriorities()
        index=0
        reverseLevels=self.GenerateListOfLists(levelListImp)  
        v=True
        vals=[]
        reverse=reverseLevels[:]
        iValues=self.impValues[:]
        #this loop will run until all the choices are exhausted
        while v==True:
            #print(iValues)
            u=True
            vals=self.values
            while u==True:
                routeList=[]
                routeList=self.routeOrder(vals,iValues) 
                routeMoney=self.calculateParameters(routeList)
                u,vals=self.destinationPermutations(vals)
            for k in range(levels):
                array=reverse[k]
                e,array=self.destinationPermutations(array)
                if e==True:
                    for b in range(k):
                        reverse[b]=reverseLevels[b]
                    reverse[k]=array
                    break
                else:  
                    if k==(levels-1):
                        v=False
            if levels==0:
                v=False
            iValues1=reverse[::-1]
            iValues=[]
            for j in iValues1:
                try:
                    if isinstance(j,numbers.Integral):
                        iValues.append(j)
                    else:
                        for g in j:
                            iValues.append(g)
                except TypeError:
                    iValues.append(j)                                        
        if self.threadRunning==True:
            self.threadRunning=False

#returns a string with all the symbols attached so that the dictionary could be accessed   
    def routeOrder(self,order,iOrder):
        routeList=[]
        routeList.append('I')
        routeList.append('F')
        for z in iOrder:
            sign='D'+str(z)
            routeList.append(sign)
        for y in order:
            sign='D'+str(y)
            routeList.append(sign)
        return routeList

#calulates the data for route supplied in the argument
    def calculateParameters(self,route):
        routeMoney=0
        routeMoneyAuto=0
        routeMoneyX=0
        routeMoneyMini=0
        routeTime=0
        routeTimeAuto=0
        routeTimeX=0
        routeTimeMini=0
        end=False
        surgeFactor=1.0
        surgeFactorAuto=1.0
        surgeFactorX=1.0
        surgeFactorMini=1.0
        signGo=True
        signAuto=True
        signX=True
        signMini=True
        for x in range(len(route)):
            if x!=1:
                if x==0:
                    link=str(route[x])+str(route[x+2])
                elif x==(len(route)-1):
                    link=str(route[x])+str(route[1])
                    end=True
                else:
                    link=str(route[x])+str(route[x+1])
                if link in self.dictionary:
                    if x==0:
                        if 'uberGO' in self.dictionary[link]:
                            surgeFactor=float(self.dictionary[link]['uberGO']['surge'])
                        if 'uberAUTO' in self.dictionary[link]:
                            surgeFactorAuto=float(self.dictionary[link]['uberAUTO']['surge'])
                        if 'uberX' in self.dictionary[link]:
                            surgeFactorX=float(self.dictionary[link]['uberX']['surge'])
                        if 'Mini' in self.dictionary[link]:
                            surgeFactorMini=float(self.dictionary[link]['Mini']['surge'])
                    if 'uberGO' in self.dictionary[link]:
                        routeMoney=routeMoney+(float(self.dictionary[link]['uberGO']['price'])*float(surgeFactor))
                        routeTime=routeTime+(float(self.dictionary[link]['uberGO']['duration'])/60)
                    else:
                        signGo=False
                    if 'uberAUTO' in self.dictionary[link]:
                        routeMoneyAuto=routeMoneyAuto+(float(self.dictionary[link]['uberAUTO']['price'])*float(surgeFactorAuto))
                        routeTimeAuto=routeTimeAuto+(float(self.dictionary[link]['uberAUTO']['duration'])/60)
                    else:
                        signAuto=False
                    if 'uberX' in self.dictionary[link]:
                        routeMoneyX=routeMoneyX+(float(self.dictionary[link]['uberX']['price'])*float(surgeFactorX))
                        routeTimeX=routeTimeX+(float(self.dictionary[link]['uberX']['duration'])/60)
                    else:
                        signX=False
                    if 'Mini' in self.dictionary[link]:
                        routeMoneyMini=routeMoneyMini+(float(self.dictionary[link]['Mini']['price'])*float(surgeFactorMini))
                        routeTimeMini=routeTimeMini+(float(self.dictionary[link]['Mini']['duration'])/60)
                    else:
                        signMini=False
                if end==True:
                    if routeMoney<self.best and signGo==True:
                        self.best=routeMoney
                        self.bestRoute=route
                        self.travellingDuration=routeTime
                    if routeMoneyAuto<self.bestAuto and signAuto==True:
                        self.bestAuto=routeMoneyAuto
                        self.bestRouteAuto=route
                        self.travellingDurationAuto=routeTimeAuto
                    if routeMoneyX<self.bestX and signX==True:
                        self.bestX=routeMoneyX
                        self.bestRouteX=route
                        self.travellingDurationX=routeTimeX
                    if routeMoneyMini<self.bestMini and signMini==True:
                        self.bestMini=routeMoneyMini
                        self.bestRouteMini=route
                        self.travellingDurationMini=routeTimeMini
        return routeMoney

#function finds the next lexicographical order for a given sequence and return false if there is no available permutation
    def destinationPermutations(self,vals):
        largestx=-1
        for x in range(len(vals)-1):
            if vals[x]<vals[x+1]:
                largestx=x
        if largestx<0:
            return False,vals
        largesty=-1
        for y in range(len(vals)):
            if vals[y]>vals[largestx]:
                largesty=y
        vals=self.swapElements(vals,largestx,largesty)
        v=vals[(largestx+1):len(vals)]
        u=vals[0:(largestx+1)]
        v=v[::-1]
        for c in v:
            u.append(c)
        return True, u


#Runs the genetic algorithm where first a random population is created and then the fitness list is generated for that population.
    def generatePopulation(self,populationSize):
        levels,levelListImp=self.arrangePriorities()
        reverseLevels=self.GenerateListOfLists(levelListImp)
        strArray=self.values[:]
        for x in range(populationSize):
            random.shuffle(strArray)
            self.population.append(x)
            self.population[x]=strArray[:]
        reverse=reverseLevels[:]
        iValues=self.impValues[:]
        v=True
        while v==True:
            self.fitness=[]
            for x in range(populationSize):
                routeList=[]
                routeList=self.routeOrder(self.population[x],iValues)        
                routeMoney=self.calculateParameters(routeList)
                self.fitness.append(1/(1+routeMoney))
            for k in range(levels):
                array=reverse[k]
                e,array=self.destinationPermutations(array)
                if e==True:
                    for b in range(k):
                        reverse[b]=reverseLevels[b]
                    reverse[k]=array
                    break
                else:  
                    if k==(levels-1):
                        v=False
            if levels==0:
                v=False
            iValues1=reverse[::-1]
            iValues=[]
            for j in iValues1:
                try:
                    if isinstance(j,numbers.Integral):
                        iValues.append(j)
                    else:
                        for g in j:
                            iValues.append(g)
                except TypeError:
                    iValues.append(j)  
        self.normalizeFitness()

#updates the population generation using different functions
    def generateNewPopulation(self):
        newPopulation=[] 
        for x in range(len(self.population)):
            order=self.selectFrom()
            order=self.mutate(order,0.3)
            newPopulation.append(order) 
        self.population=newPopulation
        
#when o is pressed the following optimizeSolution is called
#where a new population is created from the last population and then all the orders are mutated to get a good diversity
    def optimizeSolution(self):
        self.generateNewPopulation()
        levels,levelListImp=self.arrangePriorities()
        reverseLevels=self.GenerateListOfLists(levelListImp)
        reverse=reverseLevels[:]
        iValues=self.impValues[:]
        v=True
        while v==True:
            self.fitness=[]
            for x in range(len(self.population)):
                routeList=[]
                routeList=self.routeOrder(self.population[x],iValues)        
                routeMoney=self.calculateParameters(routeList)
                self.fitness.append(1/(1+routeMoney))
            for k in range(levels):
                array=reverse[k]
                e,array=self.destinationPermutations(array)
                if e==True:
                    for b in range(k):
                        reverse[b]=reverseLevels[b]
                    reverse[k]=array
                    break
                else:  
                    if k==(levels-1):
                        v=False
            if levels==0:
                v=False
            iValues1=reverse[::-1]
            iValues=[]
            for j in iValues1:
                try:
                    if isinstance(j,numbers.Integral):
                        iValues.append(j)
                    else:
                        for g in j:
                            iValues.append(g)
                except TypeError:
                    iValues.append(j) 
        self.normalizeFitness()

#Function to print out the best route data whenever called
    def printing(self,addresses,symbols):
        bRoute=[]
        bRoute.append('I')
        aRoute=bRoute[:]
        xRoute=bRoute[:]
        mRoute=bRoute[:]
        b=self.bestRoute[2:len(self.bestRoute)]
        a=self.bestRouteAuto[2:len(self.bestRouteAuto)]
        x=self.bestRouteX[2:len(self.bestRouteX)]
        m=self.bestRouteMini[2:len(self.bestRouteMini)]
        for y in b:
            bRoute.append(y)
        for f in a:
            aRoute.append(f)
        for k in x:
            xRoute.append(k)
        for o in m:
            mRoute.append(o)
        bRoute.append('F')
        aRoute.append('F')
        xRoute.append('F')
        mRoute.append('F')
        if self.best<999999:
            print("Cheapest fair for UberGO : " +  str(self.best) + "  --  Duration : " + str(self.travellingDuration)+" mins")    
            print("Best Route : " +  str(bRoute))
        else:
            print ("UberGO data is missing in some packets, for this reason the program cannot calculate the best rate for this service")
        if self.bestAuto<999999:
            print("Cheapest fair for UberAUTO : " +  str(self.bestAuto)+ "  --  Duration : " + str(self.travellingDurationAuto)+" mins")    
            print("Best Route : " +  str(aRoute))
        else:
            print ("UberAuto data is missing in some packets, for this reason the program cannot calculate the best rate for this service")
        if self.bestX<999999:
            print("Cheapest fair for UberX : " +  str(self.bestX)+ "  --  Duration : " + str(self.travellingDurationX)+" mins")    
            print("Best Route : " +  str(xRoute))
        else:
            print ("UberX data is missing in some packets, for this reason the program cannot calculate the best rate for this service")
        if self.bestMini<999999:
            print("Cheapest fair for Mini : " +  str(self.bestMini)+ "  --  Duration : " + str(self.travellingDurationMini)+" mins")    
            print("Best Route : " +  str(mRoute))
        else:
            print ("Mini data is missing in some packets, for this reason the program cannot calculate the best rate for this service")
        
        for k in range(len(addresses)):
            print (symbols[k] + "  -  " + addresses[k])

#select one order from the excisting population according to the fitness value
    def selectFrom(self):
        i=0
        r=random.random()
        while r>0:
            r=r-self.fitness[i%100]
            
            i=i+1
        return self.population[(i%100)-1]
        
#brings some mutation in an order according to the rate supplied to the function
    def mutate(self,order,rate):
        for i in range(len(order)):
            r=random.random()
            if r<rate:
                indexA=random.randint(0,len(order)-1)
                indexB=random.randint(0,len(order)-1)
                order=self.swapElements(order,indexA,indexB)
        return order
       
#gets the fitness values between zero and one
    def normalizeFitness(self):
        fitnessSum=0
        for i in range(len(self.fitness)):
            fitnessSum=fitnessSum+self.fitness[i]
        for i in range(len(self.fitness)):
            self.fitness[i]=self.fitness[i]/fitnessSum
            
#swap two elements where location is x and y in a list
    def swapElements(self,array,x,y):
        temp=array[x]
        array[x]=array[y]
        array[y]=temp
        return array







    
