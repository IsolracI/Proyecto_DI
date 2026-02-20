from Connection import *
from Events import *
import Globals

class Products:

    @staticmethod
    def loadProductsTable():
        """

        Carga la lista de productos en la tabla de la interfaz.

        :return: None

        """
        try:
            products = Connection.getProducts()

            index = 0
            uiTable = Globals.ui.tbl_productList

            for product in products:
                uiTable.setRowCount(index + 1)
                uiTable.setItem(index, 0, QtWidgets.QTableWidgetItem(str(product[0])))
                uiTable.setItem(index, 1, QtWidgets.QTableWidgetItem(str(product[1])))
                uiTable.setItem(index, 2, QtWidgets.QTableWidgetItem(str(product[2])))
                uiTable.setItem(index, 3, QtWidgets.QTableWidgetItem(str(product[3])))
                uiTable.setItem(index, 4, QtWidgets.QTableWidgetItem(str(product[4])))
                uiTable.setItem(index, 5, QtWidgets.QTableWidgetItem(str(product[5])))

                uiTable.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                index += 1

        except Exception as error:
            print("There was an error while loading products table: ", error)


    @staticmethod
    def capitalizeProductName(text, widget):   ###capitalizar
        """

        Capitaliza el nombre del producto.

        :param text: Texto a capitalizar.
        :type text: str
        :param widget: Campo de texto donde se mostrará el texto formateado.
        :type widget: QLineEdit
        :return: None

        """
        try:
            text = text.title()
            widget.setText(text)

        except Exception as error:
            print("There was an error while capitalizing: ", error)


    @staticmethod
    def clearProductFields():
        """

        Limpia los campos del formulario de productos.

        :return: None

        """
        try:
            allDataBoxes = [Globals.ui.txt_productName, Globals.ui.txt_stockAvailable, Globals.ui.txt_productPrice]

            for i in range(len(allDataBoxes)):
                allDataBoxes[i].clear()

            Globals.ui.cmb_productFamily.setCurrentIndex(0)


        except Exception as error:
            print("There was an error while clearing the fields: ", error)


    @staticmethod
    def showProductInfo():
        """

        Muestra la información del producto seleccionado.

        :return: None

        """
        try:
            selectedRow = Globals.ui.tbl_productList.currentRow()
            selectedProductId = Globals.ui.tbl_productList.item(selectedRow, 0).text()

            productData = Connection.getProductInfo(selectedProductId)

            allDataBoxes = [Globals.ui.lbl_productCodeBox, Globals.ui.txt_productName, Globals.ui.txt_stockAvailable, Globals.ui.cmb_productFamily, Globals.ui.txt_productPrice, Globals.ui.txt_discount]

            for i in range(len(allDataBoxes)):

                if hasattr(allDataBoxes[i], "setText"):
                    allDataBoxes[i].setText(str(productData[i]))
                if hasattr(allDataBoxes[i], "setCurrentText"):
                    allDataBoxes[i].setCurrentText(str(productData[i]))

        except Exception as error:
            print("There was an error while showing product info: ", error)


    @staticmethod
    def saveNewProduct():
        """

        Guarda un nuevo producto en la base de datos.

        :return: None

        """
        try:
            allDataBoxes = [Globals.ui.txt_productName, Globals.ui.txt_stockAvailable, Globals.ui.cmb_productFamily, Globals.ui.txt_productPrice]

            if Connection.addProduct(allDataBoxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The product has been added successfully.")
                mbox.exec()
                Products.loadProductsTable()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("An error has occurred while adding the product.")
                mbox.exec()


        except Exception as error:
            print("There was an error while adding the product: ", error)


    @staticmethod
    def deleteSelectedProduct():
        """

        Elimina el producto seleccionado de la base de datos.

        :return: None

        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Product?")
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            productName = Globals.ui.txt_productName.text()

            if Connection.deleteProduct(productName):
                successMbox = QtWidgets.QMessageBox()
                successMbox.setWindowTitle("Information")
                successMbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                successMbox.setText("The product has been deleted.")
                successMbox.exec()
                Products.loadProductsTable()

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while deleting the product.")

        except Exception as error:
            print("There was an error while deleting the product: ", error)


    @staticmethod
    def modifyProduct():   ###modifyCli
        """

        Modifica los datos de un producto existente.

        :return: None

        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Do you want to modify the product's data?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.No:
                mbox.hide()
                return

            allDataBoxes = [Globals.ui.txt_productName, Globals.ui.txt_stockAvailable, Globals.ui.cmb_productFamily, Globals.ui.txt_productPrice]

            if Connection.modifyProductData(allDataBoxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The product has been modified.")
                mbox.exec()
                Products.loadProductsTable()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("An error has occurred while trying to modify the product's data.")
                mbox.exec()

        except Exception as error:
            print("There was an error while modifying the products's data: ", error)