import json

# Json object to which all single flow jsons will be added
conf_json = {'flows': []}


# Function to generate a single switch flow config JSON; returns an object
# Example parameters: dev_id = 1, out_port = 1, dest_ip = 10.0.0.1, l4_type = tcp, l4_port = 5555
def generate_single_json(dev_id, out_port, dest_ip, l4_type, l4_port):
    single_conf_json = {
        "priority": 40000,
        "timeout": 0,
        "isPermanent": 'true',
        "deviceId": f"of:000000000000000{dev_id}",
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": f"{out_port}"
                }
            ]
        },
        "selector": {
            "criteria": [
                {
                    "type": "ETH_TYPE",
                    "ethType": "0x0800"
                },
                {
                    "type": f"{l4_type.upper()}_DST",
                    f"{l4_type}Port": {l4_port}
                },
                {
                    "type": "IPV4_DST",
                    "ip": f"{dest_ip}/32"
                }
            ]
        }
    }

    return single_conf_json


# Adding single flow JSON to a main json object variable - conf_json
def add_entry_to_conf(single_conf_json, json_obj):
    json_obj['flows'].append(single_conf_json)


# Function to create a main json file in a destined location - to this file the main conf_json object will be added
def create_main_json_file(json_obj, path):
    f = open(f'{path}\\config_json.json', 'w')
    f.write(json.dumps(json_obj))
    f.close()
