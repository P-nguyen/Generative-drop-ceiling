# be sure to include this so everything works in Dynamo Revit
import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
# be sure to include this so you have code completion
from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Cuboid,CoordinateSystem,Plane,Vector
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

reference_geo = []

reference_geo.extend(IN[1])
reference_geo.extend(IN[2])
reference_geo.extend(IN[3])
reference_geo.extend(IN[4])


base_plane = Plane.by_origin_normal(Point.by_coordinates(0, 0, 0), Vector.by_coordinates(0, 0, 1))

class GridNode:
	def __init__(self, start_point):
		self.start_point = start_point
		
		self.set_nearby_objects()
		
		self.set_lowest_point()
		
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
		
	def set_lowest_point(self):
		lowest_point = None
		
		for geo in self.nearby_objects:
			
			closest_point = geo.get_closest_point(base_plane)
			
			if closest_point == None:
				continue
			
			if lowest_point == None:
				lowest_point = closest_point
				continue
			
			if closest_point.z() > lowest_point.z():
				continue
			
			lowest_point = closest_point
			
		self.lowest_point = lowest_point
		
		if lowest_point == None:
			self.low_point = self.start_point
		else:
			self.low_point = Point.by_coordinates(self.start_point.x(), self.start_point.y(), lowest_point.z())
			
class GridQuad:
	def __init__(self, node_1, node_2, node_3, node_4):
		self.node_1 = node_1
		self.node_2 = node_2
		self.node_3 = node_3
		self.node_4 = node_4
		
		self.polygon_point_list = PointList([self.node_1.low_point, self.node_2.low_point, self.node_3.low_point, self.node_4.low_point])
		
		self.set_lowest_point()
		
		nearby_objects = []
		
		nearby_objects.extend(node_1.nearby_objects)
		nearby_objects.extend(node_2.nearby_objects)
		nearby_objects.extend(node_3.nearby_objects)
		nearby_objects.extend(node_4.nearby_objects)
		
		self.nearby_objects = nearby_objects
		
		self.create_polygon()
		
	def set_lowest_point(self):
		self.lowest_point = self.node_1.lowest_point
		
		pts = [self.node_2.lowest_point, self.node_3.lowest_point, self.node_4.lowest_point]
		
		for pt in pts:
			if pt.z() > self.lowest_point.z():
				continue
			self.lowest_point = pt
		
	def create_polygon(self):
		self.polygon = Polygon.by_points(self.polygon_point_list)
		
	def update_polygon(self):
		self.polygon.update_vertices(self.polygon_point_list)
		
	def intersects_nearby_objects(self):
		for geo in self.nearby_objects:
			if geo.does_intersect(self.polygon):
				return True
		return False
		
	def make_more_planar(self):
		node_1 = self.node_1
		node_2 = self.node_2
		node_3 = self.node_3
		node_4 = self.node_4
		
		plane = Plane.by_three_points(node_1.low_point, node_2.low_point, node_3.low_point)
		
		project_point = plane.get_closest_point(node_4.low_point)
		
		dif_x = project_point.x() - node_4.low_point.x()
		dif_y = project_point.y() - node_4.low_point.y()
		dif_z = project_point.z() - node_4.low_point.z()
		
		dif_x /= 2.0
		dif_y /= 2.0
		dif_z /= 2.0
		
		new_x = node_4.low_point.x() + dif_x
		new_y = node_4.low_point.y() + dif_y
		new_z = node_4.low_point.z() + dif_z
		
		node_4.low_point.set_x(new_x)
		node_4.low_point.set_y(new_y)
		node_4.low_point.set_z(new_z)
		
		self.update_polygon()
		
		if self.intersects_nearby_objects() == False:
			return
		
		dif_z = self.lowest_point.z() - node_4.low_point.z()
		
		dif_z /= 2.0
		
		new_z = node_4.low_point.z() + dif_z
		
		node_4.low_point.set_z(new_z)
		
		
grid = [ [ (y, x) for y in range( int(y_number) + 1) ] for x in range(int(x_number) + 1) ]
 
for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j] = GridNode(Point.by_coordinates(i*newx_spacing + start_offset_x, j*newy_spacing + start_offset_y, 0.0))
 
grid_nodes = [ [ (y, x) for y in range(int(y_number)) ] for x in range(int(x_number)) ]

for i in range(int(x_number)):
	for j in range(int(y_number)):
		grid_nodes[i][j] = GridQuad(grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1])
 
 
num_iterations = 50
 
for n in range(num_iterations):
	for i in range(int(x_number)):
		for j in range(int(y_number)):
			grid_nodes[i][j].make_more_planar()
 			
for i in range(int(x_number)):
	for j in range(int(y_number)):
		grid_nodes[i][j].create_polygon()

OUT = None
