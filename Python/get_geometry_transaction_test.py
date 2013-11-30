﻿# Default imports
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

elements = IN
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
     
    #opt = Options()
    
    id = elem.OwnerViewId
    document = elem.Document
    view = document.GetElement(id)
    
    geometry_element = elem.get_BoundingBox(view)
    
    #trans.Commit()
    
    max = geometry_element.Max
    min = geometry_element.Min
    
    surfaces.append(create_surface(max, min))

OUT = surfaces 
