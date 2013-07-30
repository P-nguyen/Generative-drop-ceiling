"""
# be sure to include this so everything works in Dynamo Revit
import sys
path = 'C:\\dev\\Dynamo\\bin\\Release'
sys.path.append(path)
import clr
clr.AddReference('LibGNet')
# be sure to include this so you have code completion
from Autodesk.LibG import *
from Autodesk.LibG import Point,Line,Surface,Polygon,Geometry,Cuboid,CoordinateSystem,Plane,Vector
"""


elem = IN[1][0]
 
output = []

for f in elem.Faces:
    output.append(f.Area)

OUT = output