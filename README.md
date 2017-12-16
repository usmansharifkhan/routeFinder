# RouteFinder
Multiple destination route finder using a combination of factorial combinations and genetic algorithm.

This application uses the functionality of uber python library and geocoder to get coordinates of user entered strings.

pip install uber_rides
pip install geocoder

Try the above mentioned pip commands in case libraries are not present on your system.

Try running python RoutePlanners.py to  run the updated program incorporating the functionality of certain hops order.

In case google can't verify the coordinates, try retyping the address. More often than not the coordinates get verified with the same string. 
1) Start with entering the pickup address
2) Follow it up by entering the final destination address
3) Enter the destination addresses the user intend to visit
4) Adding * at the end of destination assigns it a priority, number of stars determine the hierarchy
4) Entering y at any time will lead to the calculation of the best available route.
5) Entering r in the console input will restart the program
6) Entering "exit" will result in termination of the program
7) Once the route calculation is completed and best available route is diplayed. The best route could be optimized by entering 'o' in the console


Here are some examples destinations that has been used during the testing of this program, 
-> liberty mall lahore
-> badshahi moque lahore
-> fortress stadium lahore
-> university of engineering & Technology lahore
-> emporium mall lahore
-> sheesh mahal lahore
-> shalimar gardens,Lahore
-> allama iqbal international airport lahore
-> avari hotel lahore
-> mm alam road lahore
-> allama iqbal road lahore

Implementation of prioritizing different destinations: Putting * at the end of an address makes that address a priority. Number of stars at the end of the address determines its importance. Two or more destinations having the same priority are permutated to calculate the optimum route.

Multithreading has been used to speed up the data collection using uber API. Two algorithms are coded to find the best routes. When the visiting non-prioritized destinations are less than or equal to 8, all permutations are checked to find the best route for the user to take. If destinations are more than 8, then a genetic algorithm is used to find the optimized route. A population is initially generated randomly and for each order in the population, fitness is calculated based on the fare of that route. Next generation is populated based on the fitness probability and given mutation aiding in finding a more optimized or cheaper route. Before the genetic algorithm is run in the updated version of file,a threaded function of brute force algorithm is made to run in the background to find the optimum route eventually.

I enjoyed working on this assignment and many thanks for the opportunity given to me.
Best regards,
Usman Sharif Khan
