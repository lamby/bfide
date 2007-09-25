
class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def setup(self, xml):
        xml.signal_autoconnect(self)
        self.view.setup(self.model)

    def on_toolbutton_run_clicked(self, *_):
        self.model.reset()
        self.view.set_running(True)

        print self.view.get_editor_text()


    def on_toolbutton_stop_clicked(self, *_):
        self.view.set_running(False)
