import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN

grid = IN
count = None

def planar_quads( gridlist, point_indexs ):
    i = point_indexs[0]
    j = point_indexs[1]
    #grab the points around the main point,
    new_points = []
    point_distances = []
    #then make the planes that surround it
    #plane 1
    plane1 = Plane.by_three_points( gridlist[i][j-1], gridlist[i-1][j-1], gridlist[i-1][j] )
    closest_point = plane1.get_closest_point(gridlist[i][j])
    new_points.append(closest_point)
    point_distances.append(gridlist[i][j].distance_to(closest_point))
    #plane1_normal = plane1.normal()
    #
    
    #plane 2
    plane2 = Plane.by_three_points( gridlist[i+1][j], gridlist[i+1][j-1], gridlist[i][j-1] )
    closest_point = plane2.get_closest_point(gridlist[i][j])
    new_points.append(closest_point)
    point_distances.append(gridlist[i][j].distance_to(closest_point))
    #plane 3 
    plane3 = Plane.by_three_points( gridlist[i][j+1], gridlist[i+1][j+1], gridlist[i+1][j] )  
    closest_point = plane3.get_closest_point(gridlist[i][j])
    new_points.append(closest_point)
    point_distances.append(gridlist[i][j].distance_to(closest_point))
    #plane 4
    plane4 = Plane.by_three_points( gridlist[i-1][j], gridlist[i-1][j+1], gridlist[i][j+1] )
    closest_point = plane4.get_closest_point(gridlist[i][j])
    new_points.append(closest_point)
    point_distances.append(gridlist[i][j].distance_to(closest_point))
    
    final_point = None
    tolerence = None
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
    #take a portion of it.
    final_point.set_x(final_point.x()/len(new_points))
    final_point.set_y(final_point.y()/len(new_points))
    final_point.set_z(final_point.z()/len(new_points))
    tolerence = tolerence / len(new_points)
    
    return [final_point, tolerence ]
    
planar_process = False
while planar_process == False:
    planar_process = True
    for i in range(len(grid)):
        if i == 0 or i == len(grid)-1:
            #fix's perimeter border
            continue
        for j in range(len(grid[0])):
            
            if j == 0 or j == len(grid[0])-1:
                continue
            
            test = planar_quads(grid, [i,j])
            grid[i][j] = test[0]
            if test[1] >= 3:
                planar_process = False
            #count = test# [test.x(),test.y(),test.z()]
            

#Plane.by_three_points(Autodesk.LibG.Point, Autodesk.LibG.Point, Autodesk.LibG.Point)
#Autodesk.LibG.Geometry.get_closest_point(Autodesk.LibG.Geometry)
output_debug_new = []
for i in range(len(grid)-1 ):
     for j in range(len(grid[0])-1 ):
         new_polygon_pointlist = PointList([grid[i][j], grid[i+1][j], grid[i+1][j+1], grid[i][j+1]])
         output_debug_new.append(Polygon.by_points(new_polygon_pointlist))

OUT = output_debug_new