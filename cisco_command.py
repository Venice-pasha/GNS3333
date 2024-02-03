import json
import os

# find and read json file
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
json_dir_path = os.path.join(dir_path, "output")
config_path = os.path.join(json_dir_path, "configuration_14r.json") 
with open(config_path, 'r') as file:
    data = json.load(file)

# get RIP/OSPF loopback list
RIP_list=[]
OSPF_list=[]
for i, router in enumerate(data["routers"]):
    if router["iBGP_protocol"]=="RIP":
        RIP_list.append(router["loopback"])
    elif router["iBGP_protocol"]=="OSPF":
        OSPF_list.append(router["loopback"])

for i, router in enumerate(data["routers"]):
    config_text = ""
    config_text += "ipv6 unicast-routing\n"
    for _ in range(3):
        config_text +="!\n"

    #loopback
    config_text+="interface Loopback0\n"
    loopback=router["loopback"]
    loopback_masque=router["loopback_masque"]
    iBGP_protocol=router["iBGP_protocol"]
    BGP_ip=router["BGP_ip"]
    config_text+=" no ip address\n"
    config_text+=" no shut down\n"
    config_text+=f" ipv6 address {loopback}/{loopback_masque}\n"
    config_text+=" ipv6 enable"
    if iBGP_protocol=="RIP":
        config_text+=" ipv6 rip 1 enable\n"
    elif iBGP_protocol=="OSPF":
        config_text+=" ipv6 ospf 1 area 0\n"
    config_text+=" exit\n"
    for _ in range(2):
        config_text +="!\n"

    #interfaces
    for j,interface in enumerate(router["interfaces"]):
        config_text +="!\n"
        enable=interface["enable"]
        interface_name=interface["interface_name"]
        config_text+=f"interface {interface_name}\n"
        if interface["enable"]=="0":
            config_text+=" no ip address\n"
            config_text+=" shutdown\n"
        elif interface["enable"]=="1":
            config_text+=" no ip address\n"
            config_text+=" no shutdown\n"
            ip_address=interface["ip_address"]
            subnet_mask=interface["subnet_mask"]
            config_text+=f" ipv6 address {ip_address}/{subnet_mask}\n"
            config_text+=" ipv6 enable"
            if iBGP_protocol=="RIP":
                config_text+=" ipv6 rip 1 enable\n"
            elif iBGP_protocol=="OSPF":
                config_text+=" ipv6 ospf 1 area 0\n"
    for _ in range(3):
        config_text +="!\n"
    
    #eBGP
    if iBGP_protocol=="RIP":
        config_text+="router bgp 100\n"
        config_text+=f" bgp router id {BGP_ip}\n"
        config_text+=" no bgp default ipv4-unicast\n"
        config_text+=" bgp log-neighbor-changes\n"
        for j in range(len(RIP_list)):
            neighbor=RIP_list[j]
            if neighbor!=loopback:
                config_text+=f" neighbor {neighbor} remote-as 100\n"
                config_text+=f" neighbor {neighbor} update-source Loopback0\n"
    elif iBGP_protocol=="OSPF":
        config_text+="router bgp 200\n"
        config_text+=f" bgp router id {BGP_ip}\n"
        config_text+=" no bgp default ipv4-unicast\n"
        config_text+=" bgp log-neighbor-changes\n"
        for j in range(len(OSPF_list)):
            neighbor=OSPF_list[j]
            if neighbor!=loopback:
                config_text+=f" neighbor {neighbor} remote-as 200\n"
                config_text+=f" neighbor {neighbor} update-source Loopback0\n"
    config_text+=" !\n"
        
    #address_family
    eBGP_enable=router["eBGP"]
    config_text+=" address family ipv6\n"
    if eBGP_enable=="0":
        if iBGP_protocol=="RIP":
            for j in range(len(RIP_list)):
                neighbor=RIP_list[j]
                if neighbor!=loopback:
                    config_text+=f"  neighbor {neighbor} activate\n"
        elif iBGP_protocol=="OSPF":
            for j in range(len(OSPF_list)):
                neighbor=OSPF_list[j]
                if neighbor!=loopback:
                    config_text+=f"  neighbor {neighbor} activate\n"
    elif eBGP_enable=="1":
        if iBGP_protocol=="RIP":
            for j in range(len(RIP_list)):
                neighbor=RIP_list[j]
                if neighbor!=loopback:
                    config_text+=f"  neighbor {neighbor} activate\n"
                    config_text+=f"  neighbor {neighbor} send community\n"
        elif iBGP_protocol=="OSPF":
            for j in range(len(OSPF_list)):
                neighbor=OSPF_list[j]
                if neighbor!=loopback:
                    config_text+=f"  neighbor {neighbor} activate\n"
                    config_text+=f"  neighbor {neighbor} send community\n"
    config_text+=f"  network {loopback}/{loopback_masque}\n"
    for j,interface in enumerate(router["interfaces"]):
        if interface["enable"]=="1":
            network_add=interface["ip_address"][:-1]
            config_text+=f"  network  {network_add}/{subnet_mask}\n"
    config_text+=" exit-address-family\n"

    #iBGP
    if iBGP_protocol=="RIP":
        config_text+="ipv6 router rip 1\n"
        config_text+=" redistribute connected\n"
    elif iBGP_protocol=="OSPF":
        config_text+="ipv6 router ospf 1\n"
        config_text+=f" router-id {BGP_ip}"
    config_text+="exit\n"


    # write in cfg
    file_path = os.path.join(json_dir_path, f"router_{i+1}.cfg")
    with open(file_path, 'w') as cfg_file:
        cfg_file.write(config_text)
    print(f"router{i+1} finished!")

print("All routers finsihed!")
