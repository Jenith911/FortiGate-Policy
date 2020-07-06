import sys
import os
import json

def Serv_Obj_json(filepath):
	serv_obj = []
	
	
	if not os.path.isfile(filepath):
		print("File path {} does not exist. Exiting ..".format(filepath))
		sys.exit()

	with open(filepath) as fp:
		for eachline in fp:
			eol_line = (eachline.strip().split(' '))
			eol_words = [item.strip() for item in eol_line]

			if eol_words[0] == "edit":
				nameobj = eol_words[1]

				service = {
					"Name" : nameobj[1:-1]
				}
				serv_obj.append(service)
	fp.close()
	return serv_obj
