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

dataEnteringNode = IN
#The input to this node will be stored in the IN variable.

objects = IN

air_vents = []
column = []
light_fixtures = []
standard_geometry = []

for obj in objects:
	name = obj.Category.Name
	if "Air Terminals" in name:
		#air_vents.append( name )
		air_vents.append( obj )
	elif "Column" in name:
		#column.append(name)
		column.append(obj)
	elif "Light" and "Fix" in name:
		#light_fixtures.append(name)
		light_fixtures.append(obj)
	else:
		#standard_geometry.append(name)
		standard_geometry.append(obj)



#Assign your output to the OUT variable
OUT = air_vents, column, light_fixtures, standard_geometry
