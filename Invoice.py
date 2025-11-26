from PyQt6 import QtWidgets, QtCore
from datetime import datetime
from Connection import *
from time import sleep
import Globals

class Invoice:

    @staticmethod
    def verifyCustomer(widget):
        try:
            dni = widget.text().upper().strip()
            widget.setText(dni)
            if dni == "" or Connection.getCustomerInfo(dni):
                if dni == "":
                    dni = "00000000T"
                record = Connection.getCustomerInfo(dni)
                print(record)
                Globals.ui.lbl_nameFac.setText(record[2] + " " + record[3])
                Globals.ui.lbl_invoiceType.setText(record[9])
                Globals.ui.lbl_addressFac.setText(record[6] + " " + record[8] + " " + record[7])
                Globals.ui.lbl_mobileFac.setText(str(record[5]))

                if record[10] == "True":
                    Globals.ui.lbl_statusFac.setText("Activo")
                else:
                    Globals.ui.lbl_statusFac.setText("Inactivo")

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing fields or data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as e:
            print("error alta factura", e)


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
            data = datetime.now().strftime("%d/%m/%Y")
            if dni != "" and data != "":
                Globals.ui.lbl_dateFactura.setText(data)
                if Connection.insertInvoice(dni, data):
                    Invoice.loadTableFac()
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Invoice")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Invoice created successfully")
                    sleep(2)
                    mbox.hide()
                else:
                    mbox =QtWidgets.QMessageBox()
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