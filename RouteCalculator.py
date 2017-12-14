import random

class routeCalculator:

    def __init__(self,dictionary,values):
        self.best=999999
        self.bestAuto=999999
        self.bestX=999999
        self.bestMini=999999
        self.travellingDuration=0
        self.travellingDurationAuto=0
        self.travellingDurationX=0
        self.travellingDurationMini=0
        self.values=values
        self.bestRoute=[]
        self.bestRouteAuto=[]
        self.bestRouteX=[]
        self.bestRouteMini=[]
        self.dictionary=dictionary
        self.population=[]
        self.fitness=[]
        self.permutations=0
        
    def checkEveryCombination(self):
        
        u=True
        while u==True:
            routeList=[]
            routeList=self.routeOrder(self.values) 
            routeMoney=self.calculateParameters(routeList)
            u,self.values=self.destinationPermutations(self.values)
        #print("best route : " + str(self.bestRoute))
        #print("best fare : " + str(self.best))
        
    def routeOrder(self,order):
        routeList=[]
        routeList.append('I')
        routeList.append('F')
        for y in order:
            sign='D'+str(y)
            routeList.append(sign)
        return routeList

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



    def generatePopulation(self,populationSize):
        strArray=self.values[:]
        for x in range(populationSize):
            random.shuffle(strArray)
            self.population.append(x)
            self.population[x]=strArray[:]
        for x in range(populationSize):
            routeList=[]
            routeList=self.routeOrder(self.population[x])        
            routeMoney=self.calculateParameters(routeList)
            self.fitness.append(1/(1+routeMoney))
        self.normalizeFitness()
        self.generateNewPopulation()
        for x in range(populationSize):
            routeList1=[]
            routeList1=self.routeOrder(self.population[x])        
            routeMoney=self.calculateParameters(routeList1)
        #print (self.best)
        #print(self.bestRoute)

    def generateNewPopulation(self):
        newPopulation=[]
        
        for x in range(len(self.population)):
            order=self.selectFrom()
            order=self.mutate(order,0.3)
            newPopulation.append(order)
            
        self.population=newPopulation
        
    def optimizeSolution(self):
        self.generateNewPopulation()
        for x in range(len(self.population)):
            routeList=[]
            routeList=self.routeOrder(self.population[x])        
            routeMoney=self.calculateParameters(routeList)     

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
        
    def selectFrom(self):
        i=0
        r=random.random()
        #print(self.fitness)
        while r>0:
            r=r-self.fitness[i%100]
            
            i=i+1
        return self.population[(i%100)-1]
        

    def mutate(self,order,rate):
        for i in range(len(order)):
            r=random.random()
            if r<rate:
                indexA=random.randint(0,len(order)-1)
                indexB=random.randint(0,len(order)-1)
                order=self.swapElements(order,indexA,indexB)
        return order
       
    
    def normalizeFitness(self):
        fitnessSum=0
        for i in range(len(self.fitness)):
            fitnessSum=fitnessSum+self.fitness[i]
        for i in range(len(self.fitness)):
            self.fitness[i]=self.fitness[i]/fitnessSum
        
    def swapElements(self,array,x,y):
        temp=array[x]
        array[x]=array[y]
        array[y]=temp
        return array







    
