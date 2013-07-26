import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Vector

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

grid = IN
count = None

lens = []

def planar_quads( gridlist, point_indexs ):
    i = point_indexs[0]
    j = point_indexs[1]
    #grab the points around the main point,
    new_points = []
    point_distances = []
    #then make the planes that surround it
    
    #plane 1
    try:
        plane = Plane.by_three_points( gridlist[i][j-1], gridlist[i-1][j-1], gridlist[i-1][j] )
    except ValueError:
        plane = None
    if plane:
        closest_point = plane.get_closest_point(gridlist[i][j])
        new_points.append(closest_point)
        point_distances.append(gridlist[i][j].distance_to(closest_point))
        #plane1_normal = plane1.normal()
        
    #plane 2
    #if i < len(gridlist) and j > 0: #grid[i+1][j-1]:
    try:
        plane = Plane.by_three_points( gridlist[i+1][j], gridlist[i+1][j-1], gridlist[i][j-1] )
    except ValueError:
        plane = None
    if plane:
        closest_point = plane.get_closest_point(gridlist[i][j])
        new_points.append(closest_point)
        point_distances.append(gridlist[i][j].distance_to(closest_point))
        
    #plane 3 
    #if i < len(gridlist) and j < len(gridlist[0]):  #grid[i+1][j+1]:
    try:
        plane = Plane.by_three_points( gridlist[i][j+1], gridlist[i+1][j+1], gridlist[i+1][j] )  
    except ValueError:
        plane = None
    if plane:
        closest_point = plane.get_closest_point(gridlist[i][j])
        new_points.append(closest_point)
        point_distances.append(gridlist[i][j].distance_to(closest_point))
    #plane 4
    #if i > 0 and j < len(gridlist[0]): #grid[i-1][j+1]:
    try:
        plane = Plane.by_three_points( gridlist[i-1][j], gridlist[i-1][j+1], gridlist[i][j+1] )
    except ValueError:
        plane = None
    if plane:
        closest_point = plane.get_closest_point(gridlist[i][j])
        new_points.append(closest_point)
        point_distances.append(gridlist[i][j].distance_to(closest_point))
    
    
    new_points.append(gridlist[i][j])
    point_distances.append(0.0) #to account for the extra point.
    final_point = None
    count = 0
    #find average of points
    for pt in new_points:
        if final_point == None:
            final_point = pt
            tolerence = point_distances[count]
            count += 1
            continue
        
        final_point.set_x( final_point.x() + pt.x() )
        final_point.set_y( final_point.y() + pt.y() )
        final_point.set_z( final_point.z() + pt.z() )
        
        tolerence = tolerence + point_distances[count]
        count +=1 

    final_point.set_x(final_point.x()/len(new_points))
    final_point.set_y(final_point.y()/len(new_points))
    final_point.set_z(final_point.z()/len(new_points))
    
    tolerence = tolerence / len(new_points)
    
    return [final_point, tolerence ]

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
    
    vector_1.set_x( (vector_1.x() + vector_2.x()) / 2 )
    vector_1.set_y( (vector_1.y() + vector_2.y()) / 2 )
    vector_1.set_z( (vector_1.z() + vector_2.z()) / 2 )
    
    final_vec = vector_1
    
    return final_vec

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
        
        point.append(move_point_byvector( vertex_list[i], vectest, 15 ))
        
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
            
    
def intersect_plane( polygons, point_indexs ):
    i = point_indexs[0]
    j = point_indexs[1]
    large_polygon = enlarge_polygon(polygons[i][j])
    solid = large_polygon.thicken(10)
    
    poly_points = polygons[i][j].vertices()
    center_norm = polygons[i][j].normal_at_parameter (0.5, 0.5)
    cutting_planes = []
    
    #points = []
    #poly1
    if j-1 >= 0: 
        adjacent_norm = polygons[i][j-1].normal_at_parameter (0.5, 0.5)

        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[1], edge_normal, 10 )
        cutting_planes.append(Plane.by_three_points( poly_points[0], poly_points[1], vertical_point ))
    else:
        vertical_point = Point.by_coordinates(poly_points[1].x(), poly_points[1].y(), poly_points[1].z())
        vertical_point.set_z(vertical_point.z() + 100)
        cutting_planes.append(Plane.by_three_points( poly_points[0], poly_points[1], vertical_point ))
    #cutting_planes.append(Polygon.by_points(PointList([poly_points[0], poly_points[1], vertical_point])))
    #points.append([poly_points[0], poly_points[1], vertical_point])
    
    #poly2    
    if i+1 <= len(polygons)-1:
        adjacent_norm = polygons[i+1][j].normal_at_parameter (0.5, 0.5)
        
        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[2], edge_normal, 10 )
        cutting_planes.append(Plane.by_three_points( poly_points[1], poly_points[2], vertical_point ))
    else:
        vertical_point = Point.by_coordinates(poly_points[2].x(), poly_points[2].y(), poly_points[2].z())
        vertical_point.set_z(vertical_point.z() + 10)
        cutting_planes.append(Plane.by_three_points( poly_points[1], poly_points[2], vertical_point ))
    #cutting_planes.append(Polygon.by_points(PointList([poly_points[1], poly_points[2], vertical_point])))
    
    #poly3 
    if j+1 <= len(polygons[0])-1:
        adjacent_norm = polygons[i][j+1].normal_at_parameter (0.5, 0.5)
        
        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[3], edge_normal, 10 )
        cutting_planes.append(Plane.by_three_points( poly_points[2], poly_points[3], vertical_point ))
    else:
        vertical_point = Point.by_coordinates(poly_points[3].x(), poly_points[3].y(), poly_points[3].z())
        vertical_point.set_z(vertical_point.z() + 10)
        cutting_planes.append(Plane.by_three_points( poly_points[2], poly_points[3], vertical_point ))
    #cutting_planes.append(Polygon.by_points(PointList([poly_points[2], poly_points[3], vertical_point])))
        
    #poly4 
    if i-1 >= 0:
        adjacent_norm = polygons[i-1][j].normal_at_parameter (0.5, 0.5)

        edge_normal = add_two_vectors( center_norm, adjacent_norm )
        vertical_point = move_point_byvector(poly_points[0], edge_normal, 10 )
        cutting_planes.append(Plane.by_three_points( poly_points[3], poly_points[0], vertical_point ))       
    else:
        vertical_point = Point.by_coordinates(poly_points[0].x(), poly_points[0].y(), poly_points[0].z())
        vertical_point.set_z(vertical_point.z() + 10)
        cutting_planes.append(Plane.by_three_points( poly_points[3], poly_points[0], vertical_point ))
    #cutting_planes.append(Polygon.by_points(PointList([poly_points[3], poly_points[0], vertical_point])))
                          
    planelist = PlaneList([ cutting_planes[0],cutting_planes[1],cutting_planes[2],cutting_planes[3] ])
    test = solid.slice_with_planes(planelist,True)
    centroid = polygons[i][j].point_at_parameter (0.5, 0.5)
    
    return find_panel(test, centroid)

####Main####
cuttoff_tolerance = 1
planar_process = False

while planar_process == False:
    planar_process = True
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j], tolerance = planar_quads(grid, [i,j])

            if tolerance >= cuttoff_tolerance:
                planar_process = False
                     
polygon_list = [ [ (y,x) for y in range( len(grid[0])-1) ] for x in range( len(grid)-1  ) ]
for i in range(len(grid)-1 ):
     for j in range(len(grid[0])-1 ):
         new_polygon_pointlist = PointList([grid[i][j], grid[i+1][j], grid[i+1][j+1], grid[i][j+1]])
         polygon_list[i][j] = Polygon.by_points(new_polygon_pointlist)


debug_planes = []

#create new grid of points that are correctly offset from the original pointlist.
for i in range(len(polygon_list)):
    for j in range(len(polygon_list[0])):
       #debug_planes.extend( intersect_plane( polygon_list, [i,j] ) )
       debug_planes.append( intersect_plane( polygon_list, [i,j] ) )

################################################################################################################
#output txt file.
f = open("planarQuad_textfile.txt", "w")

for i in range(len(grid)):
    for j in range(len(grid[0])):
        f.write( str(grid[i][j].x()) + "," + str(grid[i][j].y()) + "," + str(grid[i][j].z()) )
        if j != (len(grid[0])-1):
            f.write("/")
    if i != (len(grid)-1):
        f.write("\n")
f.close()
################################################################################################################

OUT = debug_planes #polygon_list ,debug_planes