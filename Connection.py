from PyQt6 import QtSql, QtWidgets
import Globals
import os
import re


class Connection:

    @staticmethod
    def dbConnection():
        """

        Establece la conexión con la base de datos SQLite y devuelve un booleano
        indicando si la conexión tuvo exito o no

        :return: True si la conexión es válida, False en caso contrario
        :rtype: bool

        """
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


         #######################
    #### ##--## CUSTOMERS ##--## ####   ##########################################################################################
         #######################

    @staticmethod
    def getProvinces():   ###listProv
        """

        Al cargar la aplicación, se busca en la bbdd la lista de provincias y
        se cargan en el comboBox de selección de provincias.

        :return: Una lista de provincias
        :rtype: list[str]

        """
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
        """

        Cuando se selecciona la provincia, se cargan los municipios asociados a esa provincia.

        :param province: Nombre de la provincia
        :type province: str
        :return: Lista de municipios de la provincia
        :rtype: list[str]

        """
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
    def getCustomers(activeOnly = True):   ###listCustomers
        """

        Obtiene el listado de clientes. Permite filtrar para obtener solamente los que
        están activos.

        :param activeOnly: True para solo clientes activos, False para cargar a todos.
        :type activeOnly: bool
        :return: listado de clientes
        :rtype: list[str]

        """
        if activeOnly:
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
        """

        Devuelve los datos del cliente que corresponden al DNI seleccionado.

        :param dni: DNI o NIE del cliente.
        :type dni: str.
        :return: Datos de un cliente.
        :rtype: list.

        """
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
        """

        Obtiene el DNI de un cliente a partir de su número de móvil.

        :param mobile: Número de teléfono del cliente.
        :type mobile: str
        :return: DNI del cliente.
        :rtype: str

        """
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
        """

        Pasa un cliente a histórico.

        :param dni: DNI del cliente a desactivar
        :type dni: str
        :return: True si la operación fue exitosa, False en caso contrario.
        :rtype: bool

        """
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
        """

        Inserta un nuevo cliente en la base de datos.

        :param data: Lista de valores con los datos del cliente
        :type data: list
        :return: True si se insertó correctamente, False en caso contrario.
        :rtype: bool

        """
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
        """

        Modifica los datos de un cliente existente en la base de datos.

        :param data: Lista de valores con los nuevos datos del cliente
        :type data: list
        :return: True si la modificación fue exitosa, False en caso contrario
        :rtype: bool

        """
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


         ######################
    #### ##--## PRODUCTS ##--## ####  ###########################################################################################
         ######################

    @staticmethod
    def _checkPrice(price):
        """

        Valida y formatea el precio de un producto.

        Permite números enteros o decimales con uno o dos decimales,
        usando coma o punto como separador. Devuelve el valor con
        punto como separador decimal.

        :param price: Precio introducido por el usuario
        :type price: str
        :return: Precio formateado o False si no es válido
        :rtype: str | bool

        """
        pattern = r'^\d+([,.]\d{1,2})?$'

        try:
            price = price.strip()

            if re.match(pattern, price):
                formattedPrice = price.replace(',', '.')
                Globals.ui.txt_productPrice.setStyleSheet("background-color: rgb(255, 255, 220); color black")
                return formattedPrice

            else:
                Globals.ui.txt_productPrice.setStyleSheet("background-color: #FFC0CB; color black")
                Globals.ui.txt_productPrice.setText(None)
                Globals.ui.txt_productPrice.setPlaceholderText("Invalid price format")

                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Please, use formats like:\n"
                             "0,00\t 99,99\t 12,90\t 10,5")
                mbox.exec()
                return False

        except Exception as error:
            print("(Connection._checkPrice) There was an error while checking price: ", error)


    @staticmethod
    def getProducts():
        """

        Devuelve la lista completa de productos.

        :return: Listado de productos
        :rtype: list[list]

        """
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
        """

        Obtiene toda la información de un producto a partir de su código.

        :param code: Código del producto
        :type code: str
        :return: Lista con los datos del producto
        :rtype: list

        """
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
        """

        Inserta un nuevo producto en la base de datos.

        :param data: Lista con los datos del producto
        :type data: list
        :return: True si el producto se insertó correctamente, False en caso contrario
        :rtype: bool

        """
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
        """

        Borra el producto de la base de datos.

        :param productName: Nombre del producto a eliminar
        :type productName: str
        :return: True si la eliminación fue exitosa, False en caso contrario
        :rtype: bool

        """
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
        """

        Modifica los datos de un producto existente.

        :param data: Lista con los nuevos datos del producto.
        :type data: list
        :return: True si la modificación fue exitosa, False en caso contrario
        :rtype: bool

        """
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


         ###################
    #### ##-## INVOICE ##-## ####   ##########################################################################################
         ###################
    @staticmethod
    def getInvoices():  ### allInvoices
        """

        Obtiene todas las facturas de la base de datos.

        :return: Listado de facturas
        :rtype: list[list]

        """
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
        """

        Obtiene el identificador de la última factura asociada a un cliente.

        :param dni: DNI del cliente.
        :type dni: str
        :return: Identificador de la factura.
        :rtype: int | None

        """
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
        """

        Obtiene la información completa de una factura.

        :param id: Identificador de la factura.
        :type id: int
        :return: Lista con los datos de la factura.
        :rtype: list

        """
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
        """

        Inserta una nueva factura en la base de datos.

        :param dni: DNI del cliente a facturar.
        :type dni: str
        :param data: Datos asociados a la factura.
        :type data: str
        :return: True si la factura se insertó correctamente, False en caso contrario
        :rtype: bool

        """
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
    def deleteInvoice(invoiceId):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE  FROM invoices "
                          "    WHERE id_fac = :invoiceId;")
            query.bindValue(":invoiceId", invoiceId)

            if not query.exec():
                return False
            return True
        except Exception as error:
            print("(Connection.deleteInvoice) An error occurred while trying to delete the invoice from the database: ", error)
        return True


    @staticmethod
    def selectProduct(item):
        """

        Obtiene la información de un producto en específico.

        :param item: Código del producto
        :type item: str | int
        :return: Lista con los datos del producto.
        :rtype: list

        """

        try:
            row = []
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
    def verifyInvoiceSale(invoice):   #existeFacturaSales
        """

         Verifica si una factura tiene ventas asociadas.

        :param invoice: Identificador de la factura.
        :type invoice: int
        :return: True si la factura tiene ventas asociadas, False en caso contrario.
        :rtype: bool

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT  *"
                          "    FROM sales"
                          "    WHERE idfac = :invoice")
            query.bindValue(":invoice", int(invoice))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False

        except Exception as error:
            print("There was an error while verifying the invoice: ", error)


    @staticmethod
    def addSale(data):
        """

        Inserta una venta asociada a una factura.

        :param data: Datos de la venta.
        :type data: list
        :return: True si se insertó correctamente, False en caso contrario.
        :rtype: bool

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO sales "
                          "(invoice_id, product_id, cuantity, Product, unit_price, total) "
                          "VALUES "
                          "(:invoice_id, :product_id, :cuantity, :Product, :unit_price, :total)")

            valuesOrder = [":invoice_id", ":product_id", ":cuantity", ":Product", ":unit_price", ":total"]

            for i in range(len(valuesOrder)):
                query.bindValue(valuesOrder[i], str(data[i]))

            if not query.exec():
                print("(Connection.addSale) There was an SQL error.")
                return False

            return True

        except Exception as error:
            print("(Connection.addSale) There was an error while adding the sale: ", error)


    @staticmethod
    def getSales(invoiceId):
        """

        Obtiene todas las ventas asociadas a una factura.

        :param invoiceId: Identificador de la factura.
        :type invoiceId: int
        :return: Lista de ventas asociadas a la factura.
        :rtype: list[list]

        """
        try:
            saleData = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT  *"
                          "    FROM sales"
                          "    WHERE invoice_id = :invoice_id")

            query.bindValue(":invoice_id", int(invoiceId))

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    saleData.append(row)

            return saleData

        except Exception as error:
            print("(Connection.getSale) There was an error while getting the sale: ", error)
