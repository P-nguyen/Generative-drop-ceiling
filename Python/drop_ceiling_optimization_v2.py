from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry
#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

#class is needed for each point? 
	#class info contains the point, and a boolean telling if it is still moveable
class PointCheck:
	def __init__(self, _point):
		self.point = _point
		self.closest_geometry = None
		self.closest_geometry_distance = None
		self.closest_geometry_point = None
		self.top_point = None
		#self.point_direction = None #possible will need to give the point a direction of movement.

		
	def set_closest_geometry( self, geometry_list ): 
		for object in geometry_list:
			
			object_point = object.get_closest_point(self.point)
			dist = self.point.distance_to(object_point)
			
			
			if self.closest_geometry == None:
				self.closest_geometry = object
				self.closest_geometry_point = object_point
				self.closest_geometry_distance = dist
				continue

			if dist >= self.closest_geometry_distance:
				continue
			
			self.closest_geometry_distance = dist
			self.closest_geometry = object
			self.closest_geometry_point = object_point
			
		return #closest_geometry
	
	def set_top_point(self):
		if self.closest_geometry_point == None:
			return
		
		self.top_point = Point.by_coordinates(self.point.x(), self.point.y(), self.closest_geometry_point.z() )


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
output_debug_geometry = []
#create grid spacing based on input and distances.
#grid_points = []
for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j] = PointCheck(Point.by_coordinates(i*newx_spacing, j*newy_spacing, 0.0))
		#output_debug_geometry.append(Point.by_coordinates(i*newx_spacing, j*newy_spacing, 0.0))

for i in range(int(x_number) + 1):
		for j in range(int(y_number) + 1):
			grid[i][j].set_closest_geometry(reference_geo)
			grid[i][j].set_top_point()
			output_debug_geometry.append(grid[i][j].top_point)
			#l = Line.by_start_point_end_point(grid[i][j].point, grid[i][j].top_point)
			#output_debug_geometry.append(l)
			



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

	"""		
	#*new addition needs to constantly check objects. to see if it can move up or down, this creates the directional push.

	def find_closest_panel_geometry(self, reference_geometry ): #must add all references to see what the closes obj is now that the point is adjusted.
		previous_distance = None		
		for object in reference_geometry:
			object_point = object.get_closest_point(self.point_checks[0].top_point)
			dist = self.point_checks[0].top_point.distance_to(object_point)			
			
			if dist < previous_distance:
				possible_intersecting_geometry = object
			
		return possible_intersecting_geometry, and direction. for each point.
	"""
	
	def does_intersect(self):
		# Geometry.does_intersect(Geometry)
		# four pieces of ceiling geometry
		geo1 = self.point_checks[0].closest_geometry
		geo2 = self.point_checks[1].closest_geometry
		geo3 = self.point_checks[2].closest_geometry
		geo4 = self.point_checks[3].closest_geometry
		
		self.is_invalid = geo1.does_intersect(self.polygon) or geo2.does_intersect(self.polygon) or geo3.does_intersect(self.polygon) or geo4.does_intersect(self.polygon)
		return self.is_invalid
	
	""" OLD
	def adjust_point(self):
		self.does_intersect()
		while self.is_invalid == True:
			self.point_checks[0].top_point.set_z(self.point_checks[0].top_point.z() - 1)
			self.polygon.update_vertices(self.polygon_pointlist)
			self.does_intersect()
			#move the top_point down until it clears.
		return self.point_checks[0].top_point
	"""
	
	#create boolean for up or down. SO if it starts out as false, them move it up point.? if true move down points?
	def adjust_point(self):
		self.does_intersect()
		while self.is_invalid == True:
			for i in range(len(self.point_checks)): #needs direction. 
				self.point_checks[i].top_point.set_z(self.point_checks[i].top_point.z() - 1)
			self.polygon.update_vertices(self.polygon_pointlist)
			self.does_intersect()
			#move the top_point down until it clears.
		return #self.point_checks[0].top_point


# 	def pannels_intersect(surface_grid):
# 		for i in range(int(x_number) ):
# 			for j in range(int(y_number) ):
# 				if surface_grid[i][j].does_intersect()
# 					return True
# 		return False
# 	
# 	surface_grid = [ [ (y,x) for y in range( int(y_number)) ] for x in range( int(x_number) ) ]		
# 	
# 	# rig up the points into surfaces
# 	
# 	# 
# 	
# 	while pannels_intersect(surface_grid) == True:
# 		# move top point down
# 		for i in range(int(x_number) ):
# 			for j in range(int(y_number) ):
# 				if surface_grid[i][j].is_invalid:
# 					# fix something here, move top_point down

output_debug_new = []		

for i in range(int(x_number) ):
 	for j in range(int(y_number) ):
 		Panel = Check_SurfacePanel_intersection([grid[i][j], grid[i+1][j], grid[i+1][j+1], grid[i][j+1]])
 		grid[i][j].top_point = Panel.adjust_point()
 		output_debug_new.append( Panel.polygon)

"""	
#create panels.
for i in range(int(x_number) ):
 	for j in range(int(y_number) ):
 		output_debug_new.append(Polygon.by_points(PointList([grid[i][j].top_point, grid[i+1][j].top_point, grid[i+1][j+1].top_point, grid[i][j+1].top_point])))
"""

#Assign your output to the OUT variable
#OUT = testpt #grid_points #grid_points[0].boolean


OUT = [output_debug_geometry, output_debug_new]

