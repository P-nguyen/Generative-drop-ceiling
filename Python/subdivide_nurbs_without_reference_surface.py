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
	"""	
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


#needs to be feed correctly
def subdivide_surface( reference_surf, _pointlist ):
	#_pointlist = rotate_points( _pointlist )

	_pointlist.append(_pointlist[0])
	midpts = [0,0,0,0,0]
	for i in range(4):
		midpts[i] = get_midpoint(_pointlist[i], _pointlist[i+1] )
	
	midpts[4] = get_midpoint(midpts[0],midpts[2])
	
	
	#lift points
	
	liftpts = []
	liftmidpts = []

	mag = -20.0
        
	for j in range(5):
	#i might have to replace Surface with srf.normalblahblah
		vec = reference_surf.normal_at_point( _pointlist[j] )
		liftpts.append(add_vector( _pointlist[j], vec , mag ))
		#liftpts.append(_pointlist[j])
		vec = reference_surf.normal_at_point( midpts[j] )
		#liftmidpts.append( midpt[j])
		liftmidpts.append(add_vector( midpts[j], vec, mag ))

	new_surfaces = []
	
	# non lift points
	ptlist = PointList( [  midpts[0], _pointlist[1],  midpts[1],  midpts[4] ] )
	new_surfaces.append(Polygon.by_vertices( ptlist))
	# end of non lift points

	ptlist = PointList([ liftpts[0], liftmidpts[0], liftmidpts[4], liftmidpts[3] ])
	new_surfaces.append( Polygon.by_vertices( ptlist))

	ptlist = PointList([ liftmidpts[3], liftmidpts[4], liftmidpts[2], liftpts[3] ])
	new_surfaces.append( Polygon.by_vertices( ptlist))
	
	ptlist = PointList([ liftmidpts[4], liftmidpts[1], liftpts[2], liftmidpts[2] ])
	new_surfaces.append( Polygon.by_vertices( ptlist))
	

	side = []

	ptlist = PointList([ midpts[4], midpts[0], liftmidpts[0], liftmidpts[4] ])
	side.append( Polygon.by_vertices( ptlist ))
	
	ptlist = PointList([ midpts[1], midpts[4], liftmidpts[4], liftmidpts[1] ])
	side.append( Polygon.by_vertices( ptlist ))

	return [new_surfaces, side]

##########################################
iterations = 1


input_surfaces = []
input_surfaces.extend(IN)


new_surfaces = []
new_sides = []
surface_points = []


for obj in input_surfaces:
	surface_points.append(corner_points(obj))
	
	
for i in range(len(input_surfaces)):
	#new_surfaces.extend(subdivide_surface( input_surfaces[i], surface_points[i] ))
	#new_surfaces.extend( subdivide_surface( reference_surface, surface_points[i] )[0] )
	temp_surfaces = subdivide_surface( input_surfaces[i], surface_points[i] )
	new_surfaces.extend( temp_surfaces[0] )
	new_sides.extend( temp_surfaces[1] )
	
"""

for j in range(iterations):
	recursive_list = []
	
	for surface in new_surfaces:
		pts = surface_points( surface )
		recursive_list.extend( subdivide_surface( reference_surface, pts ))
		
		new_surfaces = recursive_list
"""

#Assign your output to the OUT variable
OUT = [ new_surfaces, new_sides ]
