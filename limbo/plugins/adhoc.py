"""Only direct messages are accepted, format is <user> <env> <host> <mod> <args_if_any"""

try:
    from urllib import quote, unquote
except ImportError:
    from urllib.request import quote, unquote
import re
import requests
import json
from random import shuffle
import unicodedata

ALLOWED_CHANNELS = []
ALLOWED_USERS = ['xxxxx']
ALLOWED_ENV = ['xxx', 'xxx']
ALLOWED_TAG = ['xxx', 'xxx']

BOOTSTRAPPER__PROD_URL = "http://xxx.xxx.xxx.xxx:yyyy"
BOOTSTRAPPER_STAGING_URL = "http://xxx.xxx.xxx.xxx:yyyy"

def get_url(infra_env):
    if infra_env == "prod":
        return BOOTSTRAPPER__PROD_URL
    else:
        return BOOTSTRAPPER_STAGING_URL

def adhoc(ans_host, ans_mod, ans_arg, ans_env):
    base_url = get_url(ans_env)
    req_url = base_url + '/ansible/adhoc/'
    if ans_arg is None:
        resp = requests.get(req_url, params={'host': ans_host, 'mod': ans_mod})
    else:
        resp = requests.get(req_url, params={'host': ans_host, 'mod': ans_mod, 'args': ans_arg})
    return [resp.status_code, resp.text]

def on_message(msg, server):
### slight hackish method to check if the message is a direct message or not
    init_msg =  unicodedata.normalize('NFKD', msg['text']).encode('ascii','ignore').split(' ')[0]
    if init_msg == '<@xxxxxxx>:':    # Message is actually a direct message to the Bot
        orig_msg =  unicodedata.normalize('NFKD', msg['text']).encode('ascii','ignore').split(' ')[2:]
        msg_user = msg['user']
        msg_channel = msg['channel']
        if msg_user in ALLOWED_USERS and msg_channel in ALLOWED_CHANNELS:
            env = orig_msg[0]
            if env not in ALLOWED_ENV:
                return "Only Dev Environment is Supported Currently"
            host = orig_msg[1]
            mod = orig_msg[2]
            arg = orig_msg[2:]
            return adhoc(host, mod, arg, env)
        else:
            return ("!!! You are not Authorized !!!")
    else:
        return "Invalid Message, Format: <user> <env> <host> <mod> <args_if_any>"
