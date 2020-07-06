import sys
import os
import json


def Create_IP_Obj(IP):
	
	f = open("Output/New_IP_objects.txt" , "a")
	f.write("    edit " + "\" h_ " + IP + "\"\n")
	f.write("        set type iprange \n")
	#print("        set associated-interface " + "\"" + INTERFACE + "\"")
	f.write("        set start-ip " + IP + "\n")
	f.write("        set end-ip " + IP + "\n")
	f.write("    next \n")
	f.close()

#For match IP address with relevent Address object
def match_IP_to_Obj(addr_obj,IP):
	int_max = 10000
	index = 0
	IP_match_name = ""


	IP_match = [x for x in addr_obj if IP in x["IP_Address"] ]

	if len(IP_match) == 1:
		IP_match_name = IP_match[0]["Name"]
	elif len(IP_match) > 1:
		for x in range(len(IP_match)):
			if int_max > len(IP_match[x]["IP_Address"]):
				int_max = len(IP_match[x]["IP_Address"])
				index = x
		IP_match_name = IP_match[index]["Name"]
	else:
		#IF no object is found,Create object
		IP_match_name = "h_" + IP
		Create_IP_Obj(IP)


	return IP_match_name

def Create_SERV_Obj(name,type,port):
	f = open("Output/New_Serv_Obj.txt", "a")

	f.write("    edit " "\"" + name  + "\"\n")
	if type == "TCP":
		f.write("        set tcp-portrange " + port + "\n")
	else:
		f.write("        set udp-portrange " + port + "\n")
	f.write("    next \n")
	f.close()

def match_Serv_to_Obj(serv_obj,serv):
	Serv_match_name = []

	serv_match = [x for x in serv_obj if serv in x["Name"] ]
	if len(serv_match) > 1:
		Serv_match_name.append(serv) 
	else:
		serv_split = serv.split('/')
		if len(serv_split) > 1:
			Create_SERV_Obj(serv,serv_split[0], serv_split[1])
		Serv_match_name.append(serv)

	return Serv_match_name


def Create_Objects(policy_file,addr_obj,serv_obj):

	if os.path.isfile("Output/New_IP_objects.txt"):
		os.remove("Output/New_IP_objects.txt")
	if os.path.isfile("Output/New_Serv_Obj.txt"):
		os.remove("Output/New_Serv_Obj.txt")

	if not os.path.isfile(policy_file):
   		print("File path {} does not exist. Exiting ..".format(policy_file))
   		sys.exit()

	Policy_json = []
	Policy_Obj = ''
	Policy = []
	new_obj_json = []
	with open(policy_file) as fp:
		for eachline in fp:
			eol_line = (eachline.strip().split('	'))
			eol_words = [item.split('=') for item in eol_line]
			
			DESTIP = eol_words[0][1]
			SRCIP  = eol_words[1][1]
			SERVICE = eol_words[2][1]


			DEST_OBJ = match_IP_to_Obj(addr_obj,DESTIP)	
			SRC_OBJ = match_IP_to_Obj(addr_obj,SRCIP)
			SERV_OBJ = match_Serv_to_Obj(serv_obj,SERVICE)

			

			for po in Policy_json:
				if DEST_OBJ in po["DEST_OBJ"]:
					if SRC_OBJ in po["SRC_OBJ"]:
						po["SERV_OBJ"].append(str(SERV_OBJ[0]))
						break
			else:
				Policy_Obj = {
					"SRC_OBJ"  : SRC_OBJ,
					"DEST_OBJ" : DEST_OBJ,
					"SERV_OBJ" : SERV_OBJ,
					}
		
				Policy_json.append(Policy_Obj)
	for po in Policy_json:
		s = str(po["SRC_OBJ"]) + " " + str(po["DEST_OBJ"])
		new_obj={
			"SRC_OBJ + DEST_OBJ" : s ,
			"SERV_OBJ" : po["SERV_OBJ"],
		}
		new_obj_json.append(new_obj)
	unique = { each["SRC_OBJ + DEST_OBJ"] : each  for each in new_obj_json}.values()
		#print(Policy_json)


	return unique	

def Create_Policy(Source_Interface,Destination_Interface,Start_Policy_ID,Policy_objects):

	if os.path.isfile("Output/New_Policy.txt"):
		os.remove("Output/New_Policy.txt")

	f = open("Output/New_Policy.txt", 'a')
	for po in Policy_objects:
		serv = ""
		SOURCE = po["SRC_OBJ + DEST_OBJ"].split(" ")[0]
		DESTINATION = po["SRC_OBJ + DEST_OBJ"].split(" ")[1]
		for x in po["SERV_OBJ"]:
			serv = serv + " " + str(x)
		f.write("    edit " + str(Start_Policy_ID) + "\n")
		f.write("        set name \"" + SOURCE + " to "  + DESTINATION + "\"\n")
		f.write("        set srcintf " + Source_Interface + "\n")
		f.write("        set dstintf " + Destination_Interface + "\n")
		f.write("        set srcaddr " + SOURCE +"\n")
		f.write("        set dstaddr " + DESTINATION + "\n")
		f.write("        set action accept \n")
		f.write("        set schedule \"always\" \n")
		f.write("        set service " + serv + "\n")
		f.write("    next \n")
		Start_Policy_ID += 1
	f.close()

