#!/usr/bin/python
import socket
import sys
import ssl
import time
import getopt
import os
import shutil
import thread


def main(argv):
    # Bot takes a single argument which defines the current session by name and its configuration files
    # This allows you to have different bots running at the same time, by just changing their _config.txt
    try:
         opts, args = getopt.getopt(argv, "n:d", ["name="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Read out the session name from the argument and check for an already existing folder using that name
    session_name = sys.argv[1]
    if not os.path.exists(session_name):
        os.makedirs(session_name)
    os.chdir(session_name)
    print("CURRENT SESSION NAME: %s" %(session_name))

    # Ensures there is always a config file that works

    if not os.path.exists('config.txt'):
        os.chdir("..")
        shutil.copy('sample_config.txt', session_name+'/'+'config.txt')
        os.chdir(session_name)


    #grab config from .txt
    with open('config.txt', 'r') as f:
        config_strings = ''
        for line in f:
            if line[0] != '/':
                config_strings = config_strings+line+''
    try:
        config_split = str.split(config_strings)
        # print(config_split)
        server = config_split[0]
        port = int(config_split[1])
        botnick = config_split[2]
        password = config_split[3]
        channel = []
        for v in config_split:
            if v[0] == '#':
                channel.insert(0, v)
    except Exception as e:
        print("Exception '%s' , check your config.txt for errors") %(e)
        sys.exit(2)


    irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc = ssl.wrap_socket(irc_socket) # is SSL really needed? some servers don't support it. could probably write
    # auto detection for it.
    # irc = irc_socket


    print("Connecting to: %s" %(server))
    irc.connect((server, port))
    irc.setblocking(False)
    irc.send("PASS %s\n" %(password))
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick + " :bot\n")
    irc.send("NICK "+ botnick +"\n")
    irc.send("PRIVMSG nickserv :identify %s %s\r\n" %(botnick, password)) #differentiate between qnet and nickserv?
    for v in channel:
        irc.send("JOIN "+ v +"\n")


    connected = True

    # ghetto as fuck
    allowed_log_strings = ['NOTICE', 'PRIVMSG', 'JOIN', 'PART', 'TOPIC', 'KICK', 'BAN', 'MODE', 'NAMES', 'LIST',
    'INVITE', 'LUSERS', 'VERSION', 'STATS', 'LINKS', 'TIME', 'INFO' ]

    # Main Loop
    while connected:
        time.sleep(0.1)
        try:
            text=irc.recv(2040)
            text = text.strip('\n\r')
            incoming_text = text.lower()
            print(text)





            if text.find('PING') != -1:
                irc.send('PONG ' + text.split() [1] + '\r\n')

            # write Log
            with open('log.txt', 'a') as f:
                if any(string in text for string in allowed_log_strings):
                    f.write('\n'+text)

        except Exception as e:
            continue


        # map out a proper command engine
        # simple echo commands, timed repeats, sending commands to irc server
        # python parsing? so you can add something like a google script?

        # echo
        command = ':!echo'
        if incoming_text.find(command) !=-1:
            received_text = text.split()
            print(received_text)
            received_channel = received_text[2]
            received_command = received_text[3]
            received_message = received_text[4]
            outgoing_message = str(' ' + received_command + ' ' + received_message)
            irc.send('PRIVMSG ' + str(received_channel) +  outgoing_message + '\r\n')


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
            print("start main.py with a name (ex. 'main.py test')")
