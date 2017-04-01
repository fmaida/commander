from collections import deque
import urwid
from commander.common import FocusMixin


class Input(FocusMixin, urwid.Edit):
    signals = ['line_entered']

    def __init__(self, got_focus=None):
        urwid.Edit.__init__(self)
        self.history = deque(maxlen=1000)
        self._history_index = -1
        self._got_focus = got_focus

    def keypress(self, size, key):
        """
        Manages keypress on the response list window

        :param size: 
        :param key: 
        :return: 
        """

        if key == 'enter':
            # Enter the command and send a copy of the command
            # to the command history manager

            line = self.edit_text.strip()  # Strip the white spaces
            if line:  # If the line entered wasn't blank
                urwid.emit_signal(self, 'line_entered', line)
                self.history.append(line)  # Add a copy to the history manager
            self._history_index = len(self.history)  # Put the history index to its latest value
            self.edit_text = ""

        if key == 'up':
            # From command history grabs the previous command entered

            self._history_index -= 1
            if self._history_index < 0:
                self._history_index = 0
            else:
                self.edit_text = self.history[self._history_index]

        if key == 'down':
            # From command history grabs the next command entered
            self._history_index += 1
            if self._history_index >= len(self.history):
                self._history_index = len(self.history)
                self.edit_text = ""
            else:
                self.edit_text = self.history[self._history_index]
        else:
            urwid.Edit.keypress(self, size, key)
