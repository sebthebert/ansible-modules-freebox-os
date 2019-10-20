import hashlib
import hmac
import json
import os
import requests

freebox_os_api_appid = 'com.ansible.modules.freebox'
freebox_os_url = os.getenv('FREEBOX_OS_URL', 'http://mafreebox.freebox.fr')

def freebox_os_api_version():
    response = requests.get(freebox_os_url + '/api_version')
    json_data = json.loads(response.text)

    return json_data['api_version'].split('.')[0]

freebox_os_api_url = freebox_os_url + '/api/v' + freebox_os_api_version()

def freebox_os_api_login():
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

    return session_token