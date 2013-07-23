# be sure to include this so everything works in Dynamo Revit
import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
# be sure to include this so you have code completion
from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Cuboid,CoordinateSystem,Plane,Vector
from Autodesk.LibG import *


elem = IN
 
trans = DynTransaction()
trans.Start()
 
opt = Options()
geometry_list = elem.get_Geometry(opt)

trans.Commit()


OUT = [elem, geometry_list]
