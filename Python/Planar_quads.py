import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

grid = IN
count = 0

for i in range(len(grid)):
    for j in range(len(grid[0])):
        count +=1 
    


OUT = count