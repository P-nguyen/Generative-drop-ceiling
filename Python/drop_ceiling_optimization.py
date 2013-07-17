import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry
#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

#class is needed for each point? 
	#class info contains the point, and a boolean telling if it is still moveable
class Point_Check:
	def __init__(self, _point):
		self.point = _point
		self.boolean = False 
		
	def closest_geometry( self, geometry_list ):
		old_distance = 50000.0
		#
		for obj in geometry_list:
			closest_point = obj.get_closest_point(self.point)
			distance = closest_point.distance_to(self.point)
			if distance < old_distance:
				old_distance = distance
		
		return old_distance
##########################################################################

xlength = IN[0]
ylength = IN[1]
spacing = IN[2]
reference_geo = IN[3]

x_number = round(xlength/spacing)
y_number = round(ylength/spacing)

newx_spacing = xlength / x_number
newy_spacing = ylength / y_number

#create comprehensive list from [0,0,0] with all z at 0
grid = [ [ (y,x) for y in range( int(y_number)+1) ] for x in range( int(x_number) + 1 ) ]
#create grid spacing based on input and distances.
#grid_points = []
for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j] = Point_Check(Point.by_coordinates(i*newx_spacing, j*newy_spacing, 50.0))
		#grid_points.append( Point_Check(Point.by_coordinates(i*newx_spacing, j*newy_spacing, 0.0)) )
#then iterate through the points until all the z's are no longer allowed to move.

testpt = []
count = 1

while count > 0:
	count = 0
	#while there are still points.
	for i in range(int(x_number) + 1):
		for j in range(int(y_number) + 1):
			if grid[i][j].boolean == False:
				check = grid[i][j].closest_geometry( reference_geo )
				if check < 12:
					grid[i][j].boolean == True
				else:
					grid[i][j].point.set_z( grid[i][j].point.z() + 1)
					count += 1

if count == 0:
	for i in range(int(x_number) ):
		for j in range(int(y_number) ):
			#testpt.append(grid[i][j].point)
			pointlist = PointList([ grid[i][j].point, grid[i+1][j].point, grid[i+1][j+1].point, grid[i][j+1].point ])
			testpt.append( Polygon.by_points( pointlist ) )
#Assign your output to the OUT variable
OUT = testpt #grid_points #grid_points[0].boolean