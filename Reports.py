from reportlab.pdfgen import canvas
from Connection import *
import datetime
import os

class Reports:

    @staticmethod
    def customersReports():   #reportCustomers
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
            c.drawString(280, 650, str(items[3]))
            c.drawString(330, 650, str(items[4]))
            c.drawString(390, 650, str(items[5]))
            c.drawString(480, 650, str(items[6]))
            c.line(50, 645, 525, 645)
            x = 55
            y = 630

            for record in records:
                if y <= 90:
                    c.setFont("Helvetica-Oblique", 8)
                    c.drawString(450, 75, "Página siguiente...")
                    c.showPage() # crea una nueva página
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATUS"]
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(55, 650, str(items[0]))
                    c.drawString(125, 650, str(items[1]))
                    c.drawString(230, 650, str(items[2]))
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
                c.drawString(x + 70, y, record[2])
                c.drawString(x + 140, y, record[3])
                c.drawCentredString(x + 270, y, str(record[5]))
                c.drawString(x + 3280, y, record[8])
                c.drawString(x + 360, y, record[9])
                if str(record[10]) == "True":
                    c.drawString(x + 430,  y, "Active")
                else:
                    c.drawString(x + 430,  y, "Inactive")
                y = y - 25

            c.save()

            for file in os.listdir(rootPath):
                if file.endswith(customerReportName):
                    os.startfile(pdfPath)

        except Exception as error:
            print("There was an error with customersReports: ", error)

        @staticmethod
        def footer(c):
            try:
                c.line(35,50, 525, 50)
                day = datetime.date.today()
                day = day.strftime("%d/%m/%Y %H:%M:%S")
                c.setFont("Helvetica", 7)
                c.drawString(30, 40, day)


            except Exception as error:
                print("There was an error with footer: ", error)