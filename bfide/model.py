import gtk
import gobject

class Model(object):
    def __init__(self):
        self.memory = gtk.ListStore(int, int)
        self.reset()

    def reset(self):
        self.pointer = 0
        self.memory.clear()
        for i in range(256):
            self.memory.append((i,0))

    def get_value_at_pointer(self):
        return self.memory[self.pointer][1]

    # >
    def inc_pointer(self):
        self.pointer += 1

    # <
    def dec_pointer(self):
        self.pointer -= 1

    # +
    def inc_at_pointer(self):
        self.memory[self.pointer][1] += 1

    # -
    def dec_at_pointer(self):
        self.memory[self.pointer][1] -= 1
