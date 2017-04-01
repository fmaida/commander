#! /usr/bin/env python

"""
Created on Jul 14, 2015

@author: ivan
"""


import sys
from commander import Commander, Command


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


class Gigetto(Command):

    def __init__(self):
        self.count = 1
        Command.__init__(self)

    def status_line(self):
        self.count += 1
        self.status = "Count total: {}".format(self.count)
        
    def do_msg(self, *args):
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

    def do_change(self, message):
        c.change_footer(message)

if __name__ == '__main__':

    c = Commander('This is a test client', cmd_cb=Gigetto())
    c.loop()
    sys.exit(0)
