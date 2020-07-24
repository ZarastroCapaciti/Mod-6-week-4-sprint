import pymongo
from pymongo import MongoClient
import json
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import json

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.lbl1 = tk.Label(self, text="Category")
        self.lbl2 = tk.Label(self, text="Brand")
        self.number = tk.StringVar()
        self.productChosen = ttk.Combobox(self, textvariable=7)
        self.productChosen['values'] = ("Chips", "Choclates", "Drinks", "Fruits", "Pies", "Sweets", "Veggies")
        self.productChosen.current(0)
        self.brandChosen = ttk.Combobox(self, textvariable=16)
        self.brandChosen['values'] = ("Simba", "Lays", "No_Brand", "BarOne", "Chomp", "Coca-Cola", "Fanta", "Flake", "Maynards", "Monster Energy", "Play", "PS", "Score", "Speckles", "Sprite", "Tex")
        self.brandChosen.current(0)
        self.btChips = tk.Button(self, command=self.categoryClick, text = "Display Category", height = 2, width = 14)
        self.btnRestore = tk.Button(self, command=self.restoreDB, text = "Restore Database", height = 2, width = 14)
        self.scr = scrolledtext.ScrolledText(self, width=75, height=10, wrap=tk.WORD)
        self.btnTop = tk.Button(self, command=self.topThreeClick, text = "Display Top 3", height = 2, width = 14)
        self.btnDeleteBrand = tk.Button(self, command=self.deleteBrands, text = "Delete Brand", height = 2, width = 14)
        self.updateRecord = tk.Button(self, command=self.updateProduct, text = "Update Product", height = 2, width = 14)
        self.btnLeast = tk.Button(self, command=self.leastThreeBrands, text = "Least 5 Brands", height = 2, width = 14)

        self.lbl1.pack()
        self.productChosen.pack()
        self.lbl2.pack()
        self.brandChosen.pack()
        self.btChips.pack()
        self.btnTop.pack()
        self.btnDeleteBrand.pack()
        self.btnRestore.pack()
        self.updateRecord.pack()
        self.btnLeast.pack()
        self.scr.pack()

    def categoryClick(self):
        self.scr.delete('1.0', tk.END)

        self.cluster = MongoClient("mongodb+srv://admin:admin@cluster0.ycswd.mongodb.net/dbData?retryWrites=true&w=majority")

        self.db = self.cluster["dbData"]
        self.collection = self.db["Products"]

        self.prod = self.productChosen.get()

        for x in self.collection.find({ "Category": self.prod }).sort("Availible_Stock", -1):
            string = x["Product_Name"] + '\t' + str(x["Available_Stock"]) + '\n'
            string = string.expandtabs()
            self.scr.insert(tk.INSERT, string)

    def topThreeClick(self):
        self.scr.delete('1.0', tk.END)

        self.cluster = MongoClient("mongodb+srv://admin:admin@cluster0.ycswd.mongodb.net/dbData?retryWrites=true&w=majority")

        self.db = self.cluster["dbData"]
        self.collection = self.db["Products"]
        self.top_three = self.db["Top_3_Products"]

        self.x = self.top_three.delete_many({})

        self.cnt = 0

        for x in self.collection.find().sort("Available_Stock"):
            if self.cnt != 3:
                self.top_three.insert_one(x)

                string = x["Product_Name"] + '\t' + str(x["Available_Stock"]) + '\n'
                string = string.expandtabs()
                self.scr.insert(tk.INSERT, string)
                self.cnt += 1

    def deleteBrands(self):
        self.scr.delete('1.0', tk.END)

        self.cluster = MongoClient("mongodb+srv://admin:admin@cluster0.ycswd.mongodb.net/dbData?retryWrites=true&w=majority")

        self.db = self.cluster["dbData"]
        self.collection = self.db["Products"]
        self.top_three = self.db["Top_3_Products"]

        self.prod = self.brandChosen.get()

        for x in self.collection.find().sort("Available_Stock"):
            if x["Brand"] == self.prod:
                self.collection.delete_one(x)

        self.scr.insert(tk.INSERT, "Deletion Succesful")

    def restoreDB(self):
        self.scr.delete('1.0', tk.END)

        self.cluster = MongoClient("mongodb+srv://admin:admin@cluster0.ycswd.mongodb.net/dbData?retryWrites=true&w=majority")

        self.db = self.cluster["dbData"]
        self.collection = self.db["Products"]

        self.x = self.collection.delete_many({})

        with open('Products.json') as self.f:
            self.file_data = json.load(self.f)

        self.collection.insert_many(self.file_data)

        self.scr.insert(tk.INSERT, "Database Restored Succesfully")

    def updateProduct(self):
        self.scr.delete('1.0', tk.END)

        self.cluster = MongoClient("mongodb+srv://admin:admin@cluster0.ycswd.mongodb.net/dbData?retryWrites=true&w=majority")

        self.db = self.cluster["dbData"]
        self.collection = self.db["Products"]
        self.top_three = self.db["Top_3_Products"]

        self.p_name = {"Product_Name": "Butternut"}
        self.brand_name = {"Brand": "No_Brand"}

        self.p_name_chnge = { "$set": { "Product_Name": "Aero" } }
        self.brand_name_chnge = { "$set": { "Brand": "Aero" } }

        self.top_three.update_one(self.p_name, self.p_name_chnge)
        self.top_three.update_one(self.brand_name, self.brand_name_chnge)

    def leastThreeBrands(self):
        self.scr.delete('1.0', tk.END)

        self.cluster = MongoClient("mongodb+srv://admin:admin@cluster0.ycswd.mongodb.net/dbData?retryWrites=true&w=majority")

        self.db = self.cluster["dbData"]
        self.collection = self.db["Products"]
        self.top_three = self.db["Top_3_Products"]

        self.cnt = 0

        for x in self.collection.find().sort("Available_Stock", -1):
            if self.cnt != 5:
                self.scr.insert(tk.INSERT, x['Product_Name'] + '\n')
                self.cnt += 1

root = tk.Tk()
app = Application(master=root)
app.mainloop()

root.mainloop()