from reportlab.pdfgen import canvas
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
            c.drawString(100, 100, 'Customers')
            c.save()

            for file in os.listdir(rootPath):
                if file.endswith(customerReportName):
                    os.startfile(pdfPath)

        except Exception as error:
            print("There was an error with customersReports: ", error)