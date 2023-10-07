from docxtpl import DocxTemplate

doc = DocxTemplate("invoice_template.docx")

invoice_list = [["OCT1","OCT4","PM","Cris","no guide",3,10000],["OCT1","OCT4","PM","Caiden","with",3,10000],["OCT1","OCT4","PM","Kent","gidu",3,10000]]

doc.render({
            "company":"Wow",
            "date_today":"date today",
            "invoice_list": invoice_list,
            "grand_total": 30999
            
            })
doc.save("new_invoice.docx")