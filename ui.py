import json
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x450")

        self.goals = self.get_data_from_json()
        today = datetime.now()

        self.entry = Entry(self, width=50)
        self.add_button = Button(self, width=10, command=lambda: self.add_goal(today), text="Hedef Ekle")
        self.delete_button = Button(self, width=10, command=self.delete_goal, text="Hedef Sil")
        self.calendar = Calendar(self, selectmode="day", year=today.year, month=today.month, day=13, locale="tr.TR")

        self.table = ttk.Treeview(self, columns=("tarih", "hedef"), show="headings")
        self.table.heading("tarih", text="Tarih")
        self.table.heading("hedef", text="Hedef")
        self.table_init()
        self.table.bind("<<TreeviewSelect>>", lambda event: self.table_item_select())

        self.calendar.grid(row=0, column=0, padx=20)
        self.table.grid(row=0, column=1)
        self.add_button.grid(row=2, column=1)
        self.delete_button.grid(row=2, column=2)
        self.entry.grid(row=1, column=1, pady=20)

    def add_goal(self, today: datetime):
        tarih = self.calendar.get_date()
        if datetime.strptime(tarih, "%d.%m.%Y") < today:
            print("LÜTFEN İLERİ BİR TARİH SEÇİNİZ")
            return

        if tarih in self.goals:
            self.goals[tarih].append({"Hedef": self.entry.get()})
            print(self.goals[tarih])
        else:
            sozluk = {tarih: [{"Hedef": self.entry.get()}]}
            self.goals.update(sozluk)

        self.table.insert(parent="", index=0, values=(tarih, self.goals[tarih][-1]["Hedef"]))
        self.save_to_json()
        print(self.goals)

    def delete_goal(self):

        for item in self.table_item_select():
            print("tur", len(self.table_item_select()))
            tarih = self.table.item(item)["values"][0]
            uzunluk = len(self.goals[self.table.item(item)["values"][0]])

            if uzunluk == 1:
                del self.goals[tarih]
                self.table.delete(item)

            elif uzunluk > 1:
                search_dict = {"Hedef": self.table.item(item)["values"][1]}
                for i, search_item in enumerate(self.goals[tarih]):
                    if search_item == search_dict:
                        indis = i
                        self.goals[tarih].pop(indis)
                        self.table.delete(item)
                        break

        print(self.goals)

    def save_to_json(self):
        try:
            with open("goals.json", mode="r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("goals.json", mode="w") as data_file:
                json.dump(self.goals, data_file, indent=4)
        else:
            data.update(self.goals)
            print("Data", data)
            with open("goals.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)

    def get_data_from_json(self):
        try:
            with open("goals.json", mode="r") as data_file:
                data = json.load(data_file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return

    def delete_from_json(self):
        pass

    def table_item_select(self):
        return self.table.selection()

    def table_init(self):
        if self.goals is None:
            self.goals = {}
            return
        for tarih in self.goals:

            if len(self.goals[tarih]) == 1:
                self.table.insert(parent="", index=0, values=(tarih, self.goals[tarih][-1]["Hedef"]))

            elif len(self.goals[tarih]) > 1:
                for hedef in self.goals[tarih]:
                    self.table.insert(parent="", index=0, values=(tarih, hedef["Hedef"]))
