from dlgCalendar import *
from dlgAbout import *
from Events import *
import datetime
import Globals

class Calendar(QtWidgets.QDialog):
    def __init__(self):
        """

        Ventana de diálogo para selección de fechas.

        Inicializa la interfaz del calendario, establece la fecha actual
        como seleccionada por defecto y conecta el evento de clic del
        calendario para cargar la fecha seleccionada en el sistema.

        :return: None

        """
        super(Calendar, self).__init__()
        Globals.vencal = Ui_dlgCalendar()
        Globals.vencal.setupUi(self)
        day = datetime.datetime.now().day
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year

        Globals.vencal.Calendar.setSelectedDate((QtCore.QDate(year, month, day)))
        Globals.vencal.Calendar.clicked.connect(Events.loadData)

class About(QtWidgets.QDialog):
    def __init__(self):
        """

        Ventana de diálogo de información de la aplicación.

        Inicializa la interfaz de la ventana "About" y conecta el botón
        de cierre para ocultar la ventana cuando el usuario lo pulse.

        :return: None

        """
        super(About, self).__init__()
        Globals.about = Ui_dlg_about()
        Globals.about.setupUi(self)
        Globals.about.btn_CloseAbout.clicked.connect(Events.closeAbout)

class FileDialogOpen(QtWidgets.QFileDialog):
    def __init__(self):
        """

        Diálogo para abrir archivos.

        Inicializa un cuadro de diálogo estándar del sistema para
        seleccionar archivos desde el sistema de archivos del usuario.

        :return: None
        """
        super(FileDialogOpen, self).__init__()
