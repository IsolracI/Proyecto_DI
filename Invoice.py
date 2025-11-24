from datetime import datetime

from PyQt6 import QtWidgets

from Connection import *
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
                print("WTF hermano??")

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
                if Connection.insertInvoice(dni, data):
                    print("invoice successfully saved")
                else:
                    mbox =QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Warning")
                    mbox.setText("Missing fields or data")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()

        except Exception as e:
            print("There was an error while saving the Invoice: ", e)
