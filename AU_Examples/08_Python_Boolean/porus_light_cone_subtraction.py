# Default imports
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
import Autodesk
import sys
import clr
path = r'C:\Autodesk\Dynamo\Core'
exec_path = r'C:\Autodesk\Dynamo\Core\dll'
sys.path.append(path)
sys.path.append(exec_path)
clr.AddReference('LibGNet')
from Autodesk.LibG import *

# hack to get random to work
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import random
import math

#The input to this node will be stored in the IN variable.
dataEnteringNode = IN


def length(v):
  return math.sqrt(v.dot(v))

def vector_angle(v1, v2):
	radians = math.acos(v1.dot(v2) / (length(v1) * length(v2)))
	return (radians * 180)/ math.pi
  
def vector_create( point_to , point_from ):
   
    vec_x = (point_to.x() - point_from.x()) / 2 
    vec_y = (point_to.y() - point_from.y()) / 2 
    vec_z = (point_to.z() - point_from.z()) / 2 
    
    final_vec = Vector.from_xyz( vec_x, vec_y, vec_z )
    
    return final_vec
    
def move_point_byvector( point, vector, magnitude ):
    vector_copy = Vector.by_coordinates(vector.x(),vector.y(),vector.z())
    vector_copy.normalize()
       
    newpoint = [0,0,0]
    newpoint[0] = point.x() + (vector_copy.x() * magnitude)
    newpoint[1] = point.y() + (vector_copy.y() * magnitude)
    newpoint[2] = point.z() + (vector_copy.z() * magnitude)
    
    finalpt = Point.by_coordinates(newpoint[0], newpoint[1], newpoint[2])
    return finalpt

def random_points_on_surf( Bspline_surface ):
    for j in range(10):
        rand_num1 = (random.randrange(125, 875))/1000.0
        rand_num2 = (random.randrange(125, 875))/1000.0
        
        surface_points.append(Bspline_surface.point_at_parameter( rand_num1, rand_num2 ))
        
    return surface_points


def find_lightsource( all_lights, bspline_surface ):
    closest_distance = None
    
    for light_point in all_lights:
        closest_point = bspline_surface.get_closest_point(light_point)
        dist = closest_point.distance_to(light_point)
        
        if closest_distance == None:
            closest_distance = dist
            closest_light_point = light_point
            continue
        
        if dist < closest_distance:
            closest_distance = dist
            closest_light_point = light_point
            
    return closest_light_point


surfaces = IN[0]
light_points = IN[1]
solids = IN[2]
tolerence = 200

surface_points = []
final_solid_list = []

for i in range( len(surfaces) ):
    
    surface_points = random_points_on_surf(surfaces[i])
    light = find_lightsource( light_points, surfaces[i] )
    
    final_solid = solids[i]
    objs = []
    
    for point in surface_points:
    	test_point = Point.by_coordinates(point.x(),point.y(),light.z())
    	dist = test_point.distance_to(light)
    	
    	if dist >= tolerence:
    		continue
    		
    	lower_pt = Point.by_coordinates(light.x(), light.y(), light.z() - 1)
    	Zcomparision_vector = vector_create( lower_pt , light )
    	vec = vector_create( point, light )
    	angle = vector_angle(vec, Zcomparision_vector)
    	
    	if angle <= 60:
            new_point = move_point_byvector( point, vec, 20 )
    		#objs.append(Cone.by_points_radius( light , new_point, 0.1, 3.0))
            
            cutting_cone = Cone.by_points_radius( light , new_point,(random.randrange(150, 250)/1000.0), (random.randrange(250, 1000)/1000.0) )
            final_solid = final_solid.subtract_from(cutting_cone, True, True, True)    
            final_solid = final_solid[0]
    
    final_solid_list.append(final_solid)
#Assign your output to the OUT variable

OUT = final_solid_list
