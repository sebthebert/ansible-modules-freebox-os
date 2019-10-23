#!/usr/bin/python
# Copyright (c) 2019 Sebastien Thebert

"""freebox_os_switch_port Ansible module."""

import json
import requests

from ansible.module_utils.basic import AnsibleModule

try:
    from library.module_utils.network.freebox_os import freebox_os_api_url, freebox_os_api_login
except ImportError:
    from ansible.module_utils.network.freebox_os import freebox_os_api_url, freebox_os_api_login

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: freebox_os_switch_port

short_description: Configure Switch Port on Freebox OS

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
# Configure Freebox Router port '2' with 'full' duplex and speed '1000'
- name: Configure port '2' with 'full' duplex and speed '1000'
  freebox_os_switch_port:
    id: 2
    duplex: 'full'
    speed: 1000
'''

RETURN = '''

'''

AVAILABLE_PORTID = [1, 2, 3, 4]
AVAILABLE_DUPLEX = ['auto', 'half', 'full']
AVAILABLE_SPEED = ['auto', '10', '100', '1000']

session_token= freebox_os_api_login()
HEADERS = {"X-Fbx-App-Auth": session_token}

def main():
    """freebox_os_switch_port main() function."""

    module_args = dict(
        id=dict(type='int', required=True),
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
    if module.params['id'] not in AVAILABLE_PORTID:
        module.fail_json(msg="Invalid 'id' value", **result)
    if module.params['duplex'] not in AVAILABLE_DUPLEX:
        module.fail_json(msg="Invalid 'duplex' value", **result)
    if module.params['speed'] not in AVAILABLE_SPEED:
        module.fail_json(msg="Invalid 'speed' value", **result)

    # Request to Freebox OS API '/switch/port/<id>'
    response = requests.get(
        freebox_os_api_url + '/switch/port/' + str(module.params['id']),
        headers=HEADERS)
    json_data = json.loads(response.text)
    if module.params['duplex'] != json_data['result']['duplex']:
        result['changed'] = True
    if module.params['speed'] != json_data['result']['speed']:
        result['changed'] = True

    if result['changed'] is True and module.check_mode is False:
        payload = {'duplex': module.params['duplex'], 'speed': module.params['speed']}
        payload = json.dumps(payload)
        response = requests.put(
            freebox_os_api_url + '/switch/port/' + str(module.params['id']),
            data=payload,
            headers=HEADERS)
        result['msg'] = response.text

    module.exit_json(**result)

if __name__ == '__main__':
    main()
