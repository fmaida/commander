from commander import Commander
from commander.exceptions import UnknownCommand


class Command:
    """
    Base class to manage commands in commander
    similar to cmd.Cmd in standard library
    just extend with do_something  method to handle your commands
    """

    status_bar = "Command:  (Tab to switch focus to upper frame, where you can scroll text)"

    def __init__(self, status_bar=None, quit_commands=["q", "quit", "exit", "bye"],
                 help_commands=["help", "?", "h"]):

        if status_bar:
            self.status_bar = status_bar
        self._quit_cmd = quit_commands
        self._help_cmd = help_commands

    def __call__(self, line):
        """
        Each time this class is called

        :param line: 
        :return: 
        """

        tokens = line.split()  # Split the line based on spaces
        cmd = tokens[0].lower()  # Takes the first argument as command
        args = tokens[1:]  # Takes the remaining arguments as parameters

        if cmd in self._quit_cmd:  # When the user needs to exit
            return Commander.Exit
        elif cmd in self._help_cmd:  # When the user needs help
            return self.help(args[0] if args else None)
        elif hasattr(self, 'do_' + cmd):
            # When the user needs to call a command and the class has it
            return getattr(self, 'do_' + cmd)(*args)
        else:
            # Don't know what to do, raises an exception
            raise UnknownCommand(cmd)

    def help(self, cmd=None):

        def std_help():
            qc = "|".join(self._quit_cmd)
            hc = "|".join(self._help_cmd)
            res = "Type {} command_name to get more help about particular command\n".format(hc)
            res += 'Type {} to quit program\n'.format(qc)
            # List all the methods available in the class (introspection)
            cl = [name[3:] for name in dir(self) if name.startswith('do_') and len(name) > 3]
            res += "Available commands: {}".format(' '.join(sorted(cl)))
            return res

        if not cmd:
            # No command class has been passed, so the standard
            # help will be used in its place
            return std_help()
        else:
            # Command class has been passed, it takes every method
            # from that class and its relative docstring to show
            # it onscreen
            try:
                fn = getattr(self, "do_{}".format(cmd))
                doc = fn.__doc__
                return doc or "No documentation available for {}".format(cmd)
            except AttributeError:
                return std_help()
