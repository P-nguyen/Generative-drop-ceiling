# be sure to include this so everything works in Dynamo Revit
import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
# be sure to include this so you have code completion
from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Cuboid,CoordinateSystem
from Autodesk.LibG import *

start_offset_x = 75
start_offset_y = 75

xlength = 650 - start_offset_x
ylength = 650 - start_offset_y
spacing = 110

max_vertical = 1000

x_number = round(xlength/spacing)
y_number = round(ylength/spacing)

newx_spacing = xlength / x_number
newy_spacing = ylength / y_number

reference_geo = IN

class GridNode:
	def __init__(self, start_point):
		self.start_point = start_point
		line_end = Point.by_coordinates(start_point.x(), start_point.y(), start_point.z() + max_vertical)
		self.vertical_line = Line.by_start_point_end_point(start_point, line_end)
		
		self.set_nearby_objects()
		
		self.set_lowest_intersect()
		
	# finds and sets the objects this GridNode should look at when
	# performing intersection tests
	def set_nearby_objects(self):
		base_cs = CoordinateSystem.by_origin(self.start_point)
		base_cuboid = Cuboid.by_lengths(base_cs, spacing * 2, spacing * 2, max_vertical * 2)
		
		base_cuboid.set_visibility(False)
		
		nearby_objects = []
		
		for geo in reference_geo:
			if geo.does_intersect(base_cuboid) == False:
				continue
			
			nearby_objects.append(geo)
			
		self.nearby_objects = nearby_objects
		
	def set_lowest_intersect(self):
		lowest_intersection = None
		
		for geo in self.nearby_objects:
			if geo.does_intersect(self.vertical_line) == False:
				continue
			
			point_intersections = geo.intersect(self.vertical_line)
			
			for p_intersect in point_intersections:
				# since this is a line, we know the intersection will be a point
				point = Point.cast(p_intersect)
				
				# the intersection should be a point, but abort just in case something goes wrong
				if point == None:
					continue;
			
				if lowest_intersection == None:
					lowest_intersection = point
					continue
				
				# ignore the point if it's higher than our current lowest
				if point.z() > lowest_intersection.z():
					continue
				
				lowest_intersection = point
				
			# note that these won't show up in the OpenGL viewer
			self.lowest_intersection = lowest_intersection
			
class GridQuad:
	def __init__(self, node_1, node_2, node_3, node_4):
		self.node_1 = node_1
		self.node_2 = node_2
		self.node_3 = node_3
		self.node_4 = node_4
		
		nearby_objects = []
		
		nearby_objects.extend(node_1.nearby_objects)
		nearby_objects.extend(node_2.nearby_objects)
		nearby_objects.extend(node_3.nearby_objects)
		nearby_objects.extend(node_4.nearby_objects)
		
		self.nearby_objects = nearby_objects
		
		self.create_polygon()
		
	def create_polygon(self):
		points = [self.node_1.lowest_intersection, self.node_2.lowest_intersection, self.node_3.lowest_intersection, self.node_4.lowest_intersection]
		self.polygon = Polygon.by_points(PointList(points))
		
		
		
grid = [ [ (y, x) for y in range( int(y_number) + 1) ] for x in range(int(x_number) + 1) ]
 
for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j] = GridNode(Point.by_coordinates(i*newx_spacing + start_offset_x, j*newy_spacing + start_offset_y, 0.0))
 
grid_nodes = [ [ (y, x) for y in range(int(y_number)) ] for x in range(int(x_number)) ]

for i in range(int(x_number)):
	for j in range(int(y_number)):
		grid_nodes[i][j] = GridQuad(grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1])

				 
OUT = None
