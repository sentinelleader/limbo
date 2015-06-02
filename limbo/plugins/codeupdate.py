"""Only direct messages are accepted, format is @user codeupdate <tag> <env>"""

try:
    from urllib import quote, unquote
except ImportError:
    from urllib.request import quote, unquote
import requests
import json
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

def codeupdate(ans_env, ans_tag):
    base_url = get_url(ans_env)
    req_url = base_url + '/ansible/update-code/'
    resp = requests.post(req_url, data={'tags': ans_tag, 'env': ans_env})
    return [resp.status_code, resp.text]

def on_message(msg, server):
    init_msg =  unicodedata.normalize('NFKD', msg['text']).encode('ascii','ignore').split(' ')[0]
### slight hackish method to check if the message is a direct message or not
    if init_msg == '<@xxxxxx>:':    # Message is actually a direct message to the Bot
        orig_msg =  unicodedata.normalize('NFKD', msg['text']).encode('ascii','ignore').split(' ')[2:]
        msg_user = msg['user']
        msg_channel = msg['channel']
        if msg_user in ALLOWED_USERS and msg_channel in ALLOWED_CHANNELS:
            env = orig_msg[1]
            if env not in ALLOWED_ENV:
                return "Please Pass a Valid Env (xxxx/yyyy)"
            tag = orig_msg[0]
            if tag not in ALLOWED_TAG:
                return "Please Pass a Valid Tag (xxxx/yyyy)"
            return codeupdate(env, tag)
        else:
            return ("!!! You are not Authorized !!!")
    else:
        print "Not a Direct Message, Ignoring...."

