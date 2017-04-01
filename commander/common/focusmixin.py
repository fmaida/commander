class FocusMixin:

    def mouse_event(self, size, event, button, x, y, focus):

        if focus and hasattr(self, '_got_focus') and self._got_focus:
            self._got_focus()
        return super(FocusMixin, self).mouse_event(size, event, button, x, y, focus)
