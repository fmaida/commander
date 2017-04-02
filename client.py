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


class MyTest(Command):

    def __init__(self):
        self.count = 1
        Command.__init__(self)

    def error(self, e):
        self.update_status()
        return "There was an error: {}".format(e)

    def update_status(self):
        self.count += 1
        return "Count total: {}".format(self.count)
        
    def do_msg(self, *args):
        """
        sends chat msg to address, 1st param must be JID of recipient
        Other params are joined as message body
        
        :param args: 
        :return: 
        """

        if len(args) < 1:
            raise ValueError('You need to provide a message')
        return "Hello {}".format(args[0])

    def do_change(self, message):
        c.change_footer(message)

if __name__ == '__main__':

    c = Commander('This is a test client', cmd_cb=MyTest())
    c.loop()
    sys.exit(0)
