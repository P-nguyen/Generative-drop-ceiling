dataEnteringNode = IN
#The input to this node will be stored in the IN variable.

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