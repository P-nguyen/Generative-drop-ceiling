from Autodesk.LibG import *

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

bsplines = []
for i in range(len(grid)-1):
    for j in range( len(grid[0])-1):
        new_bsplines_pointlist = PointList([grid[i][j], grid[i+1][j], grid[i][j+1], grid[i+1][j+1]])
        bsplines.append(BSplineSurface.by_points(new_bsplines_pointlist,2,2))

OUT= bsplines