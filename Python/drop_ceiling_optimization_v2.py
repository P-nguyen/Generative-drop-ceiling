from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry
#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

#class is needed for each point? 
	#class info contains the point, and a boolean telling if it is still moveable
class Point_Check:
	def __init__(self, _point):
		self.point = _point
		self.boolean = False 
		self.stored_geometry = []
	
	"""	
	def closest_geometry( self, geometry_list ): #were saying F this portion and just get an estimation.
		old_distance = 50000.0
		#
		for obj in geometry_list:
			closest_point = obj.get_closest_point(self.point)
			distance = closest_point.distance_to(self.point)
			if distance < old_distance:
				old_distance = distance
		
		return old_distance
	"""
	
	def closest_geometry( self, geometry_list ): #were saying F this portion and just get an estimation.
		old_distance = 50000.0
		resulting_point = []
		#
		for obj in geometry_list:
			closest_point = obj.get_closest_point(self.point)
			distance = closest_point.distance_to(self.point)
			if distance < old_distance:
				old_distance = distance
				resulting_point = closest_point
		
		return resulting_point
	
	def objs_by_proximity(self, geometry_list): # this code will find the relative objects with in 4' and set the lowest pt as your standard Z
		test_point = self.point		
		lowest_z = 50000.0
		
		for obj in geometry_list:
			#check objs cpt
			closest_point = obj.get_closest_point(self.point)
			test_point.set_z(closest_point.z())
			
			distance = closest_point.distance_to(self.point)
			if distance < 48:
				self.stored_geometry.append(obj)
				if closest_point.z() < lowest_z:
					lowest_z = closest_point.z()
		
		self.point.set_z(lowest_z)
		return 
	
	def point_adjustment(self):
		closest_point = self.closest_geometry(self.stored_geometry)
		distance = closest_point.distance_to(self.point)
		
		while distance < 12 or distance > 14:			
			if distance < 12:
				self.point.set_z( self.point.z() - 1)
			if distance > 14: 
				self.point.set_z( self.point.z() + 1)
			
			#closest_point = self.closest_geometry(self.stored_geometry)
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
#create grid spacing based on input and distances.
#grid_points = []
for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j] = Point_Check(Point.by_coordinates(i*newx_spacing, j*newy_spacing, 0.0))

testpt = []
count = 1
"""
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
"""

for i in range(int(x_number) + 1):
		for j in range(int(y_number) + 1):
			grid[i][j].objs_by_proximity( reference_geo )
			grid[i][j].point_adjustment()
			
if count == 1:
	for i in range(int(x_number) ):
		for j in range(int(y_number) ):
			#testpt.append(grid[i][j].point)
			pointlist = PointList([ grid[i][j].point, grid[i+1][j].point, grid[i+1][j+1].point, grid[i][j+1].point ])
			testpt.append( Polygon.by_points( pointlist ) )
#Assign your output to the OUT variable
OUT = testpt #grid_points #grid_points[0].boolean