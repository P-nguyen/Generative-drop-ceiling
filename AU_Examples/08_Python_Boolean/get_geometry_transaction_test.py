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

elements = IN[0]
points = []

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
    
    pt = Point.by_coordinates(
        (bboxmax[0] + bboxmin[0]) / 2.0,
        (bboxmax[1] + bboxmin[1]) / 2.0,
        (bboxmax[2] + bboxmin[2]) / 2.0 + IN[1])

    

    points.append(pt)

OUT = points
