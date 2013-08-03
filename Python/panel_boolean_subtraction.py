import System
from System import *
import sys
path = 'C:\\Users\\t_nguyp\\Desktop\\Dynamo\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Vector,Solid

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN
input_solids = IN


def create_polygon(face): 
	face_points = []
	vertices = face.get_vertices()
	
	for v in vertices:
		face_points.append(v.get_point_geometry() )
	ptlist = PointList([face_points[0],face_points[1],face_points[3],face_points[2]])
	return BSplineSurface.by_points(ptlist,2,2)

##########################################################################################################
#### making grid to boolean from solid

def move_point_byvector( point, vector, magnitude ):
    vector_copy = Vector.by_coordinates(vector.x(),vector.y(),vector.z())
    vector_copy.normalize()
       
    newpoint = [0,0,0]
    newpoint[0] = point.x() + (vector_copy.x() * magnitude)
    newpoint[1] = point.y() + (vector_copy.y() * magnitude)
    newpoint[2] = point.z() + (vector_copy.z() * magnitude)
    
    finalpt = Point.by_coordinates(newpoint[0], newpoint[1], newpoint[2])
    return finalpt

def enlarge_polygon( polygon ):
    vertex_list = []
    for point in polygon.vertices():
        vertex_list.append(point)
    vertex_list.extend(vertex_list)
    
    point = []    
    for i in range(4):
        vectorx = vertex_list[i].x() - vertex_list[i+2].x() 
        vectory = vertex_list[i].y() - vertex_list[i+2].y()
        vectorz = vertex_list[i].z() - vertex_list[i+2].z()
    
        vectest = Vector.from_xyz(vectorx, vectory, vectorz)
        vectest.normalize()
        
        point.append(move_point_byvector( vertex_list[i], vectest, 2 ))
        
    Ptlist = PointList([ point[0], point[1], point[2], point[3] ])    
    new_polygon = Polygon.by_points(Ptlist)
    
    return new_polygon

def find_panel(solids, centroid):
    v_point = Point.by_coordinates(centroid.x(), centroid.y(), (centroid.z()+ 20))
    line =  Line.by_start_point_end_point(centroid, v_point)
    
    final_solid = None
    for obj in solids:
        check = line.does_intersect(obj)
        if check == True:
            final_solid = obj
            
    return final_solid   


##########################################################################################################
#### create points off of bottom surface
final_solid_list = []

for solid in input_solids:
	
	solid_surfaces = solid.get_faces ()
	
	srf_area_list = []
	for surface in solid_surfaces:
		srf_area_list.append( [surface, surface.get_area()] )
	
	sorted_surfaces = sorted(srf_area_list, key = lambda x: x[1], reverse = True)
	
	clean_list = []
	for i in range(2):
		clean_list.append([ sorted_surfaces[i][0] , sorted_surfaces[i][0].get_centroid().z() ])
		
	final_sort_list = sorted(clean_list, key = lambda x: x[1], reverse = True)
	
	#top_surface = create_polygon(final_sort_list[0][0])
	bottom_surface = create_polygon(final_sort_list[1][0])

	div_number = 3.0
	grid_spacing = 1.0/div_number
	
	bottom_grid  = [ [ (y,x) for y in range( int(div_number)+1) ] for x in range( int(div_number) + 1 ) ]
	
	for i in range(int(div_number) + 1):
		for j in range(int(div_number) + 1):
			surf_point = bottom_surface.point_at_parameter ( grid_spacing * i , grid_spacing * j )
			vec = bottom_surface.normal_at_parameter ( grid_spacing * i, grid_spacing * j)
			bottom_grid[i][j] = move_point_byvector( surf_point, vec, 5 )
			
	final_solid = solid
	#Thickend_panel = []
	rand = Random()
	for i in range(int(div_number) ):
		for j in range(int(div_number) ):
			panel = Polygon.by_points(PointList([bottom_grid[i][j], bottom_grid[i+1][j], bottom_grid[i+1][j+1], bottom_grid[i][j+1]]))
			panel = enlarge_polygon( panel )
			
			rand_num = (rand.Next() % 1000000) / 1000000.0
			Thickend_panel = panel.thicken(rand_num * 15)
			final_solid = final_solid.subtract_from(Thickend_panel, True, True, True)	
			final_solid = final_solid[0]

	final_solid_list.append(final_solid)
#Assign your output to the OUT variable
OUT =  final_solid_list