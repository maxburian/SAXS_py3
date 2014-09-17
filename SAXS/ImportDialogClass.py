from PyQt4 import uic
import os

widgetForm, baseClass= uic.loadUiType(os.path.dirname(__file__)+os.sep+"importdialog.ui")


class Importdialog(baseClass, widgetForm):
    def __init__(self, parent = None):
        super(Importdialog, self).__init__(parent)
        self.setupUi(self)