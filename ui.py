import json
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from ttkthemes import ThemedTk


class Window(ThemedTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x450")
        self.set_theme_advanced("radiance", hue=2)
        # Python private verisi
        self.__goals = self.get_data_from_json()
        today = datetime.now()

        self.header = Canvas(self, background="#693177", width=800, height=50)
        self.title_label = self.header.create_text(70, 35, text="To-Do List", font=("Times", "20", "bold"), fill="white")
        self.entry = ttk.Entry(self, width=40)
        self.entry2 = ttk.Entry(self, width=40)
        self.add_label = ttk.Label(self, text="Hedeflerini Buraya Ekle !!", font=("Times", "13"))
        self.tag_label = ttk.Label(self, text="Etiketlemek İçin Buraya !!", font=("Times", "13"))
        self.add_button = ttk.Button(self, width=10, command=lambda: self.add_goal(today), text="Hedef Ekle")
        self.delete_button = ttk.Button(self, width=10, command=self.delete_goal, text="Hedef Sil")
        self.calendar = Calendar(self, selectmode="day", year=today.year, month=today.month, day=13,
                                 locale="tr.TR", background="#824998", selectbackground="purple")

        self.table = ttk.Treeview(self, columns=("tarih", "hedef", "etiketler"), show="headings")
        self.table.heading("tarih", text="Tarih")
        self.table.column("tarih", anchor="w", stretch=NO, width=133)
        self.table.heading("hedef", text="Hedef")
        self.table.column("hedef", anchor="w", stretch=NO, width=133)
        self.table.heading("etiketler", text="Etiketler")
        self.table.column("etiketler", anchor="w", stretch=NO, width=133)

        self.table.bind("<<TreeviewSelect>>", lambda event: self.table_item_select())
        self.table_init()

        self.header.place(x=0, y=0)
        self.calendar.place(x=0, y=50, width=400, height=250)
        self.table.place(x=400, y=50, width=400, height=250)
        self.add_button.place(x=400, y=330)
        self.delete_button.place(x=400, y=395)
        self.entry.place(x=75, y=335)
        self.add_label.place(x=75, y=310)
        self.tag_label.place(x=75, y=375)
        self.entry2.place(x=75, y=400)

    def add_goal(self, today: datetime):
        tarih = self.calendar.get_date()
        if self.error_checker(tarih, today):
            return

        if tarih in self.__goals:
            self.__goals[tarih].append({"Hedef": self.entry.get()})
            # print(self.goals[tarih])
        else:
            sozluk = {tarih: [{"Hedef": self.entry.get()}]}
            self.__goals.update(sozluk)

        self.table.insert(parent="", index=0, values=(tarih, self.__goals[tarih][-1]["Hedef"]))
        self.save_to_json()
        # print(self.goals)

    def error_checker(self, tarih, today: datetime):
        if datetime.strptime(tarih, "%d.%m.%Y") < today:
            messagebox.showwarning(title="Geçersiz Tarih", message="LÜTFEN İLERİ BİR TARİH SEÇİNİZ")
            return True
        elif self.entry.get() == "":
            messagebox.showerror(title="Hedef YOK", message="HEDEFINIZI GIRINIZ")
            return True
        else:
            return not messagebox.askyesno(title="Ekleme", message="Hedefi eklemek istediğinizi emin misiniz")

    def delete_goal(self):
        for item in self.table_item_select():
            print("len", len(item))
            tarih = str(self.table.item(item)["values"][0])
            uzunluk = len(self.__goals[tarih])

            if uzunluk == 1:
                self.__goals.pop(tarih, None)
                self.table.delete(item)

            elif uzunluk > 1:
                search_dict = {"Hedef": str(self.table.item(item)["values"][1])}
                for i, search_item in enumerate(self.__goals[tarih]):
                    if search_item == search_dict:
                        self.__goals[tarih].pop(i)
                        self.table.delete(item)
                        break

        self.save_to_json()
        # print(self.goals)

    def save_to_json(self):

        # print("Self.goals", self.goals)
        # # data.update(self.goals)
        # new_data = {}
        # for key, value in self.goals.items():
        #     new_data[key] = value
        #
        # print("after Data", new_data)
        with open("goals.json", mode="w") as data_file:
            json.dump(self.__goals, data_file, indent=4)

    def get_data_from_json(self):
        try:
            with open("goals.json", mode="r") as data_file:
                data = json.load(data_file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return

    def table_item_select(self):
        return self.table.selection()

    def table_init(self):
        if self.__goals is None:
            self.__goals = {}
            return
        for tarih in self.__goals:

            if len(self.__goals[tarih]) == 1:
                self.table.insert(parent="", index=0, values=(tarih, self.__goals[tarih][-1]["Hedef"]))

            elif len(self.__goals[tarih]) > 1:
                for hedef in self.__goals[tarih]:
                    self.table.insert(parent="", index=0, values=(tarih, hedef["Hedef"]))
