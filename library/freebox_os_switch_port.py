#!/usr/bin/python
# Copyright (c) 2019 Sebastien Thebert

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: freebox_os_switch_port

short_description: Configure Switch Port for Freebox OS

version_added: "2.8"

description:
    Configure Switch Port for Freebox OS.
    https://dev.freebox.fr/sdk/os/switch/

options:
    id:
        description:
            - port id (1 to 4)
        required: true
    duplex:
        description:
            - port duplex mode ('auto', 'half' or 'full')
        required: false
    speed:
        description:
            - port speed ('auto', '10', '100' or '1000')
        required: false    

author:
    - Sebastien Thebert (sebthebert@gmail.com)
'''

EXAMPLES = '''
# Configure port 2 with duplex 'full' and speed '1000'
- name: Configure port 2 with duplex 'full' and speed '1000'
  freebox_os_switch_port:
    id: 2
    duplex: 'full'
    speed: 1000
'''

RETURN = '''

'''

import hashlib
import hmac
import json
import os
import requests

from ansible.module_utils.basic import AnsibleModule

available_portid = ['1', '2', '3', '4']
available_duplex = ['auto', 'half', 'full']
available_speed = ['auto', '10', '100', '1000']

freebox_os_api_appid = 'com.ansible.modules.freebox'
freebox_os_api_url = os.getenv('FREEBOX_OS_API_URL', 'http://mafreebox.freebox.fr/api/v6')
response = requests.get(freebox_os_api_url + '/login')
json_data = json.loads(response.text)
challenge = json_data['result']['challenge']

response = requests.get(freebox_os_api_url + '/login/authorize/13')

app_token = os.getenv('FREEBOX_OS_API_APP_TOKEN', '')
payload = {'app_id': freebox_os_api_appid, 'password': hmac.new(app_token,challenge,hashlib.sha1).hexdigest()}
payload = json.dumps(payload)

response = requests.post(freebox_os_api_url + '/login/session', data=payload)

json_data = json.loads(response.text)
session_token = json_data['result']['session_token']


headers = {"X-Fbx-App-Auth": session_token}


def main():
    module_args = dict(
        id=dict(type='str', required=True),
        duplex=dict(type='str', required=False),
        speed=dict(type='str', required=False)
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    result = dict(
        changed=False
    )

    # Validate module parameters
    if module.params['id'] not in available_portid:
        module.fail_json(msg="Invalid 'id' value", **result)
    if module.params['duplex'] not in available_duplex:
        module.fail_json(msg="Invalid 'duplex' value", **result)
    if module.params['speed'] not in available_speed:
        module.fail_json(msg="Invalid 'speed' value", **result)

    # Request to Freebox OS API '/switch/port/<id>'
    response = requests.get(freebox_os_api_url + '/switch/port/' + module.params['id'], headers=headers)
    json_data = json.loads(response.text)

    if module.params['duplex'] != json_data['result']['duplex']:
        result['changed'] = True
    if module.params['speed'] != json_data['result']['speed']:
        result['changed'] = True

    if result['changed'] == True and module.check_mode == False:
        payload = {'duplex': module.params['duplex'], 'speed': module.params['speed']}
        payload = json.dumps(payload)
        response = requests.put(freebox_os_api_url + '/switch/port/' + module.params['id'], data=payload, headers=headers)
        result['msg'] = response.text

    module.exit_json(**result)

if __name__ == '__main__':
    main()