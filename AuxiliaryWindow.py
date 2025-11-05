from datetime import datetime
from dlgCalendar import *
from dlgAbout import *
from Events import *
import Globals

class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        Globals.vencal = Ui_dlgCalendar()
        Globals.vencal.setupUi(self)
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        Globals.vencal.Calendar.setSelectedDate((QtCore.QDate(year, month, day)))
        Globals.vencal.Calendar.clicked.connect(Events.loadData)

class About(QtWidgets.QDialog):
    def __init__(self):
        super(About, self).__init__()
        Globals.about = Ui_dlg_about()
        Globals.about.setupUi(self)
#        Globals.about.btn_CloseAbout.clicked.connect(Events.closeAbout) no me he puesto a hacer el closeAbout :P
        Globals.about.btn_CloseAbout.clicked.connect(lambda: Globals.about.hide())

class FileDialogOpen(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogOpen, self).__init__()
