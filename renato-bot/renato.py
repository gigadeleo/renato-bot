# -*- coding: utf-8 -*-

"""renato-bot a Python-based Slack Bot client whose purpose is to help you learn a new Maltese word every day.
renato answers to a handful of different commands:
* 
"""
import os
import time
import random 
from commands.motd import *
from slackclient import SlackClient

# renato's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# commands known to renato. 
# comment out any ones you don't need.
HELP = "help"
HELLO = "hello"
KANTALI = "kantali"
MOTD = "motd"

# random selection or responses
HELLOS = ['Bonġu dawl t\'għajnejja',
          'Aw muqran!',
          'X\'għandna ġisem!',
          'Aw sexlife']

BANTERS = ['Mela le ħanini',
           'Għalik nagħmel dan, u aktar!',
           'Ħa! Magħżula apposta għalik!',
           'Iii kemm inħobb!!!']

SONGS = ['https://www.youtube.com/watch?v=A-pcwbVl_qc',
           'https://www.youtube.com/watch?v=X5-C1Kx_JNA',
           'https://www.youtube.com/watch?v=Qg_AhuBqQUI',
           'https://www.youtube.com/watch?v=l407bnafnlU']

OOPS = ['Toni taghni tina talli taghjtu tuta tajba, talli taghjtu tuta tajba Toni taghni tina.',
           'Dari rari tara re, tara lira tara re.',
           'Ħija taġhni ħawħa u qalli: "Ħa, ħi, ħudu u ħawilla fil-ħamrija ħamra taħt il-ħitan tà Ħararaw.',
           'Trakk fuq trakk. Trakk taħt trakk.',
           'Ġorġ raġa’ ġà mill-gaġġa tal-ġgant.',
           'Platt fuq platt, platt taħt platt.',
           'Qafas tal-qasab imdendel mas-saqaf.',
           'Patri minn Napli mar Kapri għall-papri; Mela f\'Napli m\'hemmx papri; Biex patri minn Napli mar Kapri għall-papri',
           'Tqaħqaħt tqaħqieqa u t-tqaħqieha li tqaħqaht kienet tqaħqieha kbira.',
           'Il-pespus pespes pespisa lil pespusa tal-pespus u l-pespusa tal-pespus għat-tpespisa tal-pespus, pespset.',
           'Platti ċatti platti fondi, int u tiekol tikkonfondi.']

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# main function
# recieves commands in a DM or Channel and determines if they are directed to bot / valid.
# if so, it acts on the commands or replies asking for clarification.
def handle_command(command, channel):

    # checks for HELP command
    # replies with a standard help menu
    if command.startswith(HELP):
    	response = """Hi! I'm Renato! and this is the 'help' menu. These are the commands I am familiar with:\n
> *hello* - Use this if you want to be amused.\r
> *motd* - Use this to load the :flag-mt: Maltese :flag-mt: word of the day.\r
> *kantali* - Use this to load up a suggestion from Renato's favourite playlist.\r
> *help* - To load up this menu.\n\n
Usage Example:  
 • In a channel, type ` @renato <command>` to make me do something.
 • In a direct message type `<command>`.

 Disclaimer: Any resemblance between 'this bot' and any persons, living or dead, is purely unintentional."""

    # checks for MOTD command
    # replies with MOTD as image and includes phrase examples underneath.
    elif command.startswith(MOTD):
        values = extract_word()
        file = create_mwotd (values[0],values[1],values[2])
        example_phrase = values[3]
        post_image(filename=file, token=SLACK_BOT_TOKEN, channels=channel)

        response = example_phrase
    
    # checks for HELLO command
    # replies with a random hello reply back
    elif command.startswith(HELLO):
        response = random.choice(HELLOS)

    # checks for KANTALI command
    # replies with a random song and banter response.
    elif command.startswith(KANTALI):
        banter = random.choice(BANTERS)
        song = random.choice(SONGS)

        response = banter + "  " + song

    # no match found
    # replies with a random Maltese tongue twister.
    else:
        response = random.choice(OOPS)
    
    # invokes the chat.postMessage command to post a custom response back to the channel
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

# this function takes messages from Slack and determines if they are directed at renato. 
# messages in channels that start with a direct command to our bot ID OR direct messages are handled by this code.
def parse_slack_output(slack_rtm_output):

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            
            # if renato messaged in Channel - @ required
            if (output and \
                'text' in output and \
                AT_BOT in output['text']):
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
            
            # if messaged in DM and not a bot message - @ not required
            elif (output and \
                'text' in output and \
                'user' in output and \
                output['channel'].startswith("D") and \
                'bot_id' not in output):

                return output['text'].lower(), \
                output['channel']
                #if output and 'bot_id' in output:
                #    pass
                #else:
                #    return output['text'], output['channel']

    return None, None

# connect to the Slack RTM API WebSocket and loop while parsing messages from the firehose.
# if any of the messages are directed at renato call 'handle_command' to determine what to do.
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("renato connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")