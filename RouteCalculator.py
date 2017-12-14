import random

class routeCalculator:

    def __init__(self,dictionary,values):
        self.best=999999
        self.values=values
        self.bestRoute=[]
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
        end=False
        surgeFactor=1.0
        for x in range(len(route)):
            if x!=1:
                if x==0:
                    link=str(route[x])+str(route[x+2])
                elif x==(len(route)-1):
                    link=str(route[x])+str(route[1])
                    end=True
                else:
                    link=str(route[x])+str(route[x+1])
                #print(link)
                if link in self.dictionary:
                    if x==0:
                        #print("alpha")
                        surgeFactor=float(self.dictionary[link]['surge'])
                    routeMoney=routeMoney+(float(self.dictionary[link]['price'])*float(surgeFactor))
                    #print(routeMoney)

                if end==True:
                    if routeMoney<self.best:
                        self.best=routeMoney
                        self.bestRoute=route
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
        b=self.bestRoute[2:len(self.bestRoute)]
        for y in b:
            bRoute.append(y)
        bRoute.append('F')
        print("Cheapest fair for UberAUTO : " +  str(self.best))    
        print("Best Route : " +  str(bRoute))
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







    
