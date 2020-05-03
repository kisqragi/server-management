#!/usr/bin/python3

import requests, json, subprocess, ipaddress

ALLOW_IP_LIST = ['x.x.x.x/x']
WEBHOOK_URL = ""
CHANNEL = "#hoge"
USERNAME = "webhookbot"

def check_login():
    ret = '----- check_login -----\n'
    deallow_ip_flag = True
    cmd = 'cat /var/log/auth.log /var/log/auth.log.1 | grep Accepted  | tail -10'
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    for line in proc.stdout.decode('utf-8').split('\n'):
        if not line:
            ret += 'all ok\n'
            break
        line = line.split()
        month = line[0]
        day = line[1]
        time = line[2]
        user = line[8]
        ip = ipaddress.ip_address(line[10])
        deallow_ip_flag = True
        for nw in ALLOW_IP_LIST:
            nw = ipaddress.ip_network(nw)
            if ip in nw:
                deallow_ip_flag = False
        if deallow_ip_flag:
            ret += '{}-{}-{} {} {}\n'.format(month, day, time, user, ip)
            break
    return [deallow_ip_flag, ret]

def doPost(url, channel, username, text):
    payload = json.dumps({
        "channel": channel,
        "username": username,
        "text": text,
    }) 

    requests.post(url, payload)

if __name__ == '__main__':
    text = ""
    ret = check_login()

    if ret[0]:
        text = '<!channel>\n' + text

    text += ret[1]

    doPost(WEBHOOK_URL, CHANNEL, USERNAME, text)
