# be sure to include this so everything works in Dynamo Revit
import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
# be sure to include this so you have code completion
from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Cuboid,CoordinateSystem,Plane,Vector
from Autodesk.LibG import *


base_plane = Plane.by_origin_normal(Point.by_coordinates(0, 0, 0), Vector.by_coordinates(0, 0, 1))


cs = CoordinateSystem.by_origin(Point.by_coordinates(0, 0, 50))

cuboid = Cuboid.by_lengths(cs, 5, 5, 5)


pt = cuboid.get_closest_point(base_plane)
GraphicItem.persist(pt)

OUT = None