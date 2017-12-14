
from threading import Thread
from Queue import Queue
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from geocoder import google
from RouteCalculator import routeCalculator

#gloabal variable declared

#bestRoute=[]
startVar=2
elements=0
dictionary={}
addresses=[]
addressSymbols=[]
latitude=[]
longitude=[]
count=1
loopCount=-1
q = Queue(maxsize=0)
session = Session(server_token='AmLts06BzIyzVahlxMaT4PcTKaxFBcz8wgA4rSJF')
client = UberRidesClient(session)
strArray=['fortress stadium lahore','3 saint johns park, lahore cantt','Allama Iqbal road Lahore','mm alam road,lahore','university of engineering technology, lahore','Avari hotel lahore']


def getPriceEstimate(q,initialLat,initialLng,finalLat,finalLng,keyString):
    averagePrice=0
    duration=0
    surge=1
    response = client.get_price_estimates(start_latitude=initialLat,\
        start_longitude=initialLng,end_latitude=finalLat,\
        end_longitude=finalLng,seat_count=2)
    estimate = response.json.get('prices')
    averagePrice=(float(str(estimate[0]['high_estimate']))+float(str(estimate[0]['low_estimate'])))/2
    duration = float(str(estimate[0]['duration']))
    surge= float(str(estimate[0]['surge_multiplier']))
    newString=keyString+"@"+str(averagePrice)+"@"+str(duration)+"@"+str(surge)
    q.put(newString)
    q.task_done()
    
def checkAddress(prompt):
    while True:
        value=raw_input(prompt)
        if value=="y" or value=="exit" or value=="restart":
            break
        try:
            g = google(value)
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
                break
            elif address!="y":
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
        q.join()
        for a in range(elements):
            s=q.get()
            stringSplit=s.split("@")
            if stringSplit[0] not in dictionary:
                dictionary[stringSplit[0]]={}
                dictionary[stringSplit[0]]['price']=stringSplit[1]
                dictionary[stringSplit[0]]['duration']=stringSplit[2]
                dictionary[stringSplit[0]]['surge']=stringSplit[3]
                #print dictionary
        values=[]
        for t in range(count-1):
            values.append(t+1)
    
        router=routeCalculator(dictionary,values)
        if count==1:
            print('Fare = ' + str(dictionary['IF']['uberAUTO']['price']))
        elif count<9:
            router.checkEveryCombination()
            router.printing(addresses,addressSymbols)
            
        else:
            router.generatePopulation(2000)
            router.printing(addresses,addressSymbols)
        while True:
            val = raw_input("Enter 'o' to optimize the solution OR 'r' to restart the program")
            if val=='r' or val=='exit':
                elements=0
                dictionary={}
                addresses=[]
                addressSymbols=[]
                latitude=[]
                longitude=[]
                count=1
                loopCount=-1
                break
            if val=='o':
                if count>8:
                    router.optimizeSolution()
                    router.printing(addresses,addressSymbols)
                    
                else:
                    print("The perfect solution is already provided")
