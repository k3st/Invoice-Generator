import datetime, os
import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
from docxtpl import DocxTemplate

def clear_values():
    driver_entry.delete(0,tk.END)
    guide_entry.delete(0,tk.END)
    quantity_entry.delete(0,tk.END)
    price_entry.delete(0,tk.END)
    price_entry.insert(0, "0.0")

def addItems():
    start = start_entry.get()
    end = end_entry.get()
    arr = arrivalTime_entry.get()
    driver = driver_entry.get()
    guide = guide_entry.get()
    days = int(quantity_entry.get())
    price = float(price_entry.get())
    line_total = days * price
    invoice_items = [start,end,arr,driver,guide,days,price,line_total]

    tree.insert('',0,values=invoice_items)
    clear_values()
    invoice_list.append(invoice_items)
    print("ADDED")

def deleteItem():
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item, 'values')
    item_values = (*item_values[:5], int(item_values[5]), float(item_values[6]), float(item_values[7]))
    print(item_values)
    

    for item in invoice_list:
        if item[:8] == list(item_values):
            invoice_list.remove(item)
            print("Exact Item Found: \n"+item+"\nitem has been deleted")
            print(invoice_list)
            break

    tree.delete(selected_item)

def newInvoice():
    company_entry.delete(0,tk.END)
    start_entry.delete(0,tk.END)
    end_entry.delete(0,tk.END)
    arrivalTime_entry.delete(0,tk.END)
    clear_values()
    tree.delete(*tree.get_children())
    invoice_list.clear()
    print("New Invoice")

def generate_invoice():
    doc = DocxTemplate("invoice_template.docx")
    getDateToday =datetime.datetime.now() 
    companyName = company_entry.get()

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
    # newInvoice()


invoice_list =[]
window = tk.Tk()
window.title("Invoice Generator")
root = tk.Frame(window)
root.pack()


# Create labels, entries, and buttons
company = tk.Label(root, text="Company: ")
company.grid(row= 0, column= 0,pady=20, sticky="e")
company_entry = tk.Entry(root)
company_entry.grid(row= 0, column= 1,columnspan=2, sticky="ew")

# # # --    START DATE
start = tk.Label(root, text="Start Date:")
start.grid(row= 1, column= 0)
start_entry = tk.Entry(root)
start_entry.grid(row= 2, column= 0)

# # # --    End Date
end = tk.Label(root, text="End Date:")
end.grid(row= 1, column= 1)
end_entry = tk.Entry(root)
end_entry.grid(row= 2, column= 1)

# # # --    Description Arrival, Driver, Guide      ---     # # #
arrivalTime = tk.Label(root, text="Arrival:")
arrivalTime.grid(row=1, column= 3)
arrivalTime_entry = tk.Entry(root,width=10)
arrivalTime_entry.grid(row= 2, column= 3)

driver_label = tk.Label(root, text="Driver:")
driver_label.grid(row= 1, column= 4,sticky="e")
driver_entry = tk.Entry(root)
driver_entry.grid(row= 1, column= 5)

guide_label = tk.Label(root, text="Guide:")
guide_label.grid(row= 2, column= 4,sticky="e")
guide_entry = tk.Entry(root)
guide_entry.grid(row= 2, column= 5)

# # # --    Description Arrival, Driver, Guide      ---     # # #


spacer = ttk.Separator(root, orient='horizontal')
spacer.grid(row= 3, pady="12")

# # # --    Pricing Start                           ---     # # #
quantity_label = tk.Label(root, text="Days:  ")
quantity_label.grid(row= 4, column= 0,sticky="se")
quantity_entry = tk.Entry(root,width=8)
quantity_entry.grid(row= 4, column= 1,sticky="sw")

price_label = tk.Label(root, text="Price:  ")
price_label.grid(row= 4, column= 3,sticky="se")
price_entry = tk.Entry(root,width=15)
price_entry.grid(row= 4, column= 4,sticky="sw")

# # # --    Pricing End                             ---     # # #


# # # --    Add An Item
add_item_button = tk.Button(root, text="Add Current Item", command=addItems)
add_item_button.grid(row = 4, column= 5,sticky="s")

# # # --    Delete An Item
add_item_button = tk.Button(root, text="Delete Item", command=deleteItem)
add_item_button.grid(row = 8, column= 5,sticky="N")


# # # -- TREE START  -- # # #
columns = ('start','end','arr','driver','guide','days', 'price', 'total')
tree = ttk.Treeview(root, columns=columns, show= "headings")            

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=100)

# # # Configure vertical scrollbar
# v_scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
# tree.configure(yscrollcommand=v_scrollbar.set)
# v_scrollbar.grid(row=0, column=9, rowspan=10, sticky=(tk.N, tk.S))

# # # Configure horizontal scrollbar
# h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
# tree.configure(xscrollcommand=h_scrollbar.set)
# h_scrollbar.grid(row=8, column=0, columnspan=8, sticky=(tk.W, tk.E))

tree.grid(row = 7, column=0,columnspan=6, padx=15, pady=10)

# # # -- TREE END  -- # # #


save_generate_button = tk.Button(root, text="Generate Invoice", command=generate_invoice)
save_generate_button.grid(row= 9, column=3,stick="NEWS",pady=20)
new_generate_button = tk.Button(root, text="New Invoice", command=newInvoice)
new_generate_button.grid(row= 10, column=3,stick="EWS",pady=5)


#windows LOOPING
root.mainloop()