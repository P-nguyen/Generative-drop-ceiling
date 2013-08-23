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
rand = Random()

def create_surface(face): 
	face_points = []
	vertices = face.get_vertices()
	
	for v in vertices:
		face_points.append(v.get_point_geometry() )
	ptlist = PointList([face_points[0],face_points[1],face_points[3],face_points[2]])
	return BSplineSurface.by_points(ptlist,2,2)

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
        
        point.append(move_point_byvector( vertex_list[i], vectest, 0.2 ))
        
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

def panel_thickness(surface_1, surface_2):
	pt1 = surface_1.point_at_parameter ( 0.5,0.5 )
	pt2 = surface_2.point_at_parameter ( 0.5,0.5 )
	thickness = pt1.distance_to(pt2)
	return thickness

def controlled_random_thickness( total_thickness, random ):
	rand_num = (random.Next() % 1000000) / 1000000.0
	if 0.0 <= rand_num <= 0.35:
		final_thickness = 0.0
		
	if 0.35 < rand_num <= 0.75:
		final_thickness = total_thickness * 0.3
		
	if 0.75 < rand_num <= 0.9:
		final_thickness = total_thickness * 0.4
		
	if 0.9 < rand_num <= 1.0:
		final_thickness = total_thickness * 0.5
		# cut through panel.

	return final_thickness

def subdivide_panel( pointlist, random ):
	rand_num = (random.Next() % 1000000) / 1000000.0
	panels = []
	
	if 0 <= rand_num <= 0.5:
		panel = Polygon.by_points(pointlist)
		panels.append(panel)
	else:
		ptlist = PointList([pointlist[3],pointlist[2],pointlist[0],pointlist[1]])
		panel = BSplineSurface.by_points(ptlist,2,2)
		grid_spacing = 1.0/2
		points  = [ [ (y,x) for y in range(3) ] for x in range(3) ]
		for i in range(3):
			for j in range(3):
				points[i][j] = panel.point_at_parameter ( grid_spacing * i , grid_spacing * j )
		for k in range(2):
			for l in range(2):
				panels.append(Polygon.by_points(PointList([points[k][l], points[k+1][l], points[k+1][l+1], points[k][l+1]])))
			  
	return panels
##########################################################################################################
#### create points off of bottom surface
final_solid_list = []
count = 0

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
	
	#top srf is used to find the thickness of the panel.
	top_surface = create_surface(final_sort_list[0][0])
	bottom_surface = create_surface(final_sort_list[1][0])
	
	thickness = panel_thickness(top_surface, bottom_surface)
	
	div_number = 3.0
	grid_spacing = 1.0/div_number
	
	bottom_grid  = [ [ (y,x) for y in range( int(div_number)+1) ] for x in range( int(div_number) + 1 ) ]
	debug_points = []
	for i in range(int(div_number) + 1):
		for j in range(int(div_number) + 1):
			surf_point = bottom_surface.point_at_parameter ( grid_spacing * i , grid_spacing * j )
			vec = bottom_surface.normal_at_parameter ( grid_spacing * i, grid_spacing * j)
			bottom_grid[i][j] = move_point_byvector( surf_point, vec, (thickness/3) )
			debug_points.append(bottom_grid[i][j])
			
	final_solid = solid
	panels = []
	debug = []
	#debug_solids = []
	#Thickend_panel = []
	#f = open( "C:\dev\Generative-drop-ceiling\Final_mockup\debug_testfile.txt", "w")
	
	for i in range(int(div_number) ):
		for j in range(int(div_number) ):
			#panels = Polygon.by_points(PointList([bottom_grid[i][j], bottom_grid[i+1][j], bottom_grid[i+1][j+1], bottom_grid[i][j+1]])) 
			panels = subdivide_panel( PointList([bottom_grid[i][j], bottom_grid[i+1][j], bottom_grid[i+1][j+1], bottom_grid[i][j+1]]), rand )
			#insert subdivision check here.
			
			for panel in panels: 
				thickness_value = controlled_random_thickness( thickness + ( thickness/3 ), rand )
				if thickness_value == 0.0:
					continue
				if len(panels) > 1:
					thickness_value = thickness_value + (thickness/6)

				panel = enlarge_polygon( panel )
				Thickend_panel = panel.thicken(thickness_value)
				
				if Thickend_panel:	
					test_solid = final_solid.subtract_from(Thickend_panel, True,True,True)
					
					try:
						final_solid = test_solid[0]
					except:
						continue
					"""
					f.write( str(final_solid))
					f.write("\n")
					"""
				#debug.append(final_solid)
				
				#debug.append(final_solid)
				#debug_solids.append( Thickend_panel)
				
			
	final_solid_list.append(final_solid)
	
	"""
	if count >= 3:
		break
	count +=1
	"""
#f.close()	
#Assign your output to the OUT variable
OUT = final_solid_list