import threading
import urwid
from commander.common import FocusMixin


class ListView(FocusMixin, urwid.ListBox):
    def __init__(self, model, got_focus, max_size=None):
        urwid.ListBox.__init__(self, model)
        self._got_focus = got_focus
        self.max_size = max_size
        self._lock = threading.Lock()

    def add(self, line):
        with self._lock:
            was_on_end = (self.get_focus()[1] == len(self.body) - 1)
            if self.max_size and len(self.body) > self.max_size:
                del self.body[0]
            self.body.append(urwid.Text(line))
            last = len(self.body) - 1
            if was_on_end:
                self.set_focus(last, 'above')
