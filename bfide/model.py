import gtk
import gobject

class Model(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, int, int)
        self.reset()

    def reset(self):
        for i in range(256):
            self.append((i,0))
