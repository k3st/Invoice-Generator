import datetime, os
import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
from docxtpl import DocxTemplate

class InvoiceApp:
    def __init__(self, root):
        self.root = root

        # Create labels, entries, and buttons

        self.company = tk.Label(root, text="Company: ")
        self.company.grid(row= 0, column= 0,pady=20, sticky="e")
        self.company_entry = tk.Entry(root)
        self.company_entry.grid(row= 0, column= 1,columnspan=2, sticky="ew")

        #CALENDAR START DATE AND END DATE

        self.start = tk.Label(root, text="Start Date:")
        self.start.grid(row= 1, column= 0)
        self.start_entry = tk.Entry(root)
        self.start_entry.grid(row= 2, column= 0)

        self.end = tk.Label(root, text="End Date:")
        self.end.grid(row= 1, column= 1)
        self.end_entry = tk.Entry(root)
        self.end_entry.grid(row= 2, column= 1)

        self.arrivalTime = tk.Label(root, text="Arrival:")
        self.arrivalTime.grid(row=1, column= 3)
        self.arrivalTime_entry = tk.Entry(root,width=10)
        self.arrivalTime_entry.grid(row= 2, column= 3)

        
        self.driver_label = tk.Label(root, text="Driver:")
        self.driver_label.grid(row= 1, column= 4,sticky="e")
        self.driver_entry = tk.Entry(root)
        self.driver_entry.grid(row= 1, column= 5)

        self.guide_label = tk.Label(root, text="Guide:")
        self.guide_label.grid(row= 2, column= 4,sticky="e")
        self.guide_entry = tk.Entry(root)
        self.guide_entry.grid(row= 2, column= 5)

        self.spacer = ttk.Separator(root, orient='horizontal')
        self.spacer.grid(row= 3, pady="12")

        self.quantity_label = tk.Label(root, text="Days:  ")
        self.quantity_label.grid(row= 4, column= 0,sticky="se")
        self.quantity_entry = tk.Entry(root,width=8)
        self.quantity_entry.grid(row= 4, column= 1,sticky="sw")

        self.price_label = tk.Label(root, text="Price:  ")
        self.price_label.grid(row= 4, column= 3,sticky="se")
        self.price_entry = tk.Entry(root,width=15)
        self.price_entry.grid(row= 4, column= 4,sticky="sw")

        ###         ADD ITEM 

        self.add_item_button = tk.Button(root, text="Add Current Item", command=self.addItems)
        self.add_item_button.grid(row = 4, column= 5,sticky="s")

        self.add_item_button = tk.Button(root, text="Delete Item", command=self.deleteItem)
        self.add_item_button.grid(row = 8, column= 5,sticky="N")
        
        columns = ('start','end','arr','driver','guide','days', 'price', 'total')
        self.tree = ttk.Treeview(root, columns=columns, show= "headings")            

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)

        # # # Configure vertical scrollbar
        # v_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        # self.tree.configure(yscrollcommand=v_scrollbar.set)
        # v_scrollbar.grid(row=0, column=9, rowspan=10, sticky=(tk.N, tk.S))

        # # # Configure horizontal scrollbar
        # h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        # self.tree.configure(xscrollcommand=h_scrollbar.set)
        # h_scrollbar.grid(row=8, column=0, columnspan=8, sticky=(tk.W, tk.E))

        # self.tree.grid(row=7, column=0, columnspan=8,sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tree.grid(row = 7, column=0,columnspan=6, padx=15, pady=10)

        ###         ALL ITEMS

        self.save_generate_button = tk.Button(root, text="Generate Invoice", command=self.generate_invoice)
        self.save_generate_button.grid(row= 9, column=3,stick="NEWS",pady=20)
        self.new_generate_button = tk.Button(root, text="New Invoice", command=self.newInvoice)
        self.new_generate_button.grid(row= 10, column=3,stick="EWS",pady=5)

    def clear_values(self):
        self.driver_entry.delete(0,tk.END)
        self.guide_entry.delete(0,tk.END)
        self.quantity_entry.delete(0,tk.END)
        self.price_entry.delete(0,tk.END)
        self.price_entry.insert(0, "0.0")

    
    def addItems(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        arr = self.arrivalTime_entry.get()
        driver = self.driver_entry.get()
        guide = self.guide_entry.get()
        days = int(self.quantity_entry.get())
        price = float(self.price_entry.get())
        line_total = days * price
        invoice_items = [start,end,arr,driver,guide,days,price,line_total]

        self.tree.insert('',0,values=invoice_items)
        self.clear_values()
        invoice_list.append(invoice_items)
        print("ADDED")

    def deleteItem(self):
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, 'values')
        item_values = (*item_values[:5], int(item_values[5]), float(item_values[6]), float(item_values[7]))
        print(item_values)
        

        for item in invoice_list:
            if item[:8] == list(item_values):
                invoice_list.remove(item)
                print("Exact Item Found: \n"+item+"\nitem has been deleted")
                print(invoice_list)
                break

        self.tree.delete(selected_item)

    def newInvoice(self):
        self.company_entry.delete(0,tk.END)
        self.start_entry.delete(0,tk.END)
        self.end_entry.delete(0,tk.END)
        self.arrivalTime_entry.delete(0,tk.END)
        self.clear_values()
        self.tree.delete(*self.tree.get_children())
        invoice_list.clear()
        print("New Invoice")

    def generate_invoice(self):
        doc = DocxTemplate("invoice_template.docx")
        getDateToday =datetime.datetime.now() 
        companyName = self.company_entry.get()

        grandTotal = sum(item[7] for item in invoice_list)
        todaysDate = getDateToday.strftime("%b %d, %Y")

        doc.render({
            "company":companyName,
            "date_today": todaysDate,
            "invoice_list": invoice_list,
            "grand_total": grandTotal
            
            })
                      
        file_path = "Invoice Receipt/" + getDateToday.strftime("%B") + "/"
        file_name = companyName +".docx"
        
        # DEBUG ##
        doc_name = file_path + getDateToday.strftime("%b-%d-%H%M%S_") + file_name
                
        # doc_name = file_path + getDateToday.strftime("%b-%d_") + file_name

        # Create the directory if it doesn't exist
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        doc.save(doc_name)

        messagebox.showinfo("Message","Invoice Completed")
        # self.newInvoice()

if __name__ == "__main__":
    invoice_list =[]
    window = tk.Tk()
    window.title("Invoice Generator")
    root = tk.Frame(window)
    root.pack()
    
    app = InvoiceApp(root)
    root.mainloop()
