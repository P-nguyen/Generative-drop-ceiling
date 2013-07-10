from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry
#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

#class is needed for each point? 
	#class info contains the point, and a boolean telling if it is still moveable
class PointCheck:
	def __init__(self, _point):
		self.point = _point
		self.boolean = False 
		self.stored_geometry = []
		self.closest_geometry = None
		self.closest_geometry_distance = None
		self.closest_geometry_point = None
		self.top_point = None
	
	"""	
	def set_closest_geometry( self, geometry_list ): #were saying F this portion and just get an estimation.
		old_distance = 50000.0
		#
		for obj in geometry_list:
			closest_point = obj.get_closest_point(self.point)
			distance = closest_point.distance_to(self.point)
			if distance < old_distance:
				old_distance = distance
		
		return old_distance
	"""
	
	def set_closest_geometry( self, geometry_list ): #were saying F this portion and just get an estimation.
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
			
	def set_top_point(self):
		if self.closest_geometry_point == None:
			return
		
		self.top_point = Point.by_coordinates(self.point.x(), self.point.y(), self.closest_geometry_point.z())
	
	def objs_by_proximity(self, geometry_list): # this code will find the relative objects with in 4' and set the lowest pt as your standard Z
		test_point = self.point		
		lowest_z = 50000.0
		
		for obj in geometry_list:
			#check objs cpt
			closest_point = obj.get_closest_point(self.point)
			test_point.set_z(closest_point.z())
			
			distance = closest_point.distance_to(self.point)
			if distance > 48:
				continue
			if closest_point.z() < lowest_z:
				self.stored_geometry.append(obj)
				lowest_z = closest_point.z()
		
		self.point.set_z( lowest_z - 2 )
		return 
	
	def point_adjustment(self):
		closest_point = self.set_closest_geometry(self.stored_geometry)
		distance = closest_point.distance_to(self.point)
		
		while (distance < 12) or (distance > 14):			
			if distance < 12:
				self.point.set_z( self.point.z() - 1)
			if distance > 14: 
				self.point.set_z( self.point.z() + 1)
			#closest_point = self.set_closest_geometry(self.stored_geometry)
			distance = closest_point.distance_to(self.point)
			#then i have to check the new distance.
			
		return 
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
		output_debug_geometry.append(Point.by_coordinates(i*newx_spacing, j*newy_spacing, 0.0))

testpt = []
count = 1
"""
while count > 0:
	count = 0
	#while there are still points.
	for i in range(int(x_number) + 1):
		for j in range(int(y_number) + 1):
			if grid[i][j].boolean == False:
				check = grid[i][j].set_closest_geometry( reference_geo )
				if check < 12:
					grid[i][j].boolean == True
				else:
					grid[i][j].point.set_z( grid[i][j].point.z() + 1)
					count += 1
"""

for i in range(int(x_number) + 1):
		for j in range(int(y_number) + 1):
			print "hi"
			grid[i][j].set_closest_geometry(reference_geo)
			grid[i][j].set_top_point()
			output_debug_geometry.append(grid[i][j].top_point)
			#l = Line.by_start_point_end_point(grid[i][j].point, grid[i][j].top_point)
			#output_debug_geometry.append(l)
			#grid[i][j].point_adjustment()
			
# if count == 1:
# 	for i in range(int(x_number) ):
# 		for j in range(int(y_number) ):
# 			print "hi"
# 			#testpt.append(grid[i][j].point)
# 			#pointlist = PointList([ grid[i][j].point, grid[i+1][j].point, grid[i+1][j+1].point, grid[i][j+1].point ])
# 			#testpt.append( Polygon.by_points( pointlist ) )
			
	
class SurfacePannel:
	def __init__(self, point_checks):
		self.point_checks = point_checks
		p1 = point_checks[0].top_point
		p2 = point_checks[1].top_point
		p3 = point_checks[2].top_point
		p4 = point_checks[3].top_point
		self.polygon = Polygon.by_points(PointList([p1, p2, p3, p4]))
		self.is_invalid = False
		
	def does_intersect(self):
		# Geometry.does_intersect(Geomtery)
		# four pieces of ceiling geometry
		geo1 = self.point_checks[0].closest_geometry
		geo2 = self.point_checks[1].closest_geometry
		geo3 = self.point_checks[2].closest_geometry
		geo4 = self.point_checks[3].closest_geometry
		
		self.is_invalid = geo1.does_intersect(self.polygon) or geo2.does_intersect(self.polygon) or geo3.does_intersect(self.polygon) or geo4.does_intersect(self.polygon)
		
		return self.is_invalid
		
		
def pannels_intersect(surface_grid):
	for i in range(int(x_number) ):
		for j in range(int(y_number) ):
			if surface_grid[i][j].does_intersect()
				return True
	return False
	
surface_grid = [ [ (y,x) for y in range( int(y_number)) ] for x in range( int(x_number) ) ]		

# rig up the points into surfaces

# 

while pannels_intersect(surface_grid) == True:
	# move top point down
	for i in range(int(x_number) ):
		for j in range(int(y_number) ):
			if surface_grid[i][j].is_invalid:
				# fix something here, move top_point down
				
	

#Assign your output to the OUT variable
#OUT = testpt #grid_points #grid_points[0].boolean

OUT = output_debug_geometry

