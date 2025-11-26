from PyQt6 import QtWidgets, QtCore
from datetime import datetime
from Connection import *
from time import sleep
import Globals

class Invoice:

    @staticmethod
    def searchCustomer(widget):
        try:
            if widget.text().upper().strip() == "":
                Invoice._loadAnonymousClient()
                return

            else:
                widget = widget.text().upper().strip()

            customerData = Connection.getCustomerInfo(widget)
            if customerData:
                Globals.ui.lbl_nameFac.setText(customerData[2] + " " + customerData[3])
                Globals.ui.lbl_invoiceType.setText(customerData[9])
                Globals.ui.lbl_addressFac.setText(customerData[6] + " " + customerData[8] + " " + customerData[7])
                Globals.ui.lbl_mobileFac.setText(str(customerData[5]))

                if customerData[10] == "True":
                    Globals.ui.lbl_statusFac.setText("Activo")
                else:
                    Globals.ui.lbl_statusFac.setText("Inactivo")

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("We couldn't find the customer, please make sure you wrote the\n"
                             "DNI correctly or that the customer you're looking for exists.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as e:
            print("error alta factura", e)


    @staticmethod
    def _loadAnonymousClient():
        Globals.ui.lbl_nameFac.setText("Anonimo")
        Globals.ui.lbl_invoiceType.setText("Anonimo")
        Globals.ui.lbl_addressFac.setText("Anonimo")
        Globals.ui.lbl_mobileFac.setText("Anonimo")
        Globals.ui.lbl_statusFac.setText("Anonimo")


    @staticmethod
    def cleanFac():
        try:
            Globals.ui.lbl_numFactura.setText("")
            Globals.ui.txt_dniFactura.setText("")
            Globals.ui.lbl_dateFactura.setText("")
            Globals.ui.lbl_nameFac.setText("")
            Globals.ui.lbl_addressFac.setText("")
            Globals.ui.lbl_statusFac.setText("")
            Globals.ui.lbl_invoiceType.setText("")
            Globals.ui.lbl_mobileFac.setText("")

        except Exception as e:
            print("There was an error while clearing the Invoice fields: ", e)


    @staticmethod
    def saveInvoice():
        try:
            dni = Globals.ui.txt_dniFactura.text()
            date = datetime.now().strftime("%d/%m/%Y")
            print(date)
            if dni != "" and date != "":
                Globals.ui.lbl_dateFactura.setText(date)
                if Connection.addInvoice(dni, date):
                    Globals.ui.lbl_numFactura.setText(str(Connection.getInvoiceId(dni)))
                    Invoice.loadTableFac()
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Invoice")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Invoice created successfully")
                    mbox.exec()
                    sleep(2)
                    mbox.hide()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Warning")
                    mbox.setText("Missing fields or data")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                        mbox.hide()

        except Exception as e:
            print("There was an error while saving the Invoice: ", e)


    @staticmethod
    def loadTableFac():
        try:
            invoices = Connection.getInvoices()

            index = 0
            uiTable = Globals.ui.tbl_invoiceTable

            for invoice in invoices:
                uiTable.setRowCount(index + 1)
                uiTable.setItem(index, 0, QtWidgets.QTableWidgetItem(str(invoice[0])))
                uiTable.setItem(index, 1, QtWidgets.QTableWidgetItem(str(invoice[1])))
                uiTable.setItem(index, 2, QtWidgets.QTableWidgetItem(str(invoice[2])))

                uiTable.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                index += 1

        except Exception as e:
            print("There was an error while loading the Invoice table: ", e)


    @staticmethod
    def showInvoiceInfo():
        try:
            selectedRow = Globals.ui.tbl_invoiceTable.currentRow()
            selectedInvoiceId = Globals.ui.tbl_invoiceTable.item(selectedRow, 0).text()
            invoiceData = Connection.getInvoiceInfo(selectedInvoiceId)
            allDataBoxes = [Globals.ui.lbl_numFactura, Globals.ui.txt_dniFactura, Globals.ui.lbl_dateFactura]

            for i in range(len(allDataBoxes)):

                if hasattr(allDataBoxes[i], "setText"):
                    allDataBoxes[i].setText(str(invoiceData[i]))
                if hasattr(allDataBoxes[i], "setCurrentText"):
                    allDataBoxes[i].setCurrentText(str(invoiceData[i]))

        except Exception as error:
            print("There was an error while showing product info: ", error)