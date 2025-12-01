from PyQt6 import QtSql, QtWidgets
import Globals
import os
import re


class Connection():

    @staticmethod
    def dbConnection():
        dbURL = "./data/bbdd.sqlite"

        if not os.path.isfile(dbURL):
            QtWidgets.QMessageBox.critical(None, "Error", "The database file does not exist.",
                                           QtWidgets.QMessageBox.StandardButton.Cancel)

        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(dbURL)

        if not db.open():
            QtWidgets.QMessageBox.critical(None, "Error", "We could not connect to the database.",
                                           QtWidgets.QMessageBox.StandardButton.Cancel)

        query = QtSql.QSqlQuery()
        query.exec("SELECT  name"
                   "    FROM sqlite_master"
                   "    WHERE type='table';")

        if not query.next():
            QtWidgets.QMessageBox.critical(None, "Error", "The database is empty or invalid",
                                           QtWidgets.QMessageBox.StandardButton.Cancel)

        else:
            QtWidgets.QMessageBox.information(None, "Info", "We successfully connected to the database.",
                                              QtWidgets.QMessageBox.StandardButton.Ok)



    ##--## CUSTOMERS ##--##   ##########################################################################################
    @staticmethod
    def getProvinces():   ###listProv
        provincesList = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT  provincia"
                      "    FROM provincias"
                      "    ORDER BY provincia")

        if query.exec():
            while query.next():
                provincesList.append(query.value("provincia"))

        return provincesList


    @staticmethod
    def getCities(province):   ###listMuniProv
        try:
            citiesList = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT  m.municipio"
                          "    FROM municipios as m INNER JOIN provincias as p on m.idprov=p.idprov"
                          "    WHERE p.provincia = :province")
            query.bindValue(":province", province)

            if query.exec():
                while query.next():
                    citiesList.append(query.value("municipio"))

            return citiesList

        except Exception as error:
            print("An error ocurred while trying to get the cities: ", error)


    @staticmethod
    def getCustomers(historicalOnly = True):   ###listCustomers
        if historicalOnly:
            queryOrder = ("SELECT  *"
                          "    FROM customers"
                          "    WHERE historical = 'True'"
                          "    ORDER BY surname")

        else:
            queryOrder = ("SELECT  *"
                          "    FROM customers"
                          "    ORDER BY surname")

        customersList = []
        query = QtSql.QSqlQuery()
        query.prepare(queryOrder)

        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                customersList.append(row)

        return customersList


    @staticmethod
    def getCustomerInfo(dni):   #dataOneCustomer
        try:
            customerData = []
            query = QtSql.QSqlQuery()
            dni = str(dni).strip().upper()
            query.prepare("SELECT  *"
                          "    FROM customers"
                          "    WHERE dni_nie = :dni")
            query.bindValue(":dni", dni)

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        customerData.append(query.value(i))
            return customerData

        except Exception as error:
            print("An error ocurred while trying to get the customer info: ", error)


    @staticmethod
    def getCustomersDni(mobile):
        try:

            query = QtSql.QSqlQuery()
            mobile = str(mobile).strip()
            customerDni = query.prepare("SELECT  dni_nie"
                                        "    FROM customers"
                                        "    WHERE mobile = :mobile")
            query.bindValue(":mobile", mobile)

            if query.exec():
                while query.next():
                    customerDni = query.value("dni_nie")
            return customerDni

        except Exception as error:
            print("An error ocurred while trying to get the customer DNI: ", error)


    @staticmethod
    def deleteCustomer(dni):   ###deleteCli
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET historical = :value WHERE dni_nie = :dni;")
            query.bindValue(":value", str(False))
            query.bindValue(":dni", dni)

            if not query.exec():
                return False
            return True
        except Exception as error:
            print("An error ocurred while trying to delete the customer: ", error)
        return True


    @staticmethod
    def addCustomer(data):   ###addCli
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers "
                           "(dni_nie, adddata, surname, name, mail, mobile, address, province, city, invoicetype, historical)"
                           "VALUES "
                           "(:dni_nie, :adddata, :surname, :name, :mail, :mobile, :address, :province, :city, :invoicetype, :historical)")

            orderValues = [":dni_nie", ":adddata", ":surname", ":name", ":mail", ":mobile", ":address", ":province", ":city", ":invoicetype"]
            radialButtons = ["electronic", "paper"]

            for i in range(len(orderValues)):
                value = data[i]

                if hasattr(value, "text"):
                    valueText = value.text()
                elif hasattr(value, "currentText"):
                    valueText = value.currentText()
                else:
                    valueText = str(value)

                query.bindValue(orderValues[i], valueText)

            query.bindValue(":historical", str(True))

            if not query.exec():
                print("An error ocurred while trying to add the customer: ", query.lastError().text())
                return False
            return True

        except Exception as error:
            print("An error ocurred while trying to add the customer: ", error)


    @staticmethod
    def modifyCustomerData(data):   ###modifyCli
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers set "
                          "adddata = :adddata, surname = :surname, name = :name, mail = :mail, mobile = :mobile,"
                          "address = :address, province = :province, city = :city, invoicetype = :invoicetype,"
                          "historical = :historical "
                          "WHERE dni_nie = :dni_nie;")

            orderValues = [":dni_nie", ":adddata", ":surname", ":name", ":mail", ":mobile", ":address", ":province", ":city", ":invoicetype"]
            radialButtons = ["electronic", "paper"]

            for i in range(len(orderValues)):
                try:
                    if data[i] in radialButtons:
                        valueText = data[i]
                    else:
                        valueText = str(data[i].text())

                except AttributeError:
                    valueText = str(data[i].currentText())
                query.bindValue(orderValues[i], valueText)

            query.bindValue(":historical", str(data[10]))

            if not query.exec():
                return False
            return True

        except Exception as error:
            print("An error occurred while trying to modify the customer's data : ", error)



    ##--## PRODUCTS ##--##   ###########################################################################################
    @staticmethod
    def _checkPrice(price):
        pattern = r'^\d+(,\d{1,2})?[\s]€?$'

        try:
            if re.match(pattern, price):

                Globals.ui.txt_productPrice.setStyleSheet("background-color: rgb(255, 255, 220); color black")
                if price.strip(" ")[-1] == "€":
                    price.strip(" ")
                    price = price + " €"
                return price

            else:
                Globals.ui.txt_productPrice.setStyleSheet("background-color: #FFC0CB; color black")
                Globals.ui.txt_productPrice.setText(None)
                Globals.ui.txt_productPrice.setPlaceholderText("Invalid price format")

                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Please, use formats like:\n"
                             "0,00\t 99,99\t 12,50\n"
                             "or\n"
                             "0,00 €\t 99,99 €\t 12,50 €\n")
                mbox.exec()
                return False

        except Exception as error:
            print("There was an error while checking price: ", error)


    @staticmethod
    def getProducts():
        queryOrder = ("SELECT  *"
                      "    FROM products")

        productsList = []
        query = QtSql.QSqlQuery()
        query.prepare(queryOrder)

        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                productsList.append(row)

        return productsList


    @staticmethod
    def getProductInfo(code):
        try:
            productData = []
            query = QtSql.QSqlQuery()
            code = str(code).strip().upper()
            query.prepare("SELECT  *"
                          "    FROM products"
                          "    WHERE Code = :code")
            query.bindValue(":code", code)

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        productData.append(query.value(i))
            return productData

        except Exception as error:
            print("An error ocurred while trying to get the product info: ", error)


    @staticmethod
    def addProduct(data):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO products "
                           "(Name, Stock, Family, UnitPrice)"
                           "VALUES "
                           "(:Name, :Stock, :Family, :UnitPrice)")

            data[3] = Connection._checkPrice(data[3].text())

            orderValues = [":Name", ":Stock", ":Family", ":UnitPrice"]

            for i in range(len(orderValues)):
                value = data[i]

                if hasattr(value, "text"):
                    valueText = value.text()
                elif hasattr(value, "currentText"):
                    valueText = value.currentText()
                else:
                    valueText = str(value)

                query.bindValue(orderValues[i], valueText)

            if not query.exec():
                print("An error ocurred in the query while trying to add the product in the database: ", query.lastError().text())
                return False
            return True

        except Exception as error:
            print("An error ocurred while trying to add the product in the database: ", error)


    @staticmethod
    def deleteProduct(productName):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE  FROM products "
                          "    WHERE Name = :productName;")
            query.bindValue(":productName", productName)

            if not query.exec():
                return False
            return True
        except Exception as error:
            print("An error ocurred while trying to delete the product in the database: ", error)
        return True


    @staticmethod
    def modifyProductData(data):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE products set "
                          "Stock = :Stock, Family = :Family, UnitPrice = :UnitPrice "
                          "WHERE Name = :Name;")

            data[3] = Connection._checkPrice(data[3].text())

            orderValues = [":Name", ":Stock", ":Family", ":UnitPrice"]

            for i in range(len(orderValues)):
                value = data[i]

                if hasattr(value, "text"):
                    valueText = value.text()
                elif hasattr(value, "currentText"):
                    valueText = value.currentText()
                else:
                    valueText = str(value)
                query.bindValue(orderValues[i], valueText)

            if not query.exec():
                return False
            return True

        except Exception as error:
            print("An error occurred while trying to modify the product in the database: ", error)



    #-# INVOICE #-#
    @staticmethod
    def getInvoices():  ### allInvoices
        try:
            invoices = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT  *"
                          "    FROM invoices"
                          "    ORDER BY id_fac DESC")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    invoices.append(row)
            return invoices
        except Exception as error:
            print("There was an error trying to get the invoice records: ", error)

    @staticmethod
    def getInvoiceId(dni):
        try:
            query = QtSql.QSqlQuery()
            invoiceInfo = query.prepare("SELECT  id_fac"
                                        "    FROM invoices"
                                        "    WHERE dni_nie = :dni;")
            query.bindValue(":dni", dni)

            if query.exec():
                while query.next():
                    invoiceInfo = query.value("id_fac")
            return invoiceInfo

        except Exception as error:
            print("There was an error trying to get the invoice information: ", error)

    @staticmethod
    def getInvoiceInfo(id):
        try:
            invoiceInfo = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT  *"
                          "    FROM invoices"
                          "    WHERE id_fac = :id;")
            query.bindValue(":id", id)

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        invoiceInfo.append(query.value(i))
            return invoiceInfo

        except Exception as error:
            print("There was an error trying to get the invoice information: ", error)


    @staticmethod
    def addInvoice(dni, data):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO Invoices"
                          "(dni_nie, data)"
                          "VALUES"
                          "(:dni, :data)")
            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(data))
            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("There was an error inserting the invoice", error)


    @staticmethod
    def selectProduct(item):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT  *"
                          "    FROM products"
                          "    WHERE Code = :code")
            query.bindValue(":code", int(item))
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
            return row
        except Exception as error:
            print("There was an error while selecting the product: ", error)


    @staticmethod
    def saveSales(data):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO sales "
                          "(idfac, )")