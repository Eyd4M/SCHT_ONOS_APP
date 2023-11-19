import requests
import json


from requests.auth import HTTPBasicAuth

# Constants needed for sending a proper HTTP POST request to ONOS
HEADERS_POST = {'Content-Type': 'application/json', 'Accept': 'application/json'}
AUTH = HTTPBasicAuth('onos', 'rocks')


def post_config(ip, json_file):
    # Opening a file containing json config
    f = open(json_file, "r")
    j_data = json.loads(f.read())

    url = f'http://{ip}:8181/onos/v1/flows'
    try:
        r = requests.post(url, json=j_data, auth=AUTH, headers=HEADERS_POST)
        r.raise_for_status()
    except Exception as err:
        print(err)
    else:
        print("Konfiguracja powiodła się")

    f.close()
