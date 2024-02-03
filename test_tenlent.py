import telnetlib
import requests

# GNS3 API URL
gns3_url = "http://localhost:3080/v2"
project_name = "untitled2"

# GNS3 ID
projects_response = requests.get(f"{gns3_url}/projects")
project_id = next((project["project_id"] for project in projects_response.json() if project["name"] == project_name), None)

if not project_id:
    print("projet non trouve!\n")
    exit()

# les infos de nodes
nodes_response = requests.get(f"{gns3_url}/projects/{project_id}/nodes")
nodes = nodes_response.json()

print(nodes)

# parcourir les ndes
for node in nodes:
    name = node.get('name')
    console_port = node.get('console')
    console_host = node.get('console_host')

    # Telnet connexion
    try:
        with telnetlib.Telnet(console_host, console_port) as tn:
            tn.write(b"hello\r")

            tn.read_until(b"hello", timeout=3)

            print(f"to {name} send 'hello' \n")

            response = tn.read_until(b"Router#", timeout=5)
            print(f"response of router {name} :\n{response.decode('ascii')}")

    except Exception as e:
        print(f"can not find {name}  (port: {console_port})：{e}")
