import sys
import os
import ipaddress
from netaddr import IPAddress
import json

def Addr_Obj_json(filepath):

    global nameobj
    global typeobj
    global associatedinf
    addr_objs = []
    newip = []


    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting ..".format(filepath))
        sys.exit()



    with open(filepath) as fp:
        for eachline in fp:
            eol_line = (eachline.strip().split(' '))
            eol_words = [item.strip() for item in eol_line]

            #Find Key words in each line
            if eol_words[0] == "edit":
                nameobj = eol_words[1]

            elif eol_words[0] == "set":
                if eol_words[1] == "type":
                    typeobj = eol_words[2]

                elif eol_words[1] == "associated-interface":
                    associatedinf = eol_words[2]

                elif eol_words[1] == "start-ip":
                    startip = eol_words[2]

                elif eol_words[1] == "end-ip":
                    endip  = eol_words[2]
                    laststartip = startip.split('.')[3]
                    lastendip = endip.split('.')[3]
                    diffip = int(lastendip) - int(laststartip)
                    if diffip > 0:
                        for x in range(diffip+1):
                            newip.append(str(ipaddress.IPv4Address(startip) + x))
                    else:
                        newip = startip

                #For ubject type sybnet
                elif eol_words[1] == "subnet":
                    typeobj = eol_words[1]                    
                    prifx = IPAddress(eol_words[3]).netmask_bits()
                    address_w_prfix = str(eol_words[2]) + "/" + str(prifx)
                    for addr in ipaddress.IPv4Network(address_w_prfix):
                        newip.append(str(addr))

            #End of an object parse values as JSON
            elif eol_words[0] == "next":
                addr = {
                    "Name" : nameobj[1:-1],
                    "type" : typeobj,
                    "associated_interfacenterface" : associatedinf[1:-1],
                    "IP_Address" : newip,
                    }
                addr_objs.append(addr)
                newip = []
    fp.close()     
        #f.write(json.dumps(addr_objs))
    return addr_objs
