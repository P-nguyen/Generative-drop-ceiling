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

elements = IN

solids = []

def cuboid_from_corners(bboxmin, bboxmax):
    center_x = (bboxmax[0] + bboxmin[0]) / 2.0
    center_y = (bboxmax[1] + bboxmin[1]) / 2.0
    center_z = (bboxmax[2] + bboxmin[2]) / 2.0
    
    width = bboxmax[0] - bboxmin[0]
    length = bboxmax[1] - bboxmin[1]
    height = bboxmax[2] - bboxmin[2]

    cs = CoordinateSystem.by_origin(center_x, center_y, center_z)

    return Cuboid.by_lengths(cs, width, length, height)

def solid_from_min_max(bboxmin, bboxmax):
    return cuboid_from_corners(bboxmin, bboxmax)

for elem in elements:
    
    #trans = DynTransaction()
    #trans.Start()
     
    #opt = Options()
    
    id = elem.OwnerViewId
    document = elem.Document
    view = document.GetElement(id)
    
    geometry_element = elem.get_BoundingBox(view)
    
    #trans.Commit()
    
    bboxmax = geometry_element.Max
    bboxmin = geometry_element.Min

    solids.append(solid_from_min_max(bboxmin, bboxmax))

OUT = solids
