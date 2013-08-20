import sys
path = 'C:\\Users\\t_nguyp\\Desktop\\Dynamo\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Vector

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN
polygon_list = IN[0]

def move_point_byvector( point, vector, magnitude ):
    vector_copy = Vector.by_coordinates(vector.x(),vector.y(),vector.z())
    vector_copy.normalize()
       
    newpoint = [0,0,0]
    newpoint[0] = point.x() + (vector_copy.x() * magnitude)
    newpoint[1] = point.y() + (vector_copy.y() * magnitude)
    newpoint[2] = point.z() + (vector_copy.z() * magnitude)
    
    finalpt = Point.by_coordinates(newpoint[0], newpoint[1], newpoint[2])
    return finalpt

def add_two_vectors( vector_1,vector_2 ):
    vector_1.normalize()
    vector_2.normalize()
    
    vec_x = (vector_1.x() + vector_2.x()) / 2 
    vec_y = (vector_1.y() + vector_2.y()) / 2 
    vec_z = (vector_1.z() + vector_2.z()) / 2 
    
    final_vec = Vector.from_xyz( vec_x, vec_y, vec_z )
    
    return final_vec
            
def create_connection_plate( Point_A, Point_B, vector, setback):
    
    curve = Line.by_start_point_end_point (Point_A, Point_B)
    dist = curve.length ()
    pt1 = curve.point_at_distance (setback)
    pt2 = curve.point_at_distance (dist - setback)
    
    v1 = move_point_byvector( pt1, vector, -plate_protrusion ) #-
    v2 = move_point_byvector( pt2, vector, -plate_protrusion ) #-
    v3 = move_point_byvector( pt2, vector, panel_thickness ) #+ The 1 is for  the hanger? do we need it? 
    v4 = move_point_byvector( pt1, vector, panel_thickness ) #+
    
    Surface = Polygon.by_points( PointList([v1,v2,v3,v4]) )
    return Surface

def check_if_plate_exist( new_plate, exisitng_plates ):
	boolean = False
	centroid_1 = new_plate.point_at_parameter( 0.5,0.5 )
	
	if existing_plates:
		for plate in existing_plates:
			centroid_2 = plate.point_at_parameter( 0.5,0.5 )
			dist = centroid_1.distance_to(centroid_2)
			if dist < .5:
				boolean = True
			
	return boolean
	
def intersect_plane_to_solid( polygons, point_indexs, panel_thickness ):
    i = point_indexs[0]
    j = point_indexs[1]
    
    poly_points = polygons[i][j].vertices()
    center_norm = polygons[i][j].normal_at_parameter (0.5, 0.5)
    
    plates = []
    #points = []
    #poly1
    if j-1 >= 0: 
        adjacent_norm = polygons[i][j-1].normal_at_parameter (0.5, 0.5)
		
        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[1], edge_normal, 10 )
        test_plate = create_connection_plate( poly_points[0], poly_points[1], edge_normal, setback)
        check = check_if_plate_exist( test_plate, existing_plates )
        if check == False:
			plates.append(test_plate)
    
    #poly2    
    if i+1 <= len(polygons)-1:
        adjacent_norm = polygons[i+1][j].normal_at_parameter (0.5, 0.5)
        
        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[2], edge_normal, 10 )
        test_plate = create_connection_plate( poly_points[1], poly_points[2], edge_normal, setback)
        check = check_if_plate_exist( test_plate, existing_plates )
        if check == False:
        	plates.append(test_plate)
    
    #poly3 
    if j+1 <= len(polygons[0])-1:
        adjacent_norm = polygons[i][j+1].normal_at_parameter (0.5, 0.5)
        
        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[3], edge_normal, 10 )
        test_plate = create_connection_plate( poly_points[2], poly_points[3], edge_normal, setback)
        check = check_if_plate_exist( test_plate, existing_plates )
        if check == False:
        	plates.append(test_plate)
        
    #poly4 
    if i-1 >= 0:
        adjacent_norm = polygons[i-1][j].normal_at_parameter (0.5, 0.5)
		
        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[0], edge_normal, 10 )
        test_plate = create_connection_plate( poly_points[3], poly_points[0], edge_normal, setback)
        check = check_if_plate_exist( test_plate, existing_plates )
        if check == False:
        	plates.append(test_plate)
    
    return plates

####Main####
panel_thickness = IN[1] /12 #for DYNAMO SANDBOX  # for REVIT FEET 0.166

#plate specific variables
plate_protrusion = 0.25 # how much the plate pops out // look at DEF create_connection_plate
setback = 1 # shortens the plate to avoid conflict at corners
existing_plates = []


#debug_plates = []
#create new grid of points that are correctly offset from the original pointlist.
for i in range(len(polygon_list)):
    for j in range(len(polygon_list[0])):
       #debug_planes.extend( intersect_plane( polygon_list, [i,j] ) )
       result = intersect_plane_to_solid( polygon_list, [i,j], panel_thickness )
       existing_plates.extend(result)
       #debug_plates.extend( result)


OUT = existing_plates #polygon_list# ,debug_planes