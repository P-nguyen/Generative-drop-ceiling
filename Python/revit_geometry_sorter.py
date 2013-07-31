dataEnteringNode = IN
#The input to this node will be stored in the IN variable.
test = []
objects = IN

air_vents = []
column = []
light_fixtures = []
standard_geometry = []

def get_solid( revit_object ):
	elem = revit_object
	 
	trans = DynTransaction()
	trans.Start()
	 
	opt = Options()
	geometry_list = elem.get_Geometry(opt)
	
	trans.Commit()
	
	return geometry_list

for obj in objects:
	name = obj.Category.Name
	if "Air Terminals" in name:
		air_vents.append( name )
	elif "Column" in name:
		column.append(name)
	elif "Light" and "Fix" in name:
		light_fixtures.append(name)
	else:
		standard_geometry.append(name)
	#GetOriginalGeometry(Options())
	#.get_Geometry(Options())


#Assign your output to the OUT variable
OUT = air_vents, column, light_fixtures, standard_geometry