import tkinter as tk
from tkinter import ttk
from fpdf import FPDF

class InvoiceApp:
    def __init__(self, root):
        self.root = root

        # Create labels, entries, and buttons

        self.company = tk.Label(root, text="Company")
        self.company.grid(row= 0, column= 0)
        self.company_entry = tk.Entry(root)
        self.company_entry.grid(row= 0, column= 1)



        self.details = tk.Label(root, text="Enter Invoice Details:")
        self.details.grid(row= 1,pady=10)
        
        self.invoice_label = tk.Label(root, text="Invoice Number:")
        self.invoice_label.grid(row= 2, column= 0)
        self.invoice_entry = tk.Entry(root)
        self.invoice_entry.grid(row= 2, column= 1)

        #CALENDAR START DATE AND END DATE

        self.desc_label = tk.Label(root, text="Description:")
        self.desc_label.grid(row= 3, column= 0)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row= 3, column= 1)

        self.quantity_label = tk.Label(root, text="Days:")
        self.quantity_label.grid(row= 4, column= 0)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row= 4, column= 1)

        self.price_label = tk.Label(root, text="Price:")
        self.price_label.grid(row= 5, column= 0)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row= 5, column= 1)

        ###         ADD ITEM 

        self.add_item_button = tk.Button(root, text="Add Item", command=self.addItems)
        self.add_item_button.grid(row = 7, column= 1, pady=5)

        columns = ('desc','qty',  'price', 'total')
        self.tree = ttk.Treeview(root, columns=columns, show= "headings")
        self.tree.heading('desc', text='Description')
        self.tree.heading('qty', text='Number of Days')        
        self.tree.heading('price', text='Price')
        self.tree.heading('total', text='TOTAL')

        self.tree.grid(row = 8, column=0,columnspan=2,padx=30,pady=10)

        ###         ALL ITEMS

        self.save_generate_button = tk.Button(root, text="Generate Invoice", command=self.generate_invoice)
        self.save_generate_button.grid(row= 9, column=1,pady=10)
        self.new_generate_button = tk.Button(root, text="New Invoice", command=self.newInvoice)
        self.new_generate_button.grid(row= 10, column=0,columnspan=2,pady=10)

    def addItems(self):
        qty = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        desc = self.desc_entry.get()
        line_total = qty * price
        invoice_items = [qty,desc,price,line_total]

        self.tree.insert('',0,values=invoice_items)
        

        print("ADDED")

    def newInvoice(self):
        print("NEWWWW")

    def generate_invoice(self):
        invoice_number = self.invoice_entry.get()
        item = self.item_entry.get()
        quantity = self.quantity_entry.get()

        # Generate invoice text
        invoice_text = f"Invoice Number: {invoice_number}\nItem: {item}\nQuantity: {quantity}"

        # Save invoice to a text file
        with open("invoice.txt", "w") as file:
            file.write(invoice_text)

        # Generate PDF from the text
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=invoice_text, ln=True, align='L')
        pdf.output("invoice.pdf")

        print("Invoice generated successfully!")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Invoice Generator")
    root = tk.Frame(window)
    root.pack()
    
    app = InvoiceApp(root)
    root.mainloop()
