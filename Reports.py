from datetime import datetime

from reportlab.pdfgen import canvas
import os

class Reports:

    @staticmethod
    def customersReports():   #reportCustomers
        try:
            rootPath = ".\\reports"
            data = datetime.now.strftime("%d/%m/%Y %H:%M:%S")
            namePortCli = data + "_reportCustomers"
            pdfPath = os.path.join(rootPath)
            c = canvas.Canvas('reports/customers.pdf')
            c.drawString(100, 100, 'Customers')
            c.save()

            for file in os.listdir(rootPath):
                if file.endswith(namePortCli):
                    os.startfile(pdfPath)

        except Exception as error:
            print("There was an error with customersReports: ", error)