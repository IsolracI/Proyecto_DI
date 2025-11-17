from Connection import *
from Events import *
import Globals

class Products:

    @staticmethod
    def loadProductsTable():
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

                uiTable.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                index += 1

        except Exception as error:
            print("There was an error while loading products table: ", error)

    @staticmethod
    def clearProductFields():
        try:
            allDataBoxes = [Globals.ui.txt_productName, Globals.ui.txt_stockAvailable, Globals.ui.cmb_productFamily, Globals.ui.txt_productPrice]

            for i in range(len(allDataBoxes)):
                allDataBoxes[i].clear()

        except Exception as error:
            print("There was an error while clearing the fields: ", error)


    @staticmethod
    def showProductInfo():
        try:
            selectedRow = Globals.ui.tbl_productList.currentRow()
            selectedProductId = Globals.ui.tbl_productList.item(selectedRow, 0).text()

            productData = Connection.getProductInfo(selectedProductId)

            allDataBoxes = [Globals.ui.lbl_productCodeBox, Globals.ui.txt_productName, Globals.ui.txt_stockAvailable, Globals.ui.cmb_productFamily, Globals.ui.txt_productPrice]

            for i in range(len(allDataBoxes)):

                if hasattr(allDataBoxes[i], "setText"):
                    allDataBoxes[i].setText(str(productData[i]))
                if hasattr(allDataBoxes[i], "setCurrentText"):
                    allDataBoxes[i].setCurrentText(str(productData[i]))

        except Exception as error:
            print("There was an error while showing product info: ", error)







"""
    @staticmethod
    def saveNewProduct():
        try:
            allDataBoxes = [Globals.ui.txt_productName, Globals.ui.txt_stockAvailable, Globals.ui.cmb_productFamily, Globals.ui.txt_productPrice]

            if Connection.addProduct(allDataBoxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The product has been added.")
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

"""