import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

def corner_points(surf):
	
	"""
	ptlist = [0, 0, 0, 0]
	ptlist[0] = surf.point_at_parameter(0.0, 0.0)
	ptlist[1] = surf.point_at_parameter(1.0, 0.0)
	ptlist[2] = surf.point_at_parameter(1.0, 1.0)
	ptlist[3] = surf.point_at_parameter(0.0, 1.0)
	
	"""
	#if polygon then use this
	polyvert = surf.vertices()
	
	ptlist = []
	for i in range(polyvert.Count):
		ptlist.append(polyvert[i])
	
	return ptlist


def get_midpoint(pt1,pt2):
	
	midPt = [0,0,0]
	
	midPt[0] = (pt1.x() + pt2.x()) /2
	midPt[1] = (pt1.y() + pt2.y()) /2
	midPt[2] = (pt1.z() + pt2.z()) /2
	
	Final_MidPoint = Point.by_coordinates(midPt[0], midPt[1], midPt[2])
	return Final_MidPoint

def add_vector( point, vector, magnitude ):
	vector.normalize()
	
	newpoint = [0,0,0]
	newpoint[0] = point.x() + (vector.x() * magnitude)
	newpoint[1] = point.y() + (vector.y() * magnitude)
	newpoint[2] = point.z() + (vector.z() * magnitude)
	
	finalpt = Point.by_coordinates(newpoint[0], newpoint[1], newpoint[2])
	return finalpt

def rotate_points( pointlist, rotations ):
	for i in range(rotations):
		last_point = pointlist.pop()
		pointlist.insert(0,last_point)
	return pointlist
	
#needs to be feed correctly
def subdivide_surface( reference_surf, _pointlist ):
	_pointlist = rotate_points( _pointlist, number_of_rotations )

	_pointlist.append(_pointlist[0])
	midpts = [0,0,0,0,0]
	for i in range(4):
		midpts[i] = get_midpoint(_pointlist[i], _pointlist[i+1] )
	
	midpts[4] = get_midpoint(midpts[0],midpts[2])
	
	new_surfaces = []
	
	# non lift points
	#ptlist = PointList( [  midpts[0], _pointlist[1],  midpts[1],  midpts[4] ] )
	#new_surfaces.append(Polygon.by_vertices( ptlist))
	# end of non lift points

	ptlist = PointList([ _pointlist[0], midpts[0], midpts[4], midpts[3] ])
	new_surfaces.append( Polygon.by_vertices( ptlist))

	ptlist = PointList([ midpts[3], midpts[4],  midpts[2], _pointlist[3] ])
	new_surfaces.append( Polygon.by_vertices( ptlist))
	
	ptlist = PointList([ midpts[4],  midpts[1], _pointlist[2],  midpts[2] ])
	new_surfaces.append( Polygon.by_vertices( ptlist))
	
	
		
	return new_surfaces

##########################################
iterations = 1


input_surfaces = []
input_surfaces.extend(IN)


new_surfaces = []
new_sides = []
surface_points = []
number_of_rotations = 0

for obj in input_surfaces:
	surface_points.append(corner_points(obj))
	
	
for i in range(len(input_surfaces)):
	#new_surfaces.extend(subdivide_surface( input_surfaces[i], surface_points[i] ))
	#new_surfaces.extend( subdivide_surface( reference_surface, surface_points[i] )[0] )
	temp_surfaces = subdivide_surface( input_surfaces[i], surface_points[i] )
	number_of_rotations =+ 1
	if number_of_rotations > 5:
		number_of_rotations == 0
	new_surfaces.extend( temp_surfaces )
	#new_sides.extend( temp_surfaces[1] )
	

for j in range(iterations):
	recursive_list = []
	
	for surface in new_surfaces:
		pts = corner_points( surface )
		recursive_list.extend( subdivide_surface( surface, pts ))
		number_of_rotations =+ 1
		if number_of_rotations > 5:
			number_of_rotations == 0
		
	new_surfaces = recursive_list


#Assign your output to the OUT variable
OUT = new_surfaces
