from PyQt6 import QtWidgets, QtCore
from datetime import datetime
from Connection import *
from time import sleep
from Reports import *
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
            print("(Invoice.showCustomer) There was an error while trying to show the customer: ", e)


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
            print("(Invoice.cleanFac) There was an error while clearing the Invoice fields: ", e)


    @staticmethod
    def saveInvoice():
        """

        Crea uan factura nueva al cliente cuyo DNI está en la caja de texto y existe y la inserta en la base de datos. Limpia si es necesario la tabla ventas

        """
        try:
            dni = Globals.ui.txt_dniFactura.text()
            date = datetime.now().strftime("%d/%m/%Y")
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
            print("(Invoice.saveInvoice) There was an error while saving the Invoice: ", e)


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
            print("(Invoice.loadTableFac) There was an error while loading the Invoice table: ", e)


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

            Invoice.loadSalesTable(selectedInvoiceId)

        except Exception as error:
            print("(Invoice.showInvoiceInfo) There was an error while showing product info: ", error)


    @staticmethod
    def activeSales(createNewRow=False):
        """

        Prepara la tabla ventas para añadir ventas, añadiendo una fila para editarla se introducen solo datos de
        código producto y cantidad -.-.-.-.-.-.-.-.-.-.-
        :param createNewRow:
        :type createNewRow:

        """
        try:
            currentCount = Globals.ui.tbl_ventas.rowCount()
            # Si no se pasa fila, añadimos la primera fila
            if createNewRow:
                Globals.ui.tbl_ventas.setRowCount(currentCount + 1)
                targetRow = currentCount
            else:
                if currentCount == 0:
                    Globals.ui.tbl_ventas.setRowCount(1)
                    targetRow = 0
                else:
                    targetRow = currentCount - 1


            # Columna 1 (código)
            Globals.ui.tbl_ventas.setItem(targetRow, 0, QtWidgets.QTableWidgetItem(""))
            Globals.ui.tbl_ventas.item(targetRow, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 2 (no me acuerdo :p)
            Globals.ui.tbl_ventas.setItem(targetRow, 1, QtWidgets.QTableWidgetItem(""))

            # Columna 3 (price)
            Globals.ui.tbl_ventas.setItem(targetRow, 2, QtWidgets.QTableWidgetItem(""))

            # Columna 4 (cantidad)
            Globals.ui.tbl_ventas.setItem(targetRow, 3, QtWidgets.QTableWidgetItem(""))
            Globals.ui.tbl_ventas.item(targetRow, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 5 (total)
            Globals.ui.tbl_ventas.setItem(targetRow, 4, QtWidgets.QTableWidgetItem(""))
            Globals.ui.tbl_ventas.item(targetRow, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

            Globals.ui.tbl_ventas.blockSignals(False)

        except Exception as error:
            print("(Invoice.activeSales) there was an error trying to activate the sales table: ", error)


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
            salesTable = Globals.ui.tbl_ventas
            currentRow = item.row()
            currentCol = item.column()

            if currentCol not in (0, 3):
                pass

            textValue = item.text().strip()
            if not textValue:
                return

            salesTable.blockSignals(True)
            try:
                if currentRow == 0:
                    try:
                        productRowData = Connection.getProductInfo(textValue)
                        if not productRowData:
                            return

                        productMap = Invoice.mapProductData(productRowData)

                        salesTable.setItem(currentRow, 1, QtWidgets.QTableWidgetItem(str(productMap.get("name"))))
                        salesTable.setItem(currentRow, 2, QtWidgets.QTableWidgetItem(str(productMap.get("price"))))
                        salesTable.item(currentRow, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                    except Exception as error:
                        print("(Invoice.cellChangedSales) There was an error while getting product info: ", error)

                elif currentCol == 3:
                    try:
                        priceItem = salesTable.item(currentRow, 2)
                        if priceItem:
                            quantity = float(textValue)
                            priceText = priceItem.text().replace("€", "").replace(",", ".").strip()
                            price = float(priceText)
                            lineTotal = round(quantity * price, 2)

                            salesTable.setItem(currentRow, 4, QtWidgets.QTableWidgetItem(str(lineTotal)))
                            salesTable.item(currentRow, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

                    except Exception as error:
                        print("(Invoice.cellChangedSales) There was an error trying to calculate total price: ", error)

            finally:
                salesTable.blockSignals(False)

            rowComplete = all([
                salesTable.item(currentRow, 0) and salesTable.item(currentRow, 0).text().strip(),
                salesTable.item(currentRow, 1) and salesTable.item(currentRow, 1).text().strip(),
                salesTable.item(currentRow, 2) and salesTable.item(currentRow, 2).text().strip(),
                salesTable.item(currentRow, 3) and salesTable.item(currentRow, 3).text().strip(),
                salesTable.item(currentRow, 4) and salesTable.item(currentRow, 4).text().strip()
            ])

            if rowComplete:
                try:
                    Invoice.calculateTotals()
                    Invoice.activeSales(True)
                except Exception as error:
                    print("(Invoice.cellChangedSales) There was an error while trying to add a new row or calculate total price: ", error)

        except Exception as error:
            print("(Invoice.cellChangedSales) There was an error: ", error)


    @staticmethod
    def calculateTotals():
        try:
            table = Globals.ui.tbl_ventas
            subtotal = 0.0
            iva = 0.21

            for r in range(table.rowCount()):
                totalItem = table.item(r, 4)
                if totalItem and totalItem.text().strip():
                    try:
                        subtotal += float(totalItem.text())
                    except:
                        pass

            totalIva = float(iva) * float(subtotal)
            totalToPay = float(subtotal) + float(totalIva)

            Globals.ui.lbl_subtotal.setText(str(subtotal))
            Globals.ui.lbl_IVA.setText(str(totalIva))
            Globals.ui.lbl_total.setText(str(totalToPay))

        except Exception as error:
            print("(Invoice.calculateTotals) There was an error while trying to calculate total price: ", error)


    @staticmethod
    def mapProductData(data):
        try:
            return {
                "id": data[0],
                "name": data[1],
                "quantity": data[2],
                "type": data[3],
                "price": data[4]
            }
        except Exception as error:
            print("(Invoice.productRawDataToMap) There was an error while trying to insert the data into a map: ", error)


    @staticmethod
    def saveSales():
        try:
            salesTable = Globals.ui.tbl_ventas
            invoiceId = Globals.ui.lbl_numFactura.text().strip()

            for r in range(salesTable.rowCount()):
                productId = salesTable.item(r, 0).text().strip()
                productName = salesTable.item(r, 1).text().strip()
                unitPrice = salesTable.item(r, 2).text().strip()
                quantity = salesTable.item(r, 3).text().strip()
                totalPrice = salesTable.item(r, 4).text().strip()

                if not invoiceId or not productId or not productName or not unitPrice or not quantity or not totalPrice:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Error")
                    mbox.setText("Please fill all the fields")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return

                allDataBoxes = [invoiceId, productId, quantity, productName, unitPrice, totalPrice]

                if not Connection.addSale(allDataBoxes):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Error")
                    mbox.setText("Error saving the sales")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return

                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Success")
                mbox.setText("Successfully saved the sales")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

        except Exception as error:
            print("(Invoice.saveSales) There was an error while trying to save the sales: ", error)


    @staticmethod
    def loadSalesTable(invoiceId):
        try:
            salesTable = Globals.ui.tbl_ventas
            salesTable.blockSignals(True)

            salesTable.clearContents()
            salesTable.setRowCount(0)

            allSales = Connection.getSales(invoiceId)

            if not allSales:
                Invoice.activeSales(False)
                Invoice.calculateTotals()
                salesTable.blockSignals(False)
                return

            salesTable.setRowCount(len(allSales))
            for index, sale in enumerate(allSales):
#                Product ID
                salesTable.setItem(index, 0, QtWidgets.QTableWidgetItem(str(sale[2])))
#                Product name
                salesTable.setItem(index, 1, QtWidgets.QTableWidgetItem(str(sale[3])))
#                Unit price
                salesTable.setItem(index, 2, QtWidgets.QTableWidgetItem(str(sale[4])))
#                Cuantity
                salesTable.setItem(index, 3, QtWidgets.QTableWidgetItem(str(sale[5])))
#                Total price
                salesTable.setItem(index, 4, QtWidgets.QTableWidgetItem(str(sale[6])))

                itemAlignCenter = QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
                itemAlignLeft = QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter

                if salesTable.item(index, 0):
                    salesTable.item(index, 0).setTextAlignment(itemAlignCenter)
                if salesTable.item(index, 1):
                    salesTable.item(index, 1).setTextAlignment(itemAlignLeft)
                if salesTable.item(index, 2):
                    salesTable.item(index, 2).setTextAlignment(itemAlignCenter)
                if salesTable.item(index, 3):
                    salesTable.item(index, 3).setTextAlignment(itemAlignCenter)
                if salesTable.item(index, 4):
                    salesTable.item(index, 4).setTextAlignment(itemAlignCenter)

            Invoice.calculateTotals()
            salesTable.blockSignals(False)

        except Exception as error:
            print("(Invoice.loadSalesTable) There was an error while trying to load the sales table: ", error)