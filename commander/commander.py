import threading
import urwid
from commander import ListView
from commander import Input
from commander.exceptions import UnknownCommand


class Commander(urwid.Frame):
    """ 
    Simple terminal UI with command input on bottom line and display frame above
    similar to chat client etc.
    Initialize with your Command instance to execute commands and the start main 
    loop Commander.loop().
    You can also asynchronously output messages with Commander.output('message')
    """

    buffered_status = ""

    class Exit:
        pass

    PALETTE = [('reversed', urwid.BLACK, urwid.LIGHT_GRAY),
               ('normal', urwid.LIGHT_GRAY, urwid.BLACK),
               ('error', urwid.LIGHT_RED, urwid.BLACK),
               ('green', urwid.DARK_GREEN, urwid.BLACK),
               ('blue', urwid.LIGHT_BLUE, urwid.BLACK),
               ('magenta', urwid.DARK_MAGENTA, urwid.BLACK), ]

    def __init__(self, title, cmd_cb=None, max_size=1000):

        self.header = urwid.Text(title)
        self.model = urwid.SimpleListWalker([])
        self.body = ListView(self.model, lambda: self._update_focus(False), max_size=max_size)
        self.input = Input(lambda: self._update_focus(True))
        self._cmd = cmd_cb
        urwid.Frame.__init__(self,
                             urwid.AttrWrap(self.body, "normal"),
                             urwid.AttrWrap(self.header, "reversed"),
                             self._change_footer())
        self.set_focus_path(["footer", 1])
        self._focus = True
        urwid.connect_signal(self.input, "line_entered", self.on_line_entered)
        self._output_styles = [s[0] for s in self.PALETTE]
        self.eloop = None
        self._eloop_thread = None

    def set_title(self, new_title):
        """
        Set the new title of the commander window
        
        :param new_title: 
        :return: 
        """

        self.header = urwid.AttrMap(urwid.Text(new_title), "reversed")

    def _change_footer(self, message=None):

        # If the status bar needs to be updated, it does so
        if message is None:
            message = self._cmd.update_status()
        self.buffered_status = message
        return urwid.Pile([urwid.AttrMap(urwid.Text(message), "reversed"),
                           urwid.AttrMap(self.input, "normal")])

    def loop(self, handle_mouse=False):
        self.eloop = urwid.MainLoop(self, self.PALETTE, handle_mouse=handle_mouse)
        self._eloop_thread = threading.current_thread()
        self.eloop.run()

    def on_line_entered(self, line):

        # Let's look at the command just entered
        if self._cmd:
            # If the commander has a "command" instance

            try:
                res = self._cmd(line)
            except UnknownCommand as e:
                self.output(self._cmd.error(e), "error")
                return
            except Exception as e:
                self.output('Error: %s' % e, "error")
                return

            if res == Commander.Exit:
                # If the user wants to exit
                raise urwid.ExitMainLoop()
            elif res:
                self.output(str(res))

                msg = self._cmd.update_status()
                if self.buffered_status != msg:
                    urwid.Frame.footer = self._change_footer(msg)

        else:
            # If Commander doesn't have an instance of "Command"

            if line in ("q", "quit", "exit", "bye"):
                raise urwid.ExitMainLoop()
            else:
                self.output(line)

    def output(self, line, style=None):
        if style and style in self._output_styles:
            line = (style, line)
        self.body.add(line)
        # since output could be called asynchronously form
        # other threads we need to refresh screen in these cases
        if self.eloop and self._eloop_thread != threading.current_thread():
            self.eloop.draw_screen()

    def _update_focus(self, focus):
        self._focus = focus

    def switch_focus(self):
        if self._focus:
            self.set_focus("body")
            self._focus = False
        else:
            self.set_focus_path(["footer", 1])
            self._focus = True

    def keypress(self, size, key):
        if key == 'tab':
            self.switch_focus()
        return urwid.Frame.keypress(self, size, key)
