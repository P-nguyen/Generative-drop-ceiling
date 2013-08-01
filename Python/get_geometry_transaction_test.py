import sys
path = 'C:\\Users\\t_nguyp\\Desktop\\Dynamo\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
from Autodesk.LibG import *

from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry

elements = IN[3]
surfaces = []

def create_surface(max, min):
    p1 = Point.by_coordinates(min[0], min[1], min[2])
    p2 = Point.by_coordinates(max[0], min[1], min[2])
    p3 = Point.by_coordinates(max[0], max[1], min[2])
    p4 = Point.by_coordinates(min[0], max[1], min[2])
    ptlist = PointList([p1,p2,p4,p3])
    surface = BSplineSurface.by_points(ptlist, 2,2)
    
    return surface

for elem in elements:
    
    #trans = DynTransaction()
    #trans.Start()
     
    opt = Options()
    
    id = elem.OwnerViewId
    document = elem.Document
    view = document.GetElement(id)
    
    geometry_element = elem.get_BoundingBox(view)
    
    #trans.Commit()
    
    max = geometry_element.Max
    min = geometry_element.Min
    
    surfaces.append(create_surface(max, min))

OUT = surfaces #p1,p2,p3,p4 #test #.Objects #[elem, geometry_list]