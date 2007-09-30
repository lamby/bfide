import gtk
import gobject

class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def setup(self, xml):
        xml.signal_autoconnect(self)
        self.view.setup(self.model.memory)

    def on_toolbutton_run_clicked(self, *_):
        self.model.reset()
        self.view.set_running(True)

        self.program = self.view.get_editor_text()
        self.program_counter = 0
        self.stack = []
        self.running = True
        self.exec_next()

    def on_toolbutton_stop_clicked(self, *_):
        self.stop()

    def on_window_main_delete_event(self, *_):
        gtk.main_quit()

    def exec_next(self):
        try:
            fn = None
            while fn is None:
                fn = {
                    '>' : self.model.inc_pointer,
                    '<' : self.model.dec_pointer,
                    '+' : self.model.inc_at_pointer,
                    '-' : self.model.dec_at_pointer,
                    '[' : self.push_stack,
                    ']' : self.pop_stack,
                }.get(self.program[self.program_counter], None)

                self.program_counter += 1

                if fn and self.running:
                    fn()
                    self.view.set_selected_cell(self.model.pointer)
                    gobject.timeout_add(self.view.get_delay(), self.exec_next)

        except IndexError:
            self.stop()

    def push_stack(self):
        self.stack.append(self.program_counter)

    def pop_stack(self):
        val = self.stack.pop()
        if self.model.get_value_at_pointer() != 0:
            self.program_counter = val - 1

    def stop(self):
        self.running = False
        self.view.set_running(False)

