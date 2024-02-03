def p_number(text):
    if text=="company":
        return 100
    elif text=="school":
        return 150
    elif text=="VIP":
        return 20
    else:
        return 200

def find_router_ip(router_name,list_router):
    number_part = int(''.join(filter(str.isdigit, router_name)))
    router_number=number_part - 1
    router_ip=list_router[router_number]["ip"]
    return router_ip

def find_interface_ip(router_name,interface_number,list_router):
    number_part = int(''.join(filter(str.isdigit, router_name)))
    router_number=number_part - 1
    interface_number=int(interface_number)
    interface_ip=list_router[router_number]["interfaces"][interface_number]["ip_address"]
    return interface_ip

def connexion_router(list_connexion,router1,router2):
    if ([router1,router2] in list_connexion):
        connexion_number=list_connexion.index([router1,router2])+1
        return (f"{connexion_number}::2")
    elif ([router2,router1] in list_connexion):
        connexion_number=list_connexion.index([router2,router1])+1
        return (f"{connexion_number}::2")
    else:
        list_connexion.append([router1,router2])
        connexion_number=len(list_connexion)
        return (f"{connexion_number}::1")