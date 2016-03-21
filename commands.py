# Contains all commands for the bot
# TODO: change commands.py to getting read only in the respective subfolder, similar to config.txt
def check_text(incoming_text):
    try:

        received_text = incoming_text.split()

        # for x in received_text:
        #     print(x)
        received_username = received_text[0]
        received_keyword = received_text[1]
        received_channel = received_text[2]
        received_command = received_text[3]
        received_message = received_text[4:]
        received_message = " ".join(received_message)


        # test command
        if received_command == (':!echo'):
            print('received_command ' + received_command)
            print('received_message ' + str(received_message))
            outgoing_message = str(' ' + received_command + ' ' + received_message)
            print('outgoing_message '+outgoing_message)
            returned_text = ('PRIVMSG ' + str(received_channel) +  outgoing_message + '\r\n')
            print('returned_text '+returned_text)

        # returns the first search result from Google
        # not working
        if received_command == (':!g'):
            print('received_command ' + received_command)
            print('received_message ' + str(received_message))
            returned_text = ('PRIVMSG ' + str(received_channel) + " Google result for " + '"'+received_message+'"' + " :" + 'https://www.google.com/?gws_rd=ssl#safe=off&q='+received_message+'&btnK=Google+Search' + '\r\n' )

        return returned_text

    except Exception as e:
        print(e)
