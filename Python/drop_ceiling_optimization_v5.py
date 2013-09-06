from Autodesk.LibG import *

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

class PointCheck:
	def __init__(self, _point, _panel_size):
		self.point = _point
		self.stored_geometry = []
		self.stored_points = []
		self.panel_size = _panel_size
		self.top_point = None
	
	
	def objects_within_proximity( self, geometry_list ):	#stores whatever ceiling objects are with in proximity
		lowest_z = None
		
		for object in geometry_list:
			object_point = object.get_closest_point(self.point)
			test_point = Point.by_coordinates(self.point.x(), self.point.y(), object_point.z())
			dist = test_point.distance_to(object_point)
			
			if dist > (self.panel_size/2): #half of IN spacing.
				continue
			
			self.stored_geometry.append(object)
			self.stored_points.append([object_point, object_point.z()])
			
		return
	
	def set_closest_geometry( self, geometry_list ):  #this one only finds the closest point. we need one that finds the proximitiy.
		
		self.objects_within_proximity(geometry_list)
		self.stored_points.sort(key=lambda sublist: sublist[1])
		
		self.top_point = Point.by_coordinates(self.point.x(), self.point.y(), self.stored_points[0][0].z())
		
		return #closest_geometry
		

##########################################################################

min_point = IN[0][0] #min point & also start point
max_point = IN[0][1] #max point

panel_sizing = IN[1] # Panel Sizing
reference_geo = []
reference_geo.extend(IN[2]) #standard geom to avoid.
reference_geo.append(IN[0][2]) #top_surface

xlength = max_point.x() - min_point.x()
ylength = max_point.y() - min_point.y()
#get geometery from get_geo.

file_name = IN[3]

x_number = round(xlength/panel_sizing)
y_number = round(ylength/panel_sizing)

newx_spacing = xlength / x_number
newy_spacing = ylength / y_number


grid = [ [ (y,x) for y in range( int(y_number)+1) ] for x in range( int(x_number) + 1 ) ]
output_debug_geometry = []

for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j] = PointCheck(Point.by_coordinates((i*newx_spacing)+ min_point.x(), (j*newy_spacing) + min_point.y() , 0.0) , panel_sizing )

for i in range(int(x_number) + 1):
	for j in range(int(y_number) + 1):
		grid[i][j].set_closest_geometry(reference_geo)
		output_debug_geometry.append(grid[i][j].top_point)



#########################################################

output_debug_new = []		


for i in range(int(x_number) ):
	for j in range(int(y_number) ):
		panel = Polygon.by_points(PointList([grid[i][j].top_point, grid[i+1][j].top_point, grid[i+1][j+1].top_point, grid[i][j+1].top_point]))
		output_debug_new.append( panel)


f = open(file_name, "w")

bspline_surfacelist = []
for i in range(int(x_number)+1):
	for j in range(int(y_number)+1):
		f.write( str(grid[i][j].top_point.x()) + "," + str(grid[i][j].top_point.y()) + "," + str(grid[i][j].top_point.z()) )
		if j != (y_number):
			f.write("/")
	if i != (x_number):
		f.write("\n")
f.close()
#output_debug_new.append( BSplineSurface.by_points(PointList(bspline_pointlist), int(x_number) +1, int(y_number) +1) )


#create panels.
for i in range(int(x_number) ):
 	for j in range(int(y_number) ):
 		new_polygon_pointlist = PointList([grid[i][j].top_point, grid[i+1][j].top_point, grid[i+1][j+1].top_point, grid[i][j+1].top_point])
 		output_debug_new.append(Polygon.by_points(new_polygon_pointlist))


#Assign your output to the OUT variable
OUT =  output_debug_new #bspline_surfacelist #output_debug_new#[output_debug_geometry, output_debug_new]
