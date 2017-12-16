
from threading import Thread
from Queue import Queue
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from geocoder import google
from RouteCalculators import routeCalculator
import json
#gloabal variable declared

#bestRoute=[]
startVar=2
signal=True
elements=0
dictionary={}
addresses=[]
addressSymbols=[]
latitude=[]
longitude=[]
count=1
loopCount=-1
numberOfDestinations=0
importance={}
q = Queue(maxsize=0)
session = Session(server_token='AmLts06BzIyzVahlxMaT4PcTKaxFBcz8wgA4rSJF')
client = UberRidesClient(session)
strArray=['fortress stadium lahore','3 saint johns park, lahore cantt','Allama Iqbal road Lahore','mm alam road,lahore','university of engineering technology, lahore','Avari hotel lahore']

#function to get the price estimates of given coordinates using uber api
def getPriceEstimate(q,initialLat,initialLng,finalLat,finalLng,keyString):
    averagePrice=0
    duration=0
    surge=1
    #dict1={}
    newString=keyString
    response = client.get_price_estimates(start_latitude=initialLat,\
        start_longitude=initialLng,end_latitude=finalLat,\
        end_longitude=finalLng,seat_count=2)
    estimate = response.json.get('prices')
    #dict1=json.loads(estimate)
    #print (estimate)
    newString=newString+"!"+str(len(estimate))
    for z in range(len(estimate)):
        displayName=(str(estimate[z]['display_name']))
        averagePrice=(float(str(estimate[z]['high_estimate']))+float(str(estimate[0]['low_estimate'])))/2
        duration = float(str(estimate[z]['duration']))
        surge= float(str(estimate[z]['surge_multiplier']))
        newString=newString+"!"+str(displayName)+"@"+str(averagePrice)+"@"+str(duration)+"@"+str(surge)
    q.put(newString)
    q.task_done()

#function run at each data entry so that the google coordinates are properly verified
def checkAddress(prompt):
    while True:
        value=raw_input(prompt)
        if value=="y" or value=="exit" or value=="restart":
            break
        try:
            value1=value.split('*')
            g = google(value1[0])
            if g.lat==None:
                print("Retry the address, google couldn't verify the coordinates")
                continue
            else:
                latitude.append(g.lat)            
                longitude.append(g.lng)
        except:
            print("Retry the address, google couldn't verify the coordinates")
            continue
        break
    return value

#function run after each data entry of the destination to store the importance of that address so that order of hops could be implemented later
def checkImportance(addressInput,c):
    numberStars=addressInput.count('*')
    if numberStars>0:
        importance[c]=numberStars
        address=addressInput.split('*')
        return address[0]
    return addressInput
    

if __name__ == "__main__":
    while True:
        initialAddress = checkAddress("Enter the pickup address: ")
        if initialAddress=='exit':
            break
        elif initialAddress=='restart':
            continue
        addresses.append(initialAddress)
        addressSymbols.append('I')
        finalAddress = checkAddress("Enter the final destination address: ")
        if finalAddress=='exit':
            break
        elif finalAddress=='restart':
            addressSymbols=[]
            addresses=[]
            continue
        addresses.append(finalAddress)
        addressSymbols.append('F')
        worker= Thread(target=(getPriceEstimate),args=(q,latitude[0],longitude[0],latitude[1],longitude[1],addressSymbols[0]+addressSymbols[1]))
        worker.setDaemon(True)
        worker.start()
        elements=elements+1
        print ('Enter "y" at any time to find the best possible route to take' )
        address="some value"
        while address!="y":
            address = checkAddress("Enter the address of a place you wanna visit: ")
            if address=='exit':
                q.join()
                while q.empty() is False:
                    print(q.get())
                break
            elif address=='restart':
                q.join()
                while q.empty() is False:
                    print(q.get())
                elements=0
                dictionary={}
                addresses=[]
                addressSymbols=[]
                latitude=[]
                longitude=[]
                count=1
                loopCount=-1
                numberOfDestinations=0
                importance={}
                break
            elif address!="y":
                numberOfDestinations=numberOfDestinations+1
                address=checkImportance(address,numberOfDestinations)
                addresses.append(address)
                stringSymbol='D'+str(count)
                addressSymbols.append(stringSymbol)
                count=count+1
                loopCount=loopCount+1
                start=startVar
                worker= Thread(target=(getPriceEstimate),args=(q,latitude[0],longitude[0],latitude[count],longitude[count],addressSymbols[0]+addressSymbols[count]))
                worker.setDaemon(True)
                worker.start()
                elements=elements+2
                worker= Thread(target=(getPriceEstimate),args=(q,latitude[count],longitude[count],latitude[1],longitude[1],addressSymbols[count]+addressSymbols[1]))
                worker.setDaemon(True)
                worker.start()
                for k in range(loopCount):
                    worker= Thread(target=(getPriceEstimate),args=(q,latitude[start],longitude[start],latitude[count],longitude[count],addressSymbols[start]+addressSymbols[count]))        
                    worker.setDaemon(True)
                    worker.start()
                    worker= Thread(target=(getPriceEstimate),args=(q,latitude[count],longitude[count],latitude[start],longitude[start],addressSymbols[count]+addressSymbols[start]))
                    worker.setDaemon(True)
                    worker.start()
                    start=start+1
                    elements=elements+2
        if address=='exit':
            break
        elif address=='restart':
            continue
        #waits for all the queues to finish up storing 
        q.join()
        #uses queue to store the data of links in the dictionary in the following lines of code
        for a in range(elements):
            s=q.get()
            stringSplit=s.split("!")
            if stringSplit[0] not in dictionary:
                dictionary[stringSplit[0]]={}
                for t in range(int(stringSplit[1])):
                    stringSplit1=stringSplit[t+2].split("@")
                    dictionary[stringSplit[0]][stringSplit1[0]]={}
                    dictionary[stringSplit[0]][stringSplit1[0]]['price']=stringSplit1[1]
                    dictionary[stringSplit[0]][stringSplit1[0]]['duration']=stringSplit1[2]
                    dictionary[stringSplit[0]][stringSplit1[0]]['surge']=stringSplit1[3]
        
        values=[]
        impValues=[]
        impCount=0
        ordinaryCount=0
        #check to implement certain order of hops to differentiate between important destinations
        for t in range(count-1):
            index=t+1
            if index in importance:
                impCount=impCount+1
                impValues.append(index)
            else:
                ordinaryCount=ordinaryCount+1
                values.append(index)
        #print ("Important values: " + str(impValues))
        router=routeCalculator(dictionary,values,impValues,importance)
        if count==1:
            print('Fare = ' + str(dictionary['IF']['uberAUTO']['price']))
        elif ordinaryCount<8:
            signalFinished=True
            router.checkEveryCombination()
            router.printing(addresses,addressSymbols)
            
        else:
            signalFinished=False
            if signal==True:
                #call the thread to check every combination in the background
                router.runThread()
                signal=False
            router.generatePopulation(500)
            router.printing(addresses,addressSymbols)
        val=''
        while True:
            if count>1:
                val = raw_input("Enter 'o' to optimize the solution OR 'r' to restart the program")
            else:
                val = raw_input("Enter r to restart the program")                
            if val=='r' or val=='exit':
                elements=0
                dictionary={}
                addresses=[]
                addressSymbols=[]
                latitude=[]
                longitude=[]
                count=1
                loopCount=-1
                numberOfDestinations=0
                importance={}
                signal=True
                break
            if val=='o':
                if signalFinished==False:
                    if router.threadRunning==True:
                        router.optimizeSolution()
                        router.printing(addresses,addressSymbols)
                    else:
                        print ("*****The Perfect Solution*****") 
                        router.printing(addresses,addressSymbols)
                else:
                    print("The perfect solution is already provided")
        if val=='exit':
            break
