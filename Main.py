from window import Ui_MainWindow
from AuxiliaryWindow import *
from PyQt6 import QtWidgets
from Connection import *
from Customers import *
from Products import *
from Invoice import *
from Reports import *
from Events import *
import Globals
import Styles
import sys

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        Globals.ui = Ui_MainWindow()
        Globals.ui.setupUi(self)


               ###################
        ####   ##-## GENERAL ##-##   ####
               ###################

        # instances
        Globals.vencal = Calendar()
        Globals.ui.about = About()
        Globals.dlgOpen = FileDialogOpen()

        # statusBar Functions
        Events.loadStatusBar()

        # DB Connection:
        Connection.dbConnection()

        # load StyleSheet
        self.setStyleSheet(Styles.load_stylesheet())

        # menu bar Functions:
        Globals.ui.menuAbout.triggered.connect(Events.showAbout)
        Globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        Globals.ui.actionRestore_Backup.triggered.connect(Events.restoreBackup)
        Globals.ui.actionCustomers.triggered.connect(Events.exportCsvCustomers)
        Globals.ui.actionCustomer_Reports.triggered.connect(Reports.customersReports)
        Globals.ui.actionExit.triggered.connect(Events.exitWindow)


               #####################
        ####   ##-## CUSTOMERS ##-##   ####
               #####################

        # Customers DB connection
        historicalOnly = True
        Customers.loadCustomerTable(historicalOnly)
        Events.resizeCustomerTable()

        # Customers lineEdit Functions:
        Globals.ui.txt_DNICliente.editingFinished.connect(Customers.checkDni)
        Globals.ui.txt_emailCliente.editingFinished.connect(lambda: Customers.checkMail(Globals.ui.txt_emailCliente.text()))
        Globals.ui.txt_nombresCliente.editingFinished.connect(lambda: Customers.capitalizeCustomerName(Globals.ui.txt_nombresCliente.text(), Globals.ui.txt_nombresCliente))
        Globals.ui.txt_apellidosCliente.editingFinished.connect(lambda: Customers.capitalizeCustomerName(Globals.ui.txt_apellidosCliente.text(), Globals.ui.txt_apellidosCliente))
        Globals.ui.txt_numeroTelefono.editingFinished.connect(lambda: Customers.checkMobile(Globals.ui.txt_numeroTelefono.text()))

        # Customers comboBox Funtions:
        Events.loadProvinces()
#        Events.loadCities()   # actualmente tengo para que las ciudades se carguen DESPUÉS de que elijas la provincia
        Globals.ui.cmb_provinciaCliente.currentIndexChanged.connect(Events.loadCities)

        # Customers button Functions:
        Globals.ui.btn_fechaAltaCliente.clicked.connect(Events.openCalendar)
        Globals.ui.btn_delete.clicked.connect(Customers.deleteSelectedCustomer)
        Globals.ui.btn_save.clicked.connect(Customers.saveNewCustomer)
        Globals.ui.btn_modif.clicked.connect(Customers.modifyCustomer)
        Globals.ui.btn_search.clicked.connect(Customers.searchCustomer)
        Globals.ui.btn_clearCli.clicked.connect(Customers.clearCustomerFields)

        # Customers table Functions
        Globals.ui.tbl_customerList.clicked.connect(Customers.showCustomerInfo)
        Globals.ui.tbl_customerList_3.clicked.connect(Customers.showCustomerInfo)

        # Customers check Historical
        Globals.ui.chk_historico.setChecked(True)
        Globals.ui.chk_historico.stateChanged.connect(Customers.customersHistorical)


                ####################
        ####    ##-## Products ##-##   ####
                ####################

        # Products table functions
        productFamilies = ["   - select -", "Foods", "Furnitures", "Clothes", "Electronics"]
        Globals.ui.cmb_productFamily.addItems(productFamilies)
        Globals.ui.tbl_productList.clicked.connect(Products.showProductInfo)
        Products.loadProductsTable()
        Events.resizeProductTable()

        # Product button Functions
        Globals.ui.btn_clearProductFields.clicked.connect(Products.clearProductFields)
        Globals.ui.btn_saveProduct.clicked.connect(Products.saveNewProduct)
        Globals.ui.btn_deleteProduct.clicked.connect(Products.deleteSelectedProduct)
        Globals.ui.btn_modifyProduct.clicked.connect(Products.modifyProduct)

        # Products lineEdit Functions
        Globals.ui.txt_productName.editingFinished.connect(lambda: Products.capitalizeProductName(Globals.ui.txt_productName.text(), Globals.ui.txt_productName))


               ###################
        ####   ##-## Invoice ##-##   ####
               ###################

        # General
        Invoice.loadAnonymousCustomer()
        Globals.ui.txt_dniFactura.editingFinished.connect(lambda: Invoice.showCustomer(Globals.ui.txt_dniFactura))
        Events.resizeInvoiceTable()
        Events.resizeSalesTable()
#       background-color: rgb(246, 255, 187); color de fondo de los labels y text en invoice

        # Invoice button Functions
        Globals.ui.btn_saveFactura.clicked.connect(Invoice.saveInvoice)
        Globals.ui.btn_facturaFields.clicked.connect(Invoice.cleanFac)
        Globals.ui.btn_guardarVenta.clicked.connect(Invoice.saveSales)

        # Invoice invoices table Functions
        Invoice.loadTableFac()
        Globals.ui.tbl_invoiceTable.clicked.connect(Invoice.showInvoiceInfo)
        Globals.ui.tbl_invoiceTable.cellClicked.connect(Events.onInvoiceClick)
        Invoice.activeSales()

        # Invoice sales table Functions
        Globals.ui.tbl_ventas.itemChanged.connect(Invoice.cellChangedSales)

        # guardar venta en bd
#       self.scCleanFac = QtGui.QShortcut(QtGui.QKeySequence("F11"), self) para guardar la venta en la tabla ventas usando una tecla en lugar de un boton
#        self.scCleanFac.activated.connect(Invoice.saveSales)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())