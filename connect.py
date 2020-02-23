import info
import command_data
import paramiko

def check_login(client):
    #print('----- check_login -----')
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
            print(out)

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(info.ip, username=info.username, password=info.password)

    for cmd in command_data.command:
        #print('----- ' + cmd + ' -----')
        stdin, stdout, stderr = client.exec_command(cmd)
        for line in stdout:
            print(line, end='')

    check_login(client)

    client.close()


if __name__ == '__main__':
    main()
