import gtk
import gobject
import pango

class View(object):
    def __init__(self, xml):
        self.xml = xml

    def __getitem__(self, key):
        widget = self.xml.get_widget(key)
        if widget is None:
            raise KeyError, "Widget not found: %s" % key
        return widget

    def __contains__(self, key):
        try:
            _ = self[key]
        except KeyError:
            return False
        return True

    def setup(self, model_memory):
        self.setup_columns()
        self['treeview_memory'].set_model(model_memory)
        self['textview_editor'].modify_font(pango.FontDescription('monospace'))
        self['hscale_speed'].connect('format-value', lambda scale, value: "%d ms" % value)

    def setup_columns(self):
        def my_render(column, cell_renderer, tree_model, iter, format_func):
            address = tree_model.get_value(iter, 0)
            value = tree_model.get_value(iter, 1)
            out = format_func([address, value])
            cell_renderer.set_property('text', out)

        columns = (
            ('Address', lambda x: "%03d (0x%02x)" % (x[0], x[0])),
            ('Value', lambda x: "%03d (0x%02x) %s" \
                # Prints a sane ASCII representation
                % (x[1], x[1], (x[1] >= 33 and x[1] <= 126) and chr(x[1]) or ""))
        )

        for label, format_func in columns:
            cell_renderer = gtk.CellRendererText()
            column = gtk.TreeViewColumn(label, cell_renderer)
            column.set_cell_data_func(cell_renderer, my_render, format_func)
            self['treeview_memory'].append_column(column)

    def get_editor_text(self):
        buf = self['textview_editor'].get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter())

    def get_delay(self):
        return int(self['hscale_speed'].get_value())

    def set_running(self, is_running):
        self['textview_editor'].set_sensitive(not is_running)

        self['toolbutton_new'].set_sensitive(not is_running)
        self['toolbutton_open'].set_sensitive(not is_running)
        self['toolbutton_save'].set_sensitive(not is_running)
        self['toolbutton_run'].set_sensitive(not is_running)
        self['toolbutton_stop'].set_sensitive(is_running)

    def set_selected_cell(self, num):
        self['treeview_memory'].get_selection().select_path(num)

    def set_selected_opcode(self, num):
        buf = self['textview_editor'].get_buffer()
        iter = buf.get_iter_at_offset(num)
        iter2 = buf.get_iter_at_offset(num)
        iter2.forward_char()
        buf.select_range(iter, iter2)
