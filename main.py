#!/usr/bin/python
import socket
import sys
import ssl
import time
import getopt
import os
import shutil
import commands


def main(argv):
    # Bot takes a single argument which defines the current session by name and its configuration files
    # This allows you to have different bots running at the same time, by just changing their config.txt and running
    # another file with a different commandline argument.
    try:
         opts, args = getopt.getopt(argv, "n:d", ["name="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Read out the instance name from the argument and check for an already existing folder with that name
    session_name = sys.argv[1]
    if not os.path.exists(session_name):
        os.makedirs(session_name)
    os.chdir(session_name)
    print("CURRENT SESSION NAME: %s" %(session_name))

    # Ensures there is always a config file that works
    # TODO: Recreate sample_config.txt from scratch if its missing
    if not os.path.exists('config.txt'):
        os.chdir("..")
        shutil.copy('sample_config.txt', 'config.txt')
        os.chdir(session_name)


    # Grab config from config.txt
    # This is a bit rudimentary, but it does the job.
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
    irc = irc_socket
    # irc = ssl.wrap_socket(irc_socket) # is SSL really needed? some servers don't support it.
    # TODO: Add SSL auto detection

    # Establish connection

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

    # Not pretty
    allowed_log_strings = ['NOTICE', 'PRIVMSG', 'JOIN', 'PART', 'TOPIC', 'KICK', 'BAN', 'MODE', 'NAMES', 'LIST',
    'INVITE', 'LUSERS', 'VERSION', 'STATS', 'LINKS', 'TIME', 'INFO' ]

    # Main Loop
    while connected:
        time.sleep(0.3)
        try:
            text=irc.recv(2040)
            text = text.strip('\n\r')
            incoming_text = text.lower()
            print(text)

            if text.find('PING') != -1:
                irc.send('PONG ' + text.split() [1] + '\r\n')

            # write Log
            # TODO: Log Formating
            with open('log.txt', 'a') as f:
                if any(string in text for string in allowed_log_strings):
                    f.write('\n'+text)

            # Send text to commands.py, which then parses it
            # and if it finds a matching command, it executes the matching code
            text_to_be_checked = commands.check_text(text)
            print('text_to_be_checked '+text_to_be_checked)
            irc.send(text_to_be_checked)


        except Exception as e:
            # print(e)
            continue



# Requires a name argument to start an instance of the bot.
if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
            print("start main.py with a name (ex. 'main.py test')")
