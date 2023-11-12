import json

# Json object to which all single flow jsons will be added
conf_json = {'flows': []}


# Function to generate a single switch flow config JSON; returns an object
def generate_single_json(dev_id, out_port, dest_ip):
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
