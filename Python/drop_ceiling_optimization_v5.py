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
class PointCheck:
	def __init__(self, _point):
		self.point = _point
		self.stored_geometry = []
		self.stored_points = []
		self.top_point = None
		#self.point_direction = None #possible will need to give the point a direction of movement.

		
	def objects_within_proximity( self, geometry_list ):	#stores whatever ceiling objects are with in proximity
		lowest_z = None
		
		for object in geometry_list:
			object_point = object.get_closest_point(self.point)
			test_point = Point.by_coordinates(self.point.x(), self.point.y(), object_point.z())
			dist = test_point.distance_to(object_point)
			
			if dist > 120: #half of IN spacing.
				continue
			
			self.stored_geometry.append(object)
			#self.stored_points.append([ test_point, object_point, object_point.z() ])
			self.stored_points.append([object_point, object_point.z()])

		return 
				
	def set_closest_geometry( self, geometry_list ):  #this one only finds the closest point. we need one that finds the proximitiy.
		
		self.objects_within_proximity(geometry_list)
		self.stored_points.sort(key=lambda sublist: sublist[1])
		
		self.top_point = Point.by_coordinates(self.point.x(), self.point.y(), self.stored_points[0][0].z())
		
		return #closest_geometry
		

##########################################################################

xlength = IN[0]
ylength = IN[1]
spacing = IN[2]
reference_geo = IN[3]

x_number = round(xlength/spacing)
y_number = round(ylength/spacing)

newx_spacing = xlength / x_number
newy_spacing = ylength / y_number


grid = [ [ (y,x) for y in range( int(y_number)+1) ] for x in range( int(x_number) + 1 ) ]
output_debug_geometry = []

for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j] = PointCheck(Point.by_coordinates(i*newx_spacing, j*newy_spacing, 0.0))

for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j].set_closest_geometry(reference_geo)
		output_debug_geometry.append(grid[i][j].top_point)



class Check_SurfacePanel_intersection:

	def __init__(self, point_checks): #point_check is  alist of points. or [pointcheks]
		self.point_checks = point_checks
		p1 = point_checks[0].top_point
		p2 = point_checks[1].top_point
		p3 = point_checks[2].top_point
		p4 = point_checks[3].top_point
		self.polygon_pointlist = PointList([p1, p2, p3, p4])
		self.polygon = Polygon.by_points(self.polygon_pointlist)
		self.is_invalid = False
		
		self.intersecting_geometry = []
		self.index_points = []
	
	def cull_duplicates( self, object_list ):
		seen = set()
		seen_add = seen.add
		return [ x for x in object_list if x not in seen and not seen_add(x)]
   
	def find_intersecting_geometry_list(self):
		full_geometry_list = []
		for geometry in self.point_checks:
			full_geometry_list.extend(geometry.stored_geometry)
		
		clean_geometry_list = self.cull_duplicates(full_geometry_list)
		
		for object in clean_geometry_list:
			boolean_intersect = object.does_intersect(self.polygon)
			if boolean_intersect == True:
				self.intersecting_geometry.append(object)
				self.is_invalid = True
		return 
	
	def find_corresponding_point(self,geometry):
		shortest_dist = None
		
		for i in range(len(self.point_checks)):
			closest_point_on_object = geometry.get_closest_point(self.point_checks[i].top_point)
			dist = self.point_checks[i].top_point.distance_to(closest_point_on_object)
		
			if shortest_dist == None:
				shortest_dist = dist
				index_to_move = i
				continue
			
			if dist <= shortest_dist:
				index_to_move = i
			 
		return index_to_move
	
	def does_intersect(self, number):

		for object in self.intersecting_geometry:
			boolean_intersect = object.does_intersect(self.polygon)
			if boolean_intersect == True and number == 0:
				self.is_invalid = True
				continue
			
			if boolean_intersect == True and number == 1:
				self.is_invalid = True
				self.index_points.append(self.find_corresponding_point(object))
			
		#self.is_invalid = geo1.does_intersect(self.polygon) or geo2.does_intersect(self.polygon) or geo3.does_intersect(self.polygon) or geo4.does_intersect(self.polygon)
		return 
	
	
	#create boolean for up or down. SO if it starts out as false, them move it up point.? if true move down points?
	def adjust_point(self):
		
		self.find_intersecting_geometry_list()
		self.does_intersect(1)
		
		if not self.index_points:
			return
		
		while self.is_invalid == True:
			for index in self.index_points:
				self.point_checks[index].top_point.set_z(self.point_checks[index].top_point.z() - 1)
			self.polygon.update_vertices(self.polygon_pointlist)
			self.is_invalid = False
			self.does_intersect(0)
			
		return #self.point_checks[0].top_point



#########################################################

output_debug_new = []		

for i in range(int(x_number) ):
	for j in range(int(y_number) ):
		if i == 0 and j ==0:
			panel = Check_SurfacePanel_intersection([grid[i][j], grid[i+1][j], grid[i+1][j+1], grid[i][j+1]])
			#output_debug_new.append(grid[i][j].top_point)
			panel.adjust_point()
			#grid[i][j].top_point = panel.adjust_point()
			output_debug_new.append( panel.polygon)

"""
#create panels.
for i in range(int(x_number) ):
 	for j in range(int(y_number) ):
 		new_polygon_pointlist = PointList([grid[i][j].top_point, grid[i+1][j].top_point, grid[i+1][j+1].top_point, grid[i][j+1].top_point])
 		output_debug_new.append(Polygon.by_points(new_polygon_pointlist))
"""

#Assign your output to the OUT variable
OUT = [output_debug_geometry, output_debug_new]
