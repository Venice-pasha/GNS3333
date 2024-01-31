import json
import os
import copy
import func as f

# find and read json file
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
json_dir_path = os.path.join(dir_path, "json")
config_path = os.path.join(json_dir_path, "intent_14r.json") 
with open(config_path, 'r') as file:
    data = json.load(file)

#Initialisation_router
new_data={}
config_path = os.path.join(json_dir_path, "router.json")
with open(config_path, "r") as file:
    router_basic = json.load(file)
list_router=[]

#RIP/OSPF_basic,start with intent file
for network in data["networks"]:
    ip_auto=1
    as_id = network["autonomous_system"]
    loopback = network["loopback"] 
    loopback_masque=network["loopback_masque"]
    ip = network["IP"]
    ip_masque=network["IP_masque"]
    routers=network["routers"]
    protocol = network["protocol"]
    for i, router in enumerate(routers):
        temp=router_basic
        router_id=router["router_id"]
        temp["ip_version"]=6
        temp["ip"]=f"{ip}{ip_auto}"
        temp["iBGP_protocol"]=protocol
        temp["loopback_masque"]=loopback_masque
        temp["loopback"]=f"{loopback}{ip_auto}"
        temp["router_id"]=router_id
        ip_auto+=1
        for j,interface in enumerate(router["interfaces"]):
            connected_to=interface["connected_to"]
            if connected_to==None:
                continue
            interface_connect=interface["interface_connect"]
            temp["interfaces"][j]["enable"]="1"
            temp["interfaces"][j]["ip_address"]=f"{ip}{ip_auto}"
            ip_auto+=1
            temp["interfaces"][j]["subnet_mask"]=ip_masque
            temp["interfaces"][j]["dist_r"]=connected_to
            temp["interfaces"][j]["dist_i"]=interface_connect
        print (f"configuration of {router_id} finished")
        list_router.append(copy.deepcopy(temp))
    print(f"first step configuration of {protocol} finished")

#BGP semi auto
for interconnection in data["interconnections"]:
    AS1=interconnection["autonomous_system_1"]
    AS2=interconnection["autonomous_system_2"]
    router_id_a=interconnection["router_name1"]
    interface_a=interconnection["interface1"]
    pref_a=interconnection["preference_1"]
    router_id_b=interconnection["router_name2"]
    interface_b=interconnection["interface2"]
    pref_b=interconnection["preference_2"]
    ip_int=interconnection["ip_interconnection"]
    ip_ia=f"{ip_int}1"
    ip_ib=f"{ip_int}2"
    protocol= interconnection["protocol"]
    subnet_mask=interconnection["subnet_mask"]
    if protocol=="BGP":
        for i,router in enumerate(list_router):
            if router["router_id"]==router_id_a:
                router["eBGP"]="1"
                router["eBGP_interface"]=interface_a
                interface_a=int(interface_a)
                router['interfaces'][interface_a]["enable"]="1"
                router['interfaces'][interface_a]["ip_address"]=ip_ia
                router['interfaces'][interface_a]["subnet_mask"]=subnet_mask
                router['interfaces'][interface_a]["dist_r"]=router_id_b
                router['interfaces'][interface_a]["dist_i"]=interface_b
            if router["router_id"]==router_id_b:
                router["eBGP"]="1"
                router["eBGP_interface"]=interface_b
                interface_b=int(interface_b)
                router['interfaces'][interface_b]["enable"]="1"
                router['interfaces'][interface_b]["ip_address"]=ip_ib
                router['interfaces'][interface_b]["subnet_mask"]=subnet_mask
                router['interfaces'][interface_b]["dist_r"]=router_id_a
                router['interfaces'][interface_b]["dist_i"]=interface_a
    print(f"BGP interconnect of {AS1} and {AS2}:{router_id_a} in interface {interface_a} and{router_id_b} in interface {interface_b}")


# fill in blanks ip auto
for i,router in enumerate(list_router):
    for j,interface in enumerate(router["interfaces"]):
        if interface["enable"]=='1':
            dist_r=interface["dist_r"]
            interface["dist_r_ip"]=f.find_router_ip(dist_r,list_router)
            dist_i=interface["dist_i"]
            interface["dist_i_ip"]=f.find_interface_ip(dist_r,dist_i,list_router)
print("sucess to fill in null ip")

#write data into json
new_data["routers"]=list_router
output_file_path = os.path.join(dir_path, "output", "configuration_14r.json")
with open(output_file_path, "w") as file:
    json.dump(new_data, file, indent=4)
print("table of configuration ok!")
