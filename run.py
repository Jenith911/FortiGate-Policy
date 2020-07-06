import sys
import os
import address_objects
import service_obj
import policy

def main():
	Source_Interface = "DC"
	Destination_Interface = "DC"
	IP_Object_File = "Input/addr_object.txt"
	Service_Object_File = "Input/service_obj.txt"
	Policy_File = "Input/policy.txt"
	Start_Policy_ID = 1

	IP_Objects = address_objects.Addr_Obj_json(IP_Object_File)
	Serv_Objects = service_obj.Serv_Obj_json(Service_Object_File)
	
	Policy_objects = policy.Create_Objects(Policy_File,IP_Objects,Serv_Objects)
	#print(Policy_objects)
	policy.Create_Policy(Source_Interface,Destination_Interface,Start_Policy_ID,Policy_objects)



if __name__ == '__main__':
	main()