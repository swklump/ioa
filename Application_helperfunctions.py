from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

def window_defaults(self,appname,icon_path):
    self.setFixedSize(self.size())
    self.setWindowTitle(appname)
    self.setWindowIcon(QIcon(icon_path))
    self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
    self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
    try:
        self.runapp_but.setAutoDefault(True)
    except AttributeError:
        pass
    else:
        pass