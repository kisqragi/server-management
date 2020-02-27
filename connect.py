#!/usr/local/bin/python3

import paramiko
import scp 
import os
import datetime
import shutil 

import info
import command_data
import send_mail

from_addr = info.FROM_ADDRESS
to_addr = info.TO_ADDRESS
cc_addrs = info.CC
bcc_addrs = info.BCC
subject = info.SUBJECT
body = info.BODY
password = info.PASSWORD
attach_dir = info.ATTACH_DIR

def check_login(client):
    print('----- check_login -----')
    cmd = 'grep Accepted /var/log/auth.log | tail -10'
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout:
        line = line.split()
        month = line[0]
        day = line[1]
        time = line[2]
        user = line[8]
        ip = line[10]
        deallow_ip_flag = True
        for nw in info.ALLOW_IP_LIST:
            if ip in nw:
                deallow_ip_flag = False
        if deallow_ip_flag:
            out = '{}-{}-{} {} {}'.format(month, day, time, user, ip)
            return out

def get_report(client):
    scp_client = scp.SCPClient(client.get_transport())
    for file_path in info.GET_FILE_LIST:
        scp_client.get(file_path, info.ATTACH_DIR)
    scp_client.close()

def run_cmd(client):
    print('----- run_cmd -----')
    for cmd in command_data.command:
        print('----- ' + cmd + ' -----')
        stdin, stdout, stderr = client.exec_command(cmd)
        for line in stdout:
            print(line, end='')

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(info.ip, username=info.username, password=info.password)

    ret = check_login(client)
    if ret:
        subject = 'checked login'
        msg = send_mail.create_message(from_addr, to_addr, cc_addrs, bcc_addrs, subject)
        send_mail.add_text(msg, ret)
        send_mail.send_mail(from_addr, to_addr, password, msg)

    try:
        os.mkdir('attachment')
    except FileExistsError:
        shutil.rmtree('attachment')
        os.mkdir('attachment')
    get_report(client)
    yesterday = format(datetime.date.today()-datetime.timedelta(days=1), '%Y%m%d')
    subject = 'report' + yesterday
    msg = send_mail.create_message(from_addr, to_addr, cc_addrs, bcc_addrs, subject)
    send_mail.attach_file(msg, attach_dir)
    send_mail.send_mail(from_addr, to_addr, password, msg)

    #run_cmd(client)

    client.close()


if __name__ == '__main__':
    main()
