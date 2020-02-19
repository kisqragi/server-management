import connect_info as info
import command_data
import paramiko

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(info.ip, username=info.username, password=info.password)

    count = 1
    for cmd in command_data.command:
        #print('-------command-{}-------'.format(count))
        count += 1
        stdin, stdout, stderr = client.exec_command(cmd)
        for line in stdout:
            print(line, end='')

    client.close()


if __name__ == '__main__':
    main()
