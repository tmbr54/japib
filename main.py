#!/usr/bin/python
import socket
import sys
import ssl
import time
import getopt
import os
import shutil


#Configuration
def main(argv):
    #Bot takes a single argument which defines the current session by name and its configuration files
    #This allows you to have different bots running all off of the same file, by just changing its _config.txt
    try:
         opts, args = getopt.getopt(argv, "n:d", ["name="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    #Read out the session name from the argument and check for an already existing folder using that name
    session_name = sys.argv[1]
    if not os.path.exists(session_name):
        os.makedirs(session_name)
    os.chdir(session_name)
    print("CURRENT SESSION NAME: %s" %(session_name))

    #Ensures there is always a config file that works
    if not os.path.exists('config.txt'):
        os.chdir("..")
        shutil.copy('sample_config.txt', session_name+'/'+'config.txt')
        os.chdir(session_name)

    with open('config.txt', 'r') as f:
        config_strings = ''
        for line in f:
            if line[0] != '/':
                config_strings = config_strings+line+''

    config_split = str.split(config_strings)
    print(config_split)
    server = config_split[0]
    port = int(config_split[1])
    botnick = config_split[2]
    password = config_split[3]
    channel = []
    for v in config_split:
        if v[0] == '#':
            channel.insert(0, v)
    connected = True
    # #Tail log
    # tail_file = [
    # 'log/log.txt'
    # ]
    irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc = ssl.wrap_socket(irc_socket)


    print("Connecting to: %s" %(server))
    irc.connect((server, port))
    irc.setblocking(False)
    irc.send("PASS %s\n" %(password))
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Testbot\n")
    irc.send("NICK "+ botnick +"\n")
    irc.send("PRIVMSG nickserv :identify %s %s\r\n" %(botnick, password)) #differentiate between qnet and nickserv?
    for v in channel:
        irc.send("JOIN "+ v +"\n")


    # tail_line = []
    # for i, tail in enumerate(tail_file):
    #     tail_line.append('')

    while connected:
        time.sleep(0.5)

        # #Tail file
        # for i, tail in enumerate(tail_file):
        #     try:
        #         f = open(tail, 'r')
        #         line = f.readlines()[-1]
        #         f.close()
        #         if tail_line[i] != line:
        #             tail_line[i] = line
        #             irc.send("PRIVMSG %s :%s" % (channel, line))
        #     except Exception as e:
        #         print ("Error found in file %s" % (tail))
        #         print(e)


        try:
            text=irc.recv(2040)
            print(text)

            if text.find('PING') != -1:
                irc.send('PONG ' + text.split() [1] + '\r\n')

            if text.find(':!test') !=-1:
                t = text.split(':!test')
                to = t[1].strip()
                irc.send('PRIVMSG '+channel+' :Test worked! '+str(to)+'!\r\n')
        except Exception:
            continue


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
            print("start main.py with a name (ex. 'main.py test')")
