import sys
path = 'C:\\Users\\t_nguyp\\Desktop\\Dynamo\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Vector,Solid

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

solid = IN

solid_surfaces = solid.get_faces ()

srf_area_list = []
for surface in solid_surfaces:
	srf_area_list.append( [surface, surface.get_area()] )

sorted_surfaces = sorted(srf_area_list, key = lambda x: x[1], reverse = True)

clean_list = []
for i in range(2):
	clean_list.append([ sorted_surfaces[i][0] , sorted_surfaces[i][0].get_centroid().z() ])
	
final_sort_list = sorted(clean_list, key = lambda x: x[1], reverse = True)

def create_polygon(face): 
	face_points = []
	vertices = face.get_vertices()
	
	for v in vertices:
		face_points.append(v.get_point_geometry() )
	ptlist = PointList([face_points[0],face_points[1],face_points[2],face_points[3]])
	return Polygon.by_points(ptlist)

top_surface = create_polygon(final_sort_list[0][0])
bottom_surface = create_polygon(final_sort_list[1][0])
#offset_surfaces
test = top_surface.offset(3.0)
test2 = bottom_surface.offset(-3.0)

#Assign your output to the OUT variable
OUT = top_surface, bottom_surface, test,test2