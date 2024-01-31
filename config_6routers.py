import json
import os
import copy
import func as f

# find and read json file
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
json_dir_path = os.path.join(dir_path, "json")
config_path = os.path.join(json_dir_path, "intent_6r.json") 

# 读取JSON文件的内容
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

#BGP manuel
interconnection=data["interconnection"]
AS1=interconnection["autonomous_system_1"]
AS2=interconnection["autonomous_system_2"]
router_id_a,interface_a,pref_a=interconnection["router_info"][0]
router_id_b,interface_b,pref_b=interconnection["router_info"][1]
ip_int=interconnection["ip_interconnection"]
ip_ia=f"{ip_int}1"
ip_ib=f"{ip_int}2"
protocol= interconnection["protocol"]
subnet_mask=interconnection["subnet_mask"]
if protocol=="BGP":
    list_router[2]["eBGP"]="1"
    list_router[2]["eBGP_interface"]=[1]
    list_router[3]["eBGP"]="1"
    list_router[3]["eBGP_interface"]=[1]
    list_router[2]["preference"]=f.p_number(pref_a)
    list_router[3]["preference"]=f.p_number(pref_b)
    list_router[3]["eBGP"]="1"
    list_router[2]["interfaces"][1]["enable"]="1"
    list_router[2]["interfaces"][1]["ip_address"]=ip_ia
    list_router[3]["interfaces"][1]["enable"]="1"
    list_router[3]["interfaces"][1]["ip_address"]=ip_ib
    list_router[2]["interfaces"][1]["subnet_mask"]=subnet_mask
    list_router[3]["interfaces"][1]["subnet_mask"]=subnet_mask
    list_router[2]["interfaces"][1]["dist_i"]=interface_b
    list_router[3]["interfaces"][1]["dist_i"]=interface_a
    list_router[2]["interfaces"][1]["dist_i_ip"]=ip_ib
    list_router[3]["interfaces"][1]["dist_i_ip"]=ip_ia
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

new_data["routers"]=list_router
# 指定要写入的文件路径（在 'output' 子目录中）
output_file_path = os.path.join(dir_path, "output", "configuration_6r.json")

# 将数据写入文件
with open(output_file_path, "w") as file:
    json.dump(new_data, file, indent=4)
print("table of configuration ok!")