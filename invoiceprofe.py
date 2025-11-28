
import conexion
import globals
from PyQt6 import QtWidgets, QtCore
from datetime import datetime
from time import sleep

class Invoice():
    @staticmethod
    def buscaCli(self = None):
        try:
            dni = globals.ui.txtDnifac.text().upper().strip()
            if globals.ui.txtDnifac.text() == "":
                dni = "00000000T"
            globals.ui.txtDnifac.setText(dni)
            record = conexion.Conexion.dataOneCustomer(dni)
            if len(record) != 0:
                globals.ui.lblNamefac.setText(record[2] + '   ' + record[3])
                globals.ui.lblTipofac.setText(record[9])
                globals.ui.lblDirfac.setText(record[6] + '   ' + record[8] + '   ' + record[7])
                globals.ui.lblMobilefac.setText(record[5])
                if record[10] == "True":
                    globals.ui.lblStatusfac.setText('Activo')
                else:
                    globals.ui.lblStatusfac.setText('Inactivo')
            else:
                globals.ui.txtDnifac.setText("")
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Customers do not Exist")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
        except Exception as error:
            print("error alta factura", error)

    @staticmethod
    def cleanFac(self = None):
        try:
            globals.ui.lblNumfac.setText("")
            globals.ui.txtDnifac.setText("")
            globals.ui.lblFechafac.setText("")
            globals.ui.lblNamefac.setText("")
            globals.ui.lblTipofac.setText("")
            globals.ui.lblDirfac.setText("")
            globals.ui.lblMobilefac.setText("")
            globals.ui.lblStatusfac.setText("")
        except Exception as error:
            print("error limpiar factura", error)

    @staticmethod
    def saveInvoice(self=None):
        try:
            dni = globals.ui.txtDnifac.text()
            data = datetime.now().strftime("%d/%m/%Y")
            if dni != "" and data != "":
                if conexion.Conexion.insertInvoice(dni, data):
                    Invoice.loadTablefac()
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Invoice")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Invoice created successfully")
                    if mbox.exec():
                        mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing Fields or Data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
        except Exception as error:
            print("error save invoice", error)

    @staticmethod
    def loadTablefac(self=None):
        try:
            records = conexion.Conexion.allInvoices()
            index = 0
            for record in records:
                globals.ui.tableFac.setRowCount(index + 1)
                globals.ui.tableFac.setItem(index, 0, QtWidgets.QTableWidgetItem(record[0]))
                globals.ui.tableFac.setItem(index, 1, QtWidgets.QTableWidgetItem(record[1]))
                globals.ui.tableFac.setItem(index, 2, QtWidgets.QTableWidgetItem(record[2]))
                globals.ui.tableFac.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tableFac.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tableFac.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index = index + 1
            ## el último record debe cargarse sus datos en los label
            datos = records[0]
            globals.ui.lblNumfac.setText(str(datos[0]))
            globals.ui.txtDnifac.setText(str(datos[1]))
            globals.ui.lblFechafac.setText(str(datos[2]))
        except Exception as error:
            print("error load tablafac", error)

    def loadFactFirst(self=None):
        try:
            globals.ui.txtDnifac.setText("00000000T")
            globals.ui.lblNumfac.setText("")
            globals.ui.lblFechafac.setText("")
            Invoice.buscaCli(self=None)
        except Exception as error:
            print("error load fac first", error)

    def selectInvoice(self=None):
        try:
            row = globals.ui.tableFac.selectedItems()
            data = [dato.text() for dato in row]
            globals.ui.lblNumfac.setText(str(data[0]))
            globals.ui.txtDnifac.setText(str(data[1]))
            globals.ui.lblFechafac.setText(str(data[2]))
            globals.ui.tableFac.setStyleSheet("""
                        /* Fila seleccionada */
                        QTableWidget::item:selected {
                            background-color: rgb(255, 255, 202);  /* Color pálido amarillo */
                            color: black;                          /* Color del texto al seleccionar */
                        }
                        """)
            Invoice.buscaCli(self=None)
            Invoice.activeSales(self)
        except Exception as error:
            print("error select invoice", error)

    @staticmethod
    def activeSales(self, row=None):
        try:
            # Si no se pasa fila, añadimos la primera fila
            if row is None:
                row = 0
                globals.ui.tableSales.setRowCount(1)
            else:
                # Si es fila nueva, aumentamos el rowCount
                if row >= globals.ui.tableSales.rowCount():
                    globals.ui.tableSales.setRowCount(row + 1)
            globals.ui.tableSales.setStyleSheet("""
                                   /* Fila seleccionada */
                                   QTableWidget::item:selected {
                                       background-color: rgb(255, 255, 202);  /* Color pálido amarillo */
                                       color: black;                          /* Color del texto al seleccionar */
                                   }
                                   """)

            # Columna 0 (código)
            globals.ui.tableSales.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
            globals.ui.tableSales.item(row, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 2 (price)
            globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))

            # Columna 3 (cantidad)
            globals.ui.tableSales.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
            globals.ui.tableSales.item(row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 4 (total)
            globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(""))

        except Exception as error:
            print("error active sales", error)

    @staticmethod
    def cellChangedSales(item):
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

            globals.ui.tableSales.blockSignals(True)

            # Columna 0 entonces buscar producto y rellenar nombre y precio
            if col == 0:
                subtotal = 0.00
                data = conexion.Conexion.selectProduct(value)
                globals.ui.tableSales.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[0])))
                globals.ui.tableSales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1])))
                globals.ui.tableSales.item(row, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 3 → calcular total
            elif col == 3:
                cantidad = float(value)
                precio_item = globals.ui.tableSales.item(row, 2)
                if precio_item:
                    precio = float(precio_item.text())
                    tot = round(precio * cantidad, 2)
                    globals.ui.tableSales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(tot)))
                    globals.ui.tableSales.item(row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight
                                                                        | QtCore.Qt.AlignmentFlag.AlignVCenter)

            globals.ui.tableSales.blockSignals(False)

            # Comprobar si la fila actual está completa y añadir nueva fila
            if all([
                globals.ui.tableSales.item(row, 0) and globals.ui.tableSales.item(row, 0).text().strip(),
                globals.ui.tableSales.item(row, 1) and globals.ui.tableSales.item(row, 1).text().strip(),
                globals.ui.tableSales.item(row, 2) and globals.ui.tableSales.item(row, 2).text().strip(),
                globals.ui.tableSales.item(row, 3) and globals.ui.tableSales.item(row, 3).text().strip(),
                globals.ui.tableSales.item(row, 4) and globals.ui.tableSales.item(row, 4).text().strip()
            ]):
                next_row = globals.ui.tableSales.rowCount()
                Invoice.activeSales(self, row=next_row)
                subtotal = subtotal + tot
                ##iva = round(subtotal * iva, 2)
                ##total = round(subtotal + iva, 2)
                globals.ui.lblSubtotal.setText(str(subtotal))
                ##globals.ui.lblIVA.setText(str(iva))
                ##globals.ui.lblTotal.setText(str(total))



        except Exception as error:
            print("Error en cellChangedSales:", error)
            globals.ui.tableSales.blockSignals(False)
