from PyQt6 import QtWidgets, QtCore
from datetime import datetime
from Connection import *
from time import sleep
from Reports import *
import Connection
import Globals

class Invoice:

    @staticmethod
    def showCustomer(widget):   #buscaCli
        """

        Busca un cliente de la base de datos para cargarlo en el panel de ventas. Si la caja de texto del DNI está vacia, muestra el cliente anónimo
        :param widget:
        :type widget:
        :return:
        :rtype:

        """
        try:
            if widget.text().upper().strip() == "00000000T":
                Invoice.loadAnonymousCustomer()
                return
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
    def loadAnonymousCustomer():   #loadFactFirst
        Globals.ui.txt_dniFactura.setText("00000000T")
        Globals.ui.lbl_nameFac.setText("Anonimo")
        Globals.ui.lbl_invoiceType.setText("Anonimo")
        Globals.ui.lbl_addressFac.setText("Anonimo")
        Globals.ui.lbl_mobileFac.setText("Anonimo")
        Globals.ui.lbl_statusFac.setText("Anonimo")


    @staticmethod
    def cleanFac():
        """

        Limpia todo el panel de facturación

        """
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
        """

        Crea uan factura nueva al cliente cuyo DNI está en la caja de texto y existe y la inserta en la base de datos. Limpia si es necesario la tabla ventas

        """
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
        """

        Cada vez que se carga el programa o se crea una factura, consulta la base de datos y trae todas las facturas

        """
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


    @staticmethod
    def activeSales(row=None):
        """

        Prepara la tabla ventas para añadir ventas, añadiendo una fila para editarla se introducen solo datos de
        código producto y cantidad -.-.-.-.-.-.-.-.-.-.-
        :param row:
        :type row:

        """
        try:
            Globals.ui.tbl_ventas.blockSignals(False)
            Globals.ui.tbl_ventas.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
            # Si no se pasa fila, añadimos la primera fila
            if row is None:
                row = 0
                Globals.ui.tbl_ventas.setRowCount(1)
            else:
                # Si es fila nueva, aumentamos el rowCount
                if row >= Globals.ui.tbl_ventas.rowCount():
                    Globals.ui.tbl_ventas.setRowCount(row + 1)

            # Columna 0 (código)
            Globals.ui.tbl_ventas.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
            Globals.ui.tbl_ventas.item(row, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 2 (price)
            Globals.ui.tbl_ventas.setItem(row, 2, QtWidgets.QTableWidgetItem(""))

            # Columna 3 (cantidad)
            Globals.ui.tbl_ventas.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
            Globals.ui.tbl_ventas.item(row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 4 (total)
            Globals.ui.tbl_ventas.setItem(row, 4, QtWidgets.QTableWidgetItem(""))

        except Exception as error:
            print("error active sales", error)


    @staticmethod
    def cellChangedSales(item):
        """

        Comprueba en primer lugar si estoy en la fila 0, si es así, pone el subtotal a 0. Comprueba si son la columna 0 o 3, las únicas que van a ser editables y van a ejecutar alguna operación.
        Si la columna es 0, consulta si existe el producto, y si no devuelve nada, muestra un mensaje de error, si existe carga el nombre y precio del producto en las columnas 1 y 2.
        Si la columna es 3, añado una cantidad
        :param item:
        :type item:
        :return:
        :rtype:

        """
        try:
            row = item.row()
            col = item.column()
            if row == 0:
                subtotal = 0
            if col not in (0, 3):
                return

            value = item.text().strip()
            if value == "":
                return

            Globals.ui.tbl_ventas.blockSignals(True)

            # Columna 0 entonces buscar producto y rellenar nombre y precio
            if col == 0:
                subtotal = 0.00
                data = Connection.selectProduct(value)
                Globals.ui.tbl_ventas.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[0])))
                Globals.ui.tbl_ventas.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1])))
                Globals.ui.tbl_ventas.item(row, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 3 → calcular total
            elif col == 3:
                cantidad = float(value)
                precio_item = Globals.ui.tbl_ventas.item(row, 2)
                if precio_item:
                    precio = float(precio_item.text())
                    tot = round(precio * cantidad, 2)
                    Globals.ui.tbl_ventas.setItem(row, 4, QtWidgets.QTableWidgetItem(str(tot)))
                    Globals.ui.tbl_ventas.item(row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight
                                                                        | QtCore.Qt.AlignmentFlag.AlignVCenter)

            Globals.ui.tbl_ventas.blockSignals(False)

            # Comprobar si la fila actual está completa y añadir nueva fila
            if all([
                Globals.ui.tbl_ventas.item(row, 0) and Globals.ui.tbl_ventas.item(row, 0).text().strip(),
                Globals.ui.tbl_ventas.item(row, 1) and Globals.ui.tbl_ventas.item(row, 1).text().strip(),
                Globals.ui.tbl_ventas.item(row, 2) and Globals.ui.tbl_ventas.item(row, 2).text().strip(),
                Globals.ui.tbl_ventas.item(row, 3) and Globals.ui.tbl_ventas.item(row, 3).text().strip(),
                Globals.ui.tbl_ventas.item(row, 4) and Globals.ui.tbl_ventas.item(row, 4).text().strip()
            ]):
                next_row = Globals.ui.tbl_ventas.rowCount()
                Invoice.activeSales(row=next_row)
                subtotal = subtotal + tot
                ##iva = round(subtotal * iva, 2)
                ##total = round(subtotal + iva, 2)
                Globals.ui.lbl_subtotal.setText(str(subtotal))
                ##globals.ui.lblIVA.setText(str(iva))
                ##globals.ui.lblTotal.setText(str(total))

        except Exception as error:
            print("Error en cellChangedSales:", error)
            Globals.ui.tbl_ventas.blockSignals(False)


    @staticmethod
    def saveSales():
        try:
            fac = Globals.ui.lbl_numFactura.text()
            if Connection.verifyInvoiceSale(fac):
                Reports.ticket()
            for data in Globals.lineSales:
                aa = "asd"
#                correct = Connection.saveSales(data)

        except Exception as error:
            print("Error in Invoice saveSales:", error)


    @staticmethod
    def loadSalesTable(records):
        try:
            subtotal = 0.00
            index = 0
            for record in records:
                aa = ""

        except Exception as error:
            print("Error in Invoice.loadSalesTable: ", error)