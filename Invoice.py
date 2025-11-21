from PyQt6.QtSql import record

from Connection import *
import Globals

class Invoice:

    @staticmethod
    def saveInvoice(widget):
        try:
            dni = widget.text().upper().strip()
            widget.setText(dni)
            if dni == "" or Connection.getCustomerInfo(dni):
                if dni == "":
                    dni = "00000000T"
                record = Connection.getCustomerInfo(dni)
                print(record)
                Globals.ui.lbl_lbl_nameFac.setText(record[2] + " " + record[3])
                Globals.ui.lbl_invoiceType.setText(record[9])
                Globals.ui.lbl_addressFac.setText(record[6] + " " + record[8] + " " + record[7])
                Globals.ui.lbl_mobileFac.setText(record[5])

                if record[10] == "True":
                    Globals.ui.lbl_statusFac.setText("Activo")
                else:
                    Globals.ui.lbl_statusFac.setText("Inactivo")

            else:
                print("WTF hermano??")

        except Exception as e:
            print("error alta factura", e)