# routeFinder
multiple destination best route finder using genetic algorithm

this application uses the functionality of uber python library and geocoder to get coordinates of user entered strings.

pip install uber_rides
pip install geocoder

try the above mentioned pip commands in case libraries are not present on your system.

Try: python RoutePlanner.py to  run the program.

1) Start with entering the pickup address
2) Follow it up by entering the final destination address
3) Enter the destination addresses the user intend to visit
4) Entering y at any time will lead to the calculation of the best available route.
5) Entering r in the console input will restart the program
6) Entering "exit" will result in termination of the program

In case google can't verify the coordinates, try retyping the address. More often than not the coordinates get verified with the same string.

Here are some examples destinations that has been used during the testing of this program, 
-> shalimar garden lahore
-> wildlife park lahore
-> fortress stadium lahore
-> university of engineering & Technology lahore
-> emporium mall lahore
-> pak heritage hotel lahore
-> Rose palace hotel lahore
-> airport lahore
-> avari hotel lahore
-> faisal town lahore

Multithreading has been used to speed up the data collection through the uber API. Two algorithms are coded to find the best routes. When the visiting destinations are less than or equal to 8, all permutations are checked to find the best route for the user to take(kind of a brute force method). If destinations are more than 8, then a genetic algorithm is used to find the optimized route. A population is initially generated randomly and for each order in the population, fitness is calculated based on the fare of that route. Next generation is populated besed on the fitness probability and given mutation aiding in finding a more optimized or cheaper route. 

I enjoyed working on this assignment. I look forward to hearing back from you.
Best regards,
Usman Sharif Khan
