#! /usr/bin/env python
'''
Created on Jul 14, 2015

@author: ivan
'''

import sys
import logging
from commander import Commander,Command

logger = logging.getLogger()


def indent(elem, level=0):
    """
    Indent text
    
    :param elem: 
    :param level: Level of indentation 
    :return: 
    """

    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

class ChatClient:

    def __init__(self, jid, password, rooms, print_fn=None):
        pass
        
#     def message(self, msg):
#         if msg['type']=='groupchat':
#             return
#         elif msg['type']=='error':
#             logger.error('ERROR MSG: %s', msg)
#             return
#         logger.debug("MESSAGE: %s [%s] - %s", msg['from'], msg['type'], msg['body'])
#         
#     
#     def muc_message(self, msg):
#         logger.debug("%s::%s [%s] - %s" , msg['from'], msg['mucnick'], msg['type'], msg['body'])
#         
#     
#     def changed_status(self, prezence):
#         logger.debug( 'STATUS %s', prezence)
#         
#     def roster_update(self, roster):
#         logger.debug('ROSTER %s', roster)


class Gigetto(Command):
    def __init__(self):
        Command.__init__(self)
        
    def do_msg(self,*args):
        """
        sends chat msg to address, 1st param must be JID of recipient
        Other params are joined as message body
        
        :param args: 
        :return: 
        """

        # if len(args)<2:
        #     raise ValueError('Atleat two parameters are expected - recipient and message')
        # xc.send_message(mto=args[0], mbody=' '.join(args[1:]), mtype='chat')
        return "Hello {}".format(args[0])

if __name__ == '__main__':

    # xc=ChatClient(args.user, args.pwd, args.room)
    c=Commander('This is a test client', cmd_cb=Gigetto())
    # xc.print_fn=c.output
    
    c.loop()
    # xc.disconnect()
    sys.exit(0)
