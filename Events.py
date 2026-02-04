from PyQt6 import QtWidgets, QtGui
from mailbox import mbox
from Connection import *
from Customers import *
from Invoice import *
import datetime
import Globals
import zipfile
import shutil
import time
import sys
import csv
import os


class Events:

    #-# ToolBar #-#

    @staticmethod
    def saveBackup():
        """

        Crea una copia de seguridad de la base de datos.

        :return: None

        """
        try:
            backupDate = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            fileName = str(backupDate) + "_backup.zip"
            filePath, file = Globals.dlgOpen.getSaveFileName(None, "Save Backup File", fileName, "zip")

            if Globals.dlgOpen.accept and file:
                filezip = zipfile.ZipFile(file, "w")
                filezip.write("./data/bbdd.sqlite", os.path.basename("./data/bbdd.sqlite"), zipfile.ZIP_DEFLATED)
                filezip.close()
                shutil.move(file, filePath)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                #                mbox.setWindowIcon(QtGui.QIcon.("url imagen")) no tengo una imagen
                mbox.setWindowTitle("Save Backup File")
                mbox.setText("Backup File Saved")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

        except Exception as error:
            print("There was an error while saving the backup: ", error)


    @staticmethod
    def restoreBackup():
        """

        Restaura una copia de seguridad de la base de datos.

        :return: None

        """
        try:
            fileName = Globals.dlgOpen.getOpenFileName(None, "Restore Backup File", "", "*.zip;;All Files (*)")
            file = fileName[0]

            if file:
                with zipfile.ZipFile(file, "r") as bbdd:
                    bbdd.extractall(path="./data")
                bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                #                mbox.setWindowIcon(QtGui.QIcon("url imagen"))
                mbox.setWindowTitle("Restore Backup File")
                mbox.setText("Backup File Restored")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                Connection.dbConnection()
                Events.loadProvinces()
                Customers.loadCustomerTable()

        except Exception as error:
            print("There was an error while restoring the backup: ", error)


    @staticmethod
    def exportCsvCustomers():
        """

        Exporta los clientes a un archivo CSV.

        :return: None

        """
        try:
            data = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            fileName = str(data) + "_customers.csv"
            filePath, filter = Globals.dlgOpen.getSaveFileName(None, "Export Backup File", fileName,
                                                               "CSV Files (*.csv)")
            var = False

            if filePath:
                records = Connection.getCustomers(var)
                with open(filePath, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        ["DNIE_NIE", "AddData", "Surname", "Name", "eMail", "Mobile", "Address", "Province", "City",
                         "Invoice Type", "Active"])

                    for record in records:
                        writer.writerow(record)

                #                shutil.move(filter, filePath)

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                #               mbox.setWindowIcon(QtGui.QIcon("URL imagen"))
                mbox.setWindowTitle("Export Customers")
                mbox.setText("Customer data successfully exported")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                #                mbox.setWindowIcon(QtGui.QIcon("URL imagen"))
                mbox.setWindowTitle("Export Customers")
                mbox.setText("Error while exporting customer data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

        except Exception as error:
            print("There was an error while exporting the backup to csv file : ", error)



    #-# AuxiliaryWindows #-#

    @staticmethod
    def exitWindow():   ###messageExit
        """

        Muestra un cuadro de confirmación para cerrar la aplicación.

        Si el usuario confirma la acción, finaliza la ejecución del programa.
        Si cancela, la ventana se mantiene abierta.

        :return: None

        """
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
#            mbox.setWindowIcon(QtGui.QIcon("./assets/icon3.png/"))
            mbox.setWindowTitle("Exit")
            mbox.setText("Are you sure you want to exit?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText("Yes")
            mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText("No")
            mbox.resize(600,800)

            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()

            else:
                mbox.hide()

        except Exception as error:
            print("There was an error with exitMessage: ", error)


    @staticmethod
    def showAbout():
        """

        Muestra la ventana de información de la aplicación.

        :return: None

        """
        try:
            Globals.ui.about.show()

        except Exception as error:
            print("There was an error with showAbout: ", error)


    @staticmethod
    def closeAbout():
        """

        Cierra la ventana de información de la aplicación.

        :return: None

        """
        try:
            Globals.ui.about.hide()

        except Exception as error:
            print("There was an error with closeAbout: ", error)



    #-# Customers #-#

    @staticmethod
    def openCalendar():
        """

        Muestra la ventana del calendario.

        :return: None

        """
        try:
            Globals.vencal.show()

        except Exception as error:
            print("There was an error with openCalendar: ", error)


    @staticmethod
    def loadData(qDate):
        """

        Carga la fecha seleccionada en el calendario.

        :param qDate: Fecha seleccionada en el calendario
        :type qDate: QDate
        :return: None

        """
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))

            if Globals.ui.mainPanel.currentIndex() == 0:
                Globals.ui.txt_fechaAlta.setText(data)

            time.sleep(0.3)
            Globals.vencal.hide()

        except Exception as error:
            print("There was an error with loadData: ", error)


    @staticmethod
    def loadProvinces():   ###loadProv
        """

        Carga la lista de provincias en el comboBox.

        :return: None

        """
        try:
            Globals.ui.cmb_provinciaCliente.clear()
            Globals.ui.cmb_provinciaCliente.addItems(["      — Select a Province —"])
            provinces = Connection.getProvinces()
            # con conexionserver
##          provinces = conexionserver.ConexionServer.listaProv()
            Globals.ui.cmb_provinciaCliente.addItems(provinces)
            Globals.ui.cmb_provinciaCliente.setCurrentIndex(0)

        except Exception as error:
            print("There was an error loading the provinces list: ", error)


    @staticmethod
    def loadCities():   ###loadMuniCli
        """

        Carga la lista de ciudades según la provincia seleccionada.

        :return: None

        """
        try:
            Globals.ui.cmb_ciudadCliente.clear()
            province = Globals.ui.cmb_provinciaCliente.currentText()

            if not province or province[0] == "—":
                return

            cities = Connection.getCities(province)
            # con conexionserver
#           cities = conexion.ConexionServer.listMuniProv(province)
            Globals.ui.cmb_ciudadCliente.addItems(cities)

        except Exception as error:
            print("There was an error loading the cities list: ", error)


    @staticmethod
    def resizeCustomerTable():   ###resizeTabCustomer
        """

        Ajusta automáticamente el tamaño de las columnas de la tabla de clientes.

        :return: None

        """
        try:
            header = Globals.ui.tbl_customerList.horizontalHeader()

            for i in range(header.count()):

                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                headerItems = Globals.ui.tbl_customerList.horizontalHeaderItem(i)
                # Cabezera en Negrilla
                font = headerItems.font()
                font.setBold(True)
                header.setFont(font)

        except Exception as error:
            print("There was an error in resizeCustomerTable: ", error)


    @staticmethod
    def loadStatusBar():
        """

        Carga la barra de estado de la aplicación.

        :return: None

        """
        try:
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            labelStatus = QtWidgets.QLabel()
            labelStatus.setText("Date: " + data + " - Version 0.0.1")
            labelStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            labelStatus.setStyleSheet("color: white; font-weight: bold; font-size: 10px;")
            Globals.ui.statusbar.addPermanentWidget(labelStatus, 1)

        except Exception as error:
            print("There was an error while loading the status bar: ", error)


    @staticmethod
    def resizeProductTable():
        """

        Ajusta automáticamente el tamaño de las columnas de la tabla de productos.

        :return: None

        """
        try:
            header = Globals.ui.tbl_productList.horizontalHeader()

            for i in range(header.count()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                headerItems = Globals.ui.tbl_customerList.horizontalHeaderItem(i)
                # Cabezera en Negrilla
                font = headerItems.font()
                font.setBold(True)
                header.setFont(font)

        except Exception as error:
            print("There was an error in resizeCustomerTable: ", error)


    @staticmethod
    def resizeSalesTable():
        """

        Ajusta automáticamente el tamaño de las columnas de la tabla de ventas.

        :return: None

        """
        try:
            header = Globals.ui.tbl_ventas.horizontalHeader()
            for i in range(header.count()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                headerItems = Globals.ui.tbl_customerList.horizontalHeaderItem(i)
                # Cabezera en Negrilla
                font = headerItems.font()
                font.setBold(True)
                header.setFont(font)

        except Exception as error:
            print("There was an error in resizeSalesTable: ", error)


    @staticmethod
    def resizeInvoiceTable():
        """

        Ajusta automáticamente el tamaño de las columnas de la tabla de facturas.

        :return: None

        """
        try:
            header = Globals.ui.tbl_invoiceTable.horizontalHeader()
            lastColumn = Globals.ui.tbl_invoiceTable.columnCount() -1

            for i in range(header.count()):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                headerItems = Globals.ui.tbl_customerList.horizontalHeaderItem(i)
                # Cabezera en Negrilla
                font = headerItems.font()
                font.setBold(True)
                header.setFont(font)

            header.setSectionResizeMode(lastColumn, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        except Exception as error:
            print("There was an error in resizeInvoiceTable: ", error)

    @staticmethod
    def onInvoiceClick(row, column):
        if column == 3:
            Invoice.deleteSelectedInvoice(row)