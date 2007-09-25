#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

import os

import bfide

def glade_filename():
    suffix = "main.glade"

    local = os.path.join('glade', suffix)
    if os.path.isfile(local):
        return local

    for path in ['/usr/share/bfide']:
        path = os.path.join(path, suffix)
        if os.path.isfile(path):
            return path

def main():
    xml = gtk.glade.XML(glade_filename())
    view = bfide.View(xml)

    model = bfide.Model()

    controller = bfide.Controller(model, view)
    controller.setup(xml)

    try:
        gtk.main()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
