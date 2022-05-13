# # Mini Project Python Kurs Mata Uang


import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

# buat class kurs_uang
class kurs_uang:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.mata_uang = self.data["rates"]

    def convert(self, uang1, uang2, jumlah):
        jumlah_awal = jumlah
        # Ubah mata uang ke USD sebagai default
        if uang1 != "USD":
            jumlah = jumlah / self.mata_uang[uang1]

        # 2 angka setelah koma
        jumlah = round(jumlah * self.mata_uang[uang2], 2)
        return jumlah


class App(tk.Tk):
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = "Kurs Mata Uang"
        self.converter_uang = converter

        # self.configure(background = 'blue')
        self.geometry("500x200")

        # Label
        self.intro_label = Label(
            self,
            text="Kurs Mata Uang Real Time",
            fg="blue",
            relief=tk.RAISED,
            borderwidth=3,
        )
        self.intro_label.config(font=("Courier", 15, "bold"))

        self.date_label = Label(
            self,
            text=f"1 USD setara dengan = {self.converter_uang.convert('USD','IDR',1)} IDR \n Date : {self.converter_uang.data['date']}",
            relief=tk.GROOVE,
            borderwidth=5,
        )

        self.intro_label.place(x=100, y=5)
        self.date_label.place(x=120, y=50)

        # Entry box
        valid = (self.register(self.restrictNumber), "%d", "%P")
        self.kolom_uang1 = Entry(
            self,
            bd=3,
            relief=tk.RIDGE,
            justify=tk.CENTER,
            width=16,
            validate="key",
            validatecommand=valid,
        )
        self.kolom_uang2 = Label(
            self,
            text="",
            fg="black",
            bg="white",
            relief=tk.RIDGE,
            justify=tk.CENTER,
            width=16,
            borderwidth=3,
        )

        # dropdown
        self.uang1_variable = StringVar(self)
        self.uang1_variable.set("USD")  # default value
        self.uang2_variable = StringVar(self)
        self.uang2_variable.set("IDR")  # default value

        font = ("Courier", 12, "bold")
        self.option_add("*TCombobox*Listbox.font", font)
        self.uang1_dropdown = ttk.Combobox(
            self,
            textvariable=self.uang1_variable,
            values=list(self.converter_uang.mata_uang.keys()),
            font=font,
            state="readonly",
            width=12,
            justify=tk.CENTER,
        )
        self.uang2_dropdown = ttk.Combobox(
            self,
            textvariable=self.uang2_variable,
            values=list(self.converter_uang.mata_uang.keys()),
            font=font,
            state="readonly",
            width=12,
            justify=tk.CENTER,
        )

        # penempatan
        self.uang1_dropdown.place(x=30, y=120)
        self.kolom_uang1.place(x=28, y=150)
        self.uang2_dropdown.place(x=340, y=120)
        # self.converted_amount_field.place(x = 346, y = 150)
        self.kolom_uang2.place(x=338, y=150)

        # Tombol ubah
        self.tombol_ubah = Button(self, text="Rubah", fg="black", command=self.perform)
        self.tombol_ubah.config(font=("Courier", 10, "bold"))
        self.tombol_ubah.place(x=220, y=135)

    def perform(self):
        jumlah = float(self.kolom_uang1.get())
        uang_asal = self.uang1_variable.get()
        uang_baru = self.uang2_variable.get()

        hasil_kurs = self.converter_uang.convert(uang_asal, uang_baru, jumlah)
        hasil_kurs = round(hasil_kurs, 2)

        self.kolom_uang2.config(text=str(hasil_kurs))

    # validasi angka saja
    def restrictNumber(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return string == "" or (string.count(".") <= 1 and result is not None)


if __name__ == "__main__":
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    converter = kurs_uang(url)

    App(converter)
    mainloop()
