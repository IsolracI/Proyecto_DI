from reportlab.pdfgen import canvas
from Connection import *
import datetime
import Globals
import os

class Reports:

    @staticmethod
    def customersReports():   #reportCustomers
        """

        Genera un informe en PDF con la lista de clientes.

        :return: None

        """
        try:
            rootPath = ".\\reports"
            data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M_%S")
            customerReportName = data + "_reportCustomers.pdf"
            pdfPath = os.path.join(rootPath, customerReportName)
            c = canvas.Canvas(pdfPath)
            records = Connection.getCustomers(False)
            items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATUS"]
            c.setFont("Helvetica-Bold", 10)
            c.drawString(55, 650, str(items[0]))
            c.drawString(125, 650, str(items[1]))
            c.drawString(210, 650, str(items[2]))
            c.drawString(270, 650, str(items[3]))
            c.drawString(340, 650, str(items[4]))
            c.drawString(385, 650, str(items[5]))
            c.drawString(480, 650, str(items[6]))
            c.line(50, 645, 525, 645)
            x = 55
            y = 630

            Reports.footer(c, "Customers Report")

            for record in records:
                if y <= 90:
                    c.setFont("Helvetica-Oblique", 8)
                    c.drawString(450, 75, "Página siguiente...")
                    c.showPage() # crea una nueva página
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATUS"]
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(55, 650, str(items[0]))
                    c.drawString(125, 650, str(items[1]))
                    c.drawString(210, 650, str(items[2]))
                    c.drawString(280, 650, str(items[3]))
                    c.drawString(330, 650, str(items[4]))
                    c.drawString(390, 650, str(items[5]))
                    c.drawString(480, 650, str(items[6]))
                    c.line(50, 645, 525, 645)
                    x = 55
                    y = 630

                c.setFont("Helvetica", 8)
                dni = "***" + str(record[0][4:7] + "***")
                c.drawCentredString(x + 19, y, dni)
                c.drawString(x + 62, y, record[2])
                c.drawString(x + 155, y, record[3])
                c.drawCentredString(x + 234, y, str(record[5]))
                c.drawString(x + 277, y, record[8])
                c.drawString(x + 350, y, record[9])
                if str(record[10]) == "True":
                    c.drawString(x + 434,  y, "Active")
                else:
                    c.drawString(x + 431,  y, "Inactive")
                y = y - 25

            c.save()

            for file in os.listdir(rootPath):
                if file.endswith(customerReportName):
                    os.startfile(pdfPath)

        except Exception as error:
            print("There was an error with customersReports: ", error)


    @staticmethod
    def footer(c, title):
        """

        Dibuja el pie de página del documento PDF.

        :param c: Lienzo del PDF sobre el que se dibuja el contenido
        :type c: reportlab.pdfgen.canvas.Canvas
        :param title: Título del informe o documento
        :type title: str
        :return: None

        """
        try:
            day = datetime.date.today()
            day = day.strftime("%d/%m/%Y %H:%M:%S")
            c.line(35, 50, 350, 50)
            c.setFont("Helvetica", 7)
            c.drawString(30, 40, day)
            c.drawString(30, 30, title)
            c.drawString(400, 50, str("Página: " + str(c.getPageNumber())))

        except Exception as error:
            print("There was an error with footer: ", error)

    """@staticmethod
    def header(title):
        try:
            path_logo = ".\\assets\\logo.png"
            logo = Image.open(path_logo)
            if isinstance(logo, Image.Image):
                self.c.line(35, 60, 525, 60)
                self.c.setFont('Helvetica-Bold', 0)
                self.c.drawString(55, 785, "EMPRESA TEIS")
                self.c.drawCentredString(300, 675, titulo)
                self.c.line(35, 665, 525, 665)
                # Logo
                self.c.drawImage(path_logo, 490, 765, width=40, height=40)
                # Company details
                self.c.setFont('Helvetica', 9)
                self.c.drawString(55, 760, "CIF: B12345678")
                self.c.drawString(55, 745, "Dirección: Calle Galicia, 123")
                self.c.drawString(55, 730, "Vigo 36215 - España")
                self.c.drawString(55, 715, "Teléfono: +34 986 123 456")
                self.c.drawString(55, 700, "Email: teis@mail.com")

                self.c.rect(30, 690, 200, 80)
            else:
                print('No se pudo cargar el logo')

        except Exception as e:
            print('Error en toreport', e)"""

    @staticmethod
    def ticket():
        """

        Genera un ticket o factura en formato PDF para una venta.

        :return: None

        """
        try:
            dni =Globals.ui.txt_dniFactura.text()
            if dni == "00000000T":
                titulo = "FACTURA SIMPLIFICADA"
            else:
                titulo = "FACTURA"

            rootPath = ".\\reports"
            data = datetime.datetime.now().strftime("%d_%m_%Y %H_%M_%S")
            productReportName = data + "_reportProducts.pdf"
            pdfPath = os.path.join(rootPath, productReportName)
            c = canvas.Canvas(pdfPath)

            customerData = Connection.getCustomerInfo(dni)

            c.setFont('Helvetica-Bold', 10)
            c.drawString(220, 700, "DNI: " + str(customerData[0]))
            c.drawString(220, 685, "APELLIDOS: " + str(customerData[1]))
            c.drawString(220, 670, "NOMBRE: " + str(customerData[2]))
            c.drawString(220, 655, "DIRECCIÓN: " + str(customerData[6]))
            c.drawString(220, 640, "LOCALIDAD: " + str(customerData[8]) + " PROVINCIA: " + str(customerData[7]))

            Reports.footer(c, titulo)

        except Exception as error:
            print("There was an error with ticket: ", error)