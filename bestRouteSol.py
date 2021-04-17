import math
import copy

# minimum time initialize
minCost = 1000000000
finalPath = []

# Function for haversine formula

def haversine(lat1, lon1, lat2, lon2):

    # difference between latitudes and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2))
    rad = 6371
    d = 2 * rad * math.asin(math.sqrt(a))
    return d

#time calculation for given distance

def timeCalculation(distance):
    speed = 20
    time = distance/speed
    return time

# Function to find the best route

def bestRoute(graph, visited, currPos, n, count, cost, foodPrepTime, path):

    global minCost
    global finalPath

    # Condition to check whether we visited all points
    if (count == n):

        # Comparision with minimum cost
        if(cost < minCost):
            minCost = cost
            pathlist = copy.deepcopy(path)
            finalPath = pathlist
        return

    # loop for next location in path
    for i in range(n):

        # If not visited visit the location
        if (visited[i] == False and currPos != i):

            # Mark as visited
            visited[i] = True

            # condition to check - Customer must not be visited before their respective restaurant
            if(i >= n//2+1 and visited[int(i - (n-1)//2)]):
                path.append(i)

                #time Calculation for given distance
                time = timeCalculation(graph[currPos][i])
                
                bestRoute(graph, visited, i, n, count + 1,
                          cost + time, foodPrepTime, path)

                #pop current i after all permutations
                path.pop()
            # Condition for restaurant - time taken is maximum of cooking time , travelling time
            if(i <= n//2):
                path.append(i)

                #time Calculation for given distance
                time = timeCalculation(graph[currPos][i])

                # Check if food preparation is greater than cost
                if(foodPrepTime[i-1] > cost + time):
                    time = foodPrepTime[i-1] - cost

                bestRoute(graph, visited, i, n, count + 1,
                          cost + time, foodPrepTime, path)

                #pop current i after all permutations
                path.pop()
            # Mark ith node as unvisited
            visited[i] = False


# Driver code
if __name__ == "__main__":

    # Distances between every location
    graph = []

    # locations in list of tuples
    # [Aman,Restaurants R1, R2, Customers C1, C2]
    locations = [(51.5221, 12.5896), (51.5685, 12.5862), (51.5632, 12.5665),
                 (51.5266, 12.5923), (51.5696, 12.5647)]
    
    # food preparation time in Hours
    foodPrepTime = [0.5, 0.33]
    n = len(locations)
    for i in range(n):
        listt = [0]*n
        graph.append(listt)

    # Finding distances between every points
    for i in range(len(locations)):
        for j in range(i, len(locations)):
            distance = haversine(
                locations[i][0], locations[i][1], locations[j][0], locations[j][1])
            graph[i][j] = graph[j][i] = distance

    visited = [False for i in range(n)]

    # Present Aman position is visited
    visited[0] = True

    # path starts from current position
    path = [0]

    # Recursive Function call
    bestRoute(graph, visited, 0, n, 1, 0, foodPrepTime, path)

    # Shortest Possible Time
    print(minCost)

    # Printing the final Path
    print(finalPath)

    for i in finalPath:
        if(i == 0):
            print("Aman  --> ", end="")
        elif(i <= n//2):
            print("Restaurant "+str(i)+" --> ", end="")
        else:
            print("Customer "+str(i - n//2)+" --> ", end="")
    print("Completed")
