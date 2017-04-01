"""
Created on Aug 2, 2015

@author: ivan
"""


from threading import Thread
from commander.listview import ListView
from commander.input import Input
from commander.commander import Commander
from commander.command import Command


if __name__ == "__main__":

    class TestCmd(Command):

        def do_echo(self, *args):
            """
            echo - Just echos all arguments
            
            :param args: 
            :return: 
            """

            return " ".join(args)

        def do_raise(self, *args):
            raise Exception('Some Error')


    c = Commander('Test', cmd_cb=TestCmd())

    # Test asynch output -  e.g. comming from different thread
    import time


    def run():
        while True:
            time.sleep(1)
            c.output("Tick", "green")


    t = Thread(target=run)
    t.daemon = True
    t.start()

    # start main loop
    c.loop()
