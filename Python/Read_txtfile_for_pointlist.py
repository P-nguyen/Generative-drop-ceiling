import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

text = IN
split_text = text.split("\n")

pointlist = []
for text_line in split_text:
    pointlist.append(text_line.split("/"))

grid = [ [ (y,x) for y in range( len(pointlist[0])) ] for x in range( len(pointlist)) ]

for i in range(len(pointlist)):
    for j in range(len(pointlist[i])):
        xyz = pointlist[i][j].split(",")
        grid[i][j] = Point.by_coordinates( float(xyz[0]), float(xyz[1]), float(xyz[2]))

OUT = grid
