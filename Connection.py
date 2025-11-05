from PyQt6 import QtSql, QtWidgets
import Globals
import os

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
    def getCustomerInfo(phoneNumber):   #dataOneCustomer
        try:
            customerData = []
            query = QtSql.QSqlQuery()
            phoneNumber = str(phoneNumber).strip()
            query.prepare("SELECT  *"
                          "    FROM customers"
                          "    WHERE mobile = :mobile")
            query.bindValue(":mobile", phoneNumber)

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        customerData.append(query.value(i))
            return customerData

        except Exception as error:
            print("An error ocurred while trying to get the customer info: ", error)


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

