import requests
import urllib3

# Disable warning for unverified SSL certificates
urllib3.disable_warnings()

host = "10.10.20.48"
port = 443
username = "developer"
password = "C1sco12345"

url = f"https://{host}:{port}/restconf/data/ietf-interfaces:interfaces"

headers = {
       "Content-Type": "application/yang-data+json",
       "Accept": "application/yang-data+json",
}


def get_interfaces():
    response = requests.get(url, headers=headers, auth=(username, password), verify=False)
    if response.status_code != 200:
        print(f"Error {response.status_code}")
    return response.json()

def config_interface(num, ip, netmask):
    config = {
            "ietf-interfaces:interface": {
                "name": f"GigabitEthernet{num}",
                "description": "Configured by Python",
                "type": "iana-if-type:ethernetCsmacd",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": ip,
                            "netmask": netmask
                        }
                    ]
                }
            }
    }
    requests.put(url+f"/interface=GigabitEthernet{num}",
                 headers=headers, auth=(username, password),
                 verify=False, json=config)

def show_interfaces(data):
    lijst = data["ietf-interfaces:interfaces"]['interface']
    for interface in lijst:
        naam = interface['name']
        omschr = interface["description"]
        try:
            addr = interface["ietf-ip:ipv4"]["address"]
            print(f"{naam}:{omschr}, {addr}")
        except:
            print(f"{naam}:{omschr}")

def select_interface():
    inter = input("Give interface number: ")
    return inter

if __name__ == "__main__":
    data = get_interfaces()
    show_interfaces(data)
    inter = int(select_interface())
    while inter == 1:
        print("We do not want to change interface 1!")
        inter = int(select_interface())
    ip = input("Give IP address: ")
    netmask = input("Give netmask: ")
    config_interface(inter,ip,netmask)


#Dit is een nieuwe regel!
#en nog een nieuwe regel!!!!