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


elementlist = IN

bboxOfElementsMin = None
bboxOfElementsMax = None

for element in elementlist:
    
    id = element.OwnerViewId
    document = element.Document
    view = document.GetElement(id)
    
    bboxmin = element.get_BoundingBox(view).Min
    bboxmax = element.get_BoundingBox(view).Max
    
    if bboxOfElementsMin == None:
        bboxOfElementsMin = [bboxmin[0],bboxmin[1],bboxmin[2]]
        bboxOfElementsMax = [bboxmax[0],bboxmax[1],bboxmax[2]]
        continue
    
    for i in range(3):
        if  bboxmin[i] < bboxOfElementsMin[i]:
            bboxOfElementsMin[i] = bboxmin[i]
        if  bboxmax[i] > bboxOfElementsMax[i]:
            bboxOfElementsMax[i] = bboxmax[i]
    
bot_pt1 = Point.by_coordinates(bboxOfElementsMin[0],bboxOfElementsMin[1],bboxOfElementsMin[2])
bot_pt2 = Point.by_coordinates(bboxOfElementsMax[0],bboxOfElementsMin[1],bboxOfElementsMin[2])  
bot_pt3 = Point.by_coordinates(bboxOfElementsMax[0],bboxOfElementsMax[1],bboxOfElementsMin[2])  
bot_pt4 = Point.by_coordinates(bboxOfElementsMin[0],bboxOfElementsMax[1],bboxOfElementsMin[2])  
bot_ptlist = PointList([bot_pt1,bot_pt2,bot_pt4,bot_pt3])
bottom_surface = BSplineSurface.by_points(bot_ptlist,2,2)

top_pt1 = Point.by_coordinates(bboxOfElementsMin[0],bboxOfElementsMin[1],bboxOfElementsMax[2]) 
top_pt2 = Point.by_coordinates(bboxOfElementsMax[0],bboxOfElementsMin[1],bboxOfElementsMax[2]) 
top_pt3 = Point.by_coordinates(bboxOfElementsMax[0],bboxOfElementsMax[1],bboxOfElementsMax[2]) 
top_pt4 = Point.by_coordinates(bboxOfElementsMin[0],bboxOfElementsMax[1],bboxOfElementsMax[2]) 
top_ptlist = PointList([top_pt1,top_pt2,top_pt4,top_pt3])
top_surface = BSplineSurface.by_points(top_ptlist,2,2)

OUT =  bot_pt1 ,bot_pt3, top_surface#, top_ptlist#bboxOfElementsMin, bboxOfElementsMax
