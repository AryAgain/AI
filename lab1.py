"""
file: lab1.py
description: Generate optimal paths for the sport of orienteering
language: python3
"""
import sys
from sys import argv
from PIL import Image
import math

class pixelNode:
    """
    Each pixel is represented using the class to store the various
    properties for easier calculations
    :param xValue - x coordinate
    :param yValue - y coordinate
    :param type - type of terrain
    :param elevation - elevation of the pixel
    :param alreadyVisited - alreadyVisited for this pixel
    :param fValue : f(n) = g(n) + h(n)
    """

    def __init__(self,xValue,yValue):
        self.xValue = xValue
        self.yValue = yValue
        self.type = None
        self.elevation = None
        self.alreadyVisited = None
        self.fValue = float("inf")


# a list to store final path
finalPath = []

# Each terrain's speed stored as dictionary
# as per time it would take to cross through them
terrainSpeeds = {"openLand":2}
terrainSpeeds["roughMeadow"] = 0.25
terrainSpeeds["easyMoveForest"] = 1.25
terrainSpeeds["slowRunForest"] = 1
terrainSpeeds["walkForest"] = 0.75
terrainSpeeds["impassibleVegetation"] = 0
terrainSpeeds["lakeSwamp"] = 0
terrainSpeeds["pavedRoad"] = 2
terrainSpeeds["footpath"] = 2
terrainSpeeds["outOfBounds"] = 0


# Each terrain's colormap value stored in a dictionary
# corresponding to the description
colorIdentifier = {(248,148,18):"openLand"}
colorIdentifier[(255,192,0)]= "roughMeadow"
colorIdentifier[(255,255,255)]= "easyMoveForest"
colorIdentifier[(2,208,60)] = "slowRunForest"
colorIdentifier[(2,136,40)] = "walkForest"
colorIdentifier[(5,73,24)] = "impassibleVegetation"
colorIdentifier[(0,0,255)] = "lakeSwamp"
colorIdentifier[(71,51,3)] = "pavedRoad"
colorIdentifier[(0,0,0)] = "footpath"
colorIdentifier[(205,0,101)] = "outOfBounds"



def calculateG(startPoint, endPoint, movement,speed):
    """
    This function calculates the cost(g value) between two pixels
    :param  startPoint  start value
    :param  endPoint    end value point
    :param  movement    direction in which to go
    :param  speed   the calculated speed
    """
    if movement == "longitude":
        dist = math.sqrt(((endPoint.elevation - startPoint.elevation)*10.29) ** 2)
    else:
        dist = math.sqrt(((endPoint.elevation - startPoint.elevation)*7.55) ** 2)
    gValue = dist/(speed[startPoint.type] + (startPoint.elevation-endPoint.elevation)/40)

    return gValue

def calculateH(pixelPoint, destination):
    """
    This function calculates the heuristic for a pixel
    :param  pixelPoint  pixel value on map for which Heurestic needs to be calculated
    :param  destination the destination value
    """
    return math.sqrt((pixelPoint.xValue-destination.xValue)**2 + (pixelPoint.yValue-destination.yValue)**2 + \
        (pixelPoint.elevation-destination.elevation)**2)/2

def calculateF(current,neighbour,destination,speed):
    """
    This function calculates the total fValue for the pixel.
    :param  current     the current pixel value
    :param  neighbour   neigbor of current
    :param  destination destination to be reached
    :param  speed   speed value
    """
    if neighbour.xValue == current.xValue:
        totalDistance = calculateG(current,neighbour,"longitude",speed)+\
            calculateH(neighbour,destination)
    else:
        totalDistance = calculateG(current,neighbour,"lattitude",speed)+\
            calculateH(neighbour,destination)
    return totalDistance

def getNeighbors(source,terrain,speed):
    """
    Calculates all neighbor value for the provided source
    :param  source  source pixel value
    :param  terrain 2D array of terrain value
    :param  speed   speed calculated value
    """
    possibleNeighbors = []
    xValue = source.xValue
    yValue = source.yValue

    if xValue == 0 and yValue == 0:
        if speed[terrain[xValue][yValue+1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue+1])
        if speed[terrain[xValue+1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue+1][yValue])
    elif xValue == 0 and yValue == 394:
        if speed[terrain[xValue][yValue-1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue-1])
        if speed[terrain[xValue+1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue+1][yValue])
    elif xValue == 499 and yValue == 0:
        if speed[terrain[xValue][yValue+1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue+1])
        if speed[terrain[xValue-1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue-1][yValue])
    elif xValue == 499 and yValue == 394:
        if speed[terrain[xValue][yValue-1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue-1])
        if speed[terrain[xValue-1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue-1][yValue])
    elif xValue == 0 and (yValue > 0 and yValue < 394):
        if speed[terrain[xValue][yValue-1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue-1])
        if speed[terrain[xValue][yValue+1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue+1])
        if speed[terrain[xValue+1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue+1][yValue])
    elif xValue == 499 and (yValue > 0 and yValue < 394):
        if speed[terrain[xValue][yValue-1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue-1])
        if speed[terrain[xValue][yValue+1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue+1])
        if speed[terrain[xValue-1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue-1][yValue])
    elif yValue == 0 and (xValue > 0  and xValue < 499):
        if speed[terrain[xValue+1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue+1][yValue])
        if speed[terrain[xValue][yValue+1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue+1])
        if speed[terrain[xValue-1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue-1][yValue])
    elif yValue == 394 and (xValue > 0  and xValue < 499):
        if speed[terrain[xValue+1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue+1][yValue])
        if speed[terrain[xValue][yValue-1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue-1])
        if speed[terrain[xValue-1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue-1][yValue])
    else:
        if speed[terrain[xValue+1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue+1][yValue])
        if speed[terrain[xValue][yValue-1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue-1])
        if speed[terrain[xValue-1][yValue].type] != 0:
            possibleNeighbors.append(terrain[xValue-1][yValue])
        if speed[terrain[xValue][yValue+1].type] != 0:
            possibleNeighbors.append(terrain[xValue][yValue+1])

    return possibleNeighbors


def findShortestPath(source,destination,terrain,speed):
    """
    This function performs the A* search on the input to find shortest path
    :param source       The starting pixelNode
    :param destination  The end pixelNode
    :param terrain      2D array of all the 500x395 Nodes
    :param speed        dictionary of speed as per terrain
    """
    if(speed[source.type] == 0):
        print(source.xValue + "," + source.yValue + " is invalid source")
        return
    if(speed[destination.type] == 0):
        print(destination.xValue + "," + destination.yValue + " is invalid destination")
        return
    visited = []    # pixels that have been visited
    toExplore = []  # pixels that have to be visited (frontier)
    source.fValue = 0
    current = source    # current pixel
    toExplore.append(current)
    while len(toExplore) != 0:
        #calculate the lowest total fValue
        lowestF = None
        minScore = float("inf")
        for pixelNode in toExplore:
            if pixelNode.fValue < minScore:
                minScore = pixelNode.fValue
                lowestF = pixelNode

        current = lowestF
        if current == destination:
            # if a finalPath is found
            while current.alreadyVisited:
                # compute the finalPath
                pixelPoint = []
                pixelPoint.append(current.xValue)
                pixelPoint.append(current.yValue)
                finalPath.append(pixelPoint)
                current = current.alreadyVisited
            pixelPoint = []
            pixelPoint.append(current.xValue)
            pixelPoint.append(current.yValue)
            finalPath.append(pixelPoint)
            return finalPath
        toExplore.remove(current)
        visited.append(current)
        neighbors = getNeighbors(current,terrain,speed)
        for neighbour in neighbors:
            # computing the scores for each neighbor
            if neighbour not in visited:
                if neighbour in toExplore:
                    # if the neighbour has been seen before
                    fValue = calculateF(current,neighbour,destination,speed)
                    if fValue < neighbour.fValue:
                        neighbour.fValue = fValue
                        neighbour.alreadyVisited = current
                else:
                    # if the neighbour has not been seen before
                    neighbour.fValue = calculateF(current,neighbour,destination,speed)
                    neighbour.alreadyVisited = current
                    toExplore.append(neighbour)
    print("no finalPath found")

def buildMap(terrainArray,elevationList):
    """
    This function creates a 2D map of pixel nodes for all the map
    :param terrainArray     2D array of terrain
    :param elevationList    2D array of elevation values
    """
    terrain = []
    for row in range(500):
        line = []
        for col in range(395):
            temp = pixelNode(row,col)
            ## to get the value of first three color numbers
            ## as image getdata outputs 4 indexed array
            temp.type = colorIdentifier[terrainArray[row][col][:3]]
            temp.elevation = elevationList[row][col]
            line.append(temp)
        terrain.append(line)
    return terrain


def main():
    """
    This is the main program
    """
    speed = terrainSpeeds
    elevationList = []
    with open(argv[2]) as f:
        # reading the elevation data
        for line in f:
            line = line.strip()
            temp = line.split()
            for index in range(len(temp)):
                temp[index] = float(temp[index])
            elevationList.append(temp)

    # loading the respective map
    img = Image.open(argv[1])
    # making list of pixels color from image
    mapImage = list(img.getdata())
    # to store terrain finalPath in 2d array
    terrainArray = []
    cols = 0
    row = []
    # turning the list of pixels into 2D array as per image
    for pixel in mapImage:
        row.append(pixel)
        cols += 1
        if cols == 395:
            cols = 0
            terrainArray.append(row)
            row = []

    inputFile = argv[3]
    # to store course paths it need to take
    courses = []
    with open(inputFile) as inp:
        for line in inp:
            pixelPoint = []
            line = line.strip()
            temp = line.split()
            # yValue axis first in list and xValue axis value is stored second
            pixelPoint.append(int(temp[1]))
            pixelPoint.append(int(temp[0]))
            courses.append(pixelPoint)


    for index in range(len(courses)-1):
        # will store the pixelNode in 2D array as per each pixel
        terrain = buildMap(terrainArray,elevationList)
        source = courses[index]
        destination = courses[index+1]
        findShortestPath(terrain[source[0]][source[1]],terrain[destination[0]][destination[1]],terrain,speed)

    distance = 0
    # loop to calculate distance and draw finalPath
    for index in range(len(finalPath) -1):
        img.putpixel((finalPath[index][1],finalPath[index][0]),(255,0,127))
        distance = distance + (math.sqrt(((finalPath[index][0] - finalPath[index+1][0])*7.55) ** 2 +
                                         ((finalPath[index][1] - finalPath[index+1][1])*10.29) ** 2 +
                        (float(elevationList[finalPath[index][1]][finalPath[index][0]])-float(elevationList[finalPath[index+1][1]][finalPath[index+1][0]]))**2))

    img.putpixel((finalPath[len(finalPath)-1][1], finalPath[len(finalPath)-1][0]), (255, 0, 127))
    # saving the final output image
    img.save(argv[4])
    print("Total distance: " + str(distance) + " m")


if __name__ == '__main__':
    # argument check
    if len(sys.argv) == 5:
        main()
    else:
        print("Error! \n It should take 4 arguments, in order: terrain-image, elevation-file, path-file, output-image-filename")
