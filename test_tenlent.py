import telnetlib
import requests

# GNS3 API 的 URL
gns3_url = "http://localhost:3080/v2"
project_name = "untitled2"

# 获取 GNS3 项目的 ID
projects_response = requests.get(f"{gns3_url}/projects")
project_id = next((project["project_id"] for project in projects_response.json() if project["name"] == project_name), None)

if not project_id:
    print("项目未找到")
    exit()

# 获取项目中所有节点的信息
nodes_response = requests.get(f"{gns3_url}/projects/{project_id}/nodes")
nodes = nodes_response.json()

print(nodes)

# 遍历所有路由器节点
for node in nodes:
    # 获取路由器的名字和控制台端口
    name = node.get('name')
    console_port = node.get('console')
    console_host = node.get('console_host')

    # 建立 Telnet 连接
    try:
        with telnetlib.Telnet(console_host, console_port) as tn:
            # 发送 'hello' 字符串加上换行符
            tn.write(b"hello\r")

            # 假设您的路由器会回显发送的命令，这里等待回显 'hello' 字符串
            tn.read_until(b"hello", timeout=3)

            print(f"向 {name} 发送 'hello' 成功。")

            response = tn.read_until(b"Router#", timeout=5)
            print(f"路由器 {name} 的响应:\n{response.decode('ascii')}")

    except Exception as e:
        print(f"无法连接到 {name} 的控制台 (端口: {console_port})：{e}")