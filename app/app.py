import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import DISABLED
from app.db import DB

ctk.set_appearance_mode('dark')


class App:
    def __init__(self, db: DB)  -> None:
        self._db = db
        self._main_window = ctk.CTk()#tk.Tk()#
        self._main_window.geometry('1200x750')
        self._main_window.title('Заезды')

        self._tab_view = ctk.CTkTabview(self._main_window, 1200, 750)#ttk.Notebook(self._main_window, width=1200, height=700)
        races_tab = self._tab_view.add('Заезды')#ttk.Frame(self._tab_view)#
        jockeys_tab = self._tab_view.add('Жокеи')#ttk.Frame(self._tab_view)#
        hippodromes_tab = self._tab_view.add('Ипподромы')#ttk.Frame(self._tab_view)#
        owners_tab = self._tab_view.add('Владельцы')#ttk.Frame(self._tab_view)#
        horses_tab = self._tab_view.add('Лошади')#ttk.Frame(self._tab_view)

        # self._tab_view.add(races_tab, text='Заезды')
        # self._tab_view.add(jockeys_tab, text='')
        # self._tab_view.add(hippodromes_tab)
        # self._tab_view.add(owners_tab)
        # self._tab_view.add(horses_tab)


        self._races_frame = ctk.CTkScrollableFrame(races_tab, 1150, 730)
        ctk.CTkButton(self._races_frame,
                      text='Добавить заезд',
                      command=self._show_race_adding_window).pack()
        self._races_frame.pack()

        self._jockeys_frame = ctk.CTkScrollableFrame(jockeys_tab, 1150, 730)
        self._jockeys_frame.pack()

        self._hippodromes_frame = ctk.CTkScrollableFrame(hippodromes_tab, 1150, 730)
        self._hippodromes_frame.pack()


        self._owners_frame = ctk.CTkScrollableFrame(owners_tab, 1150, 730)
        self._owners_frame.pack()

        self._horses_frame = ctk.CTkScrollableFrame(horses_tab, 1150, 730)
        self._horses_frame.pack()

        self._tab_view.grid(column=0, row=0)

    def _fill_race_frame(self):
        for race in self._db.get_all_races():
            ArgumentSendButton(self._races_frame,
                          text=race[1],
                          command=self._show_race_info,
                          arg=race[0]).pack(padx=10,pady=10)

    def _show_race_adding_window(self):
        window = ctk.CTkToplevel()
        window.title('Добавление заезда')
        window.geometry('500x500')

        hippodromes = {x[1]:x[0] for x in self._db.get_all_hippodromes()}

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Название',
                                  width=400,
                                  corner_radius=0)
        date_entry = ctk.CTkEntry(window,
                                  placeholder_text='Дата',
                                  width=400,
                                  corner_radius=0)
        hippodrome_choose = ctk.CTkOptionMenu(window,
                                              width=400,
                                              values=list(hippodromes.keys()))

        name_entry.pack(padx=10, pady=10)
        date_entry.pack(padx=10, pady=10)
        hippodrome_choose.pack(padx=10, pady=10)
        ctk.CTkButton(window,
                      command=lambda: self._add_race({
                                'name': name_entry.get(),
                                'date': date_entry.get(),
                                'hippodrome_id': hippodromes[hippodrome_choose.get()]
                                },
                      window))\
                        .pack(padx=10, pady=10)

    def _show_race_info(self, race_id):
        window = ctk.CTkToplevel()
        window.title('Информация о заезде')
        window.geometry('600x600')
        window.grid_anchor('n')

        race = {
            'info': self._db.get_race(race_id)[0],
            'results': self._db.get_race_results(race_id)
        }
        LabelWithBg(window, text='Название:',font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Дата:',font=ctk.CTkFont(size=18)).grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Иподром:',font=ctk.CTkFont(size=18)).grid(row=2, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Результаты:',font=ctk.CTkFont(size=18)).grid(row=3, column=0, pady=10, padx=10, sticky='ew')

        LabelWithBg(window, text=race['info'][0],font=ctk.CTkFont(size=18)).grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=race['info'][1],font=ctk.CTkFont(size=18)).grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        ctk.CTkButton(window,
                      text=race['info'][2],
                      font=ctk.CTkFont(size=12),
                      command= lambda: ...).grid(row=2, column=1, pady=10, sticky='ew')
        scrollable_frame = ctk.CTkScrollableFrame(window)
        scrollable_frame.grid(row=3, column=0, rowspan=3, columnspan=3, sticky='ew')
        #ctk.CTkLabel(window, text=race['info'][0]).pack(padx=10, pady=10)

    def _add_race(self, race_data, window):
        try:
            race_id = self._db.create_race(
                race_data['name'],
                race_data['date'],
                race_data['hippodrome_id']
            )
            print(race_id)
        except Exception as err:
            App.show_message(str(err))
        else:
            window.destroy()
            ctk.CTkButton(self._races_frame,
                          text=race_data['name'].strip(),
                          command=lambda: self._show_race_info(race_id)).pack(padx=10,pady=10)

    @staticmethod
    def show_message(message: str) -> None:
        """
        Отрисовка окна с указанными сообщением и заголовком.

        Args:
            message: str - сообщение для отображение.
            title: str - заголовок окна.
        """
        window = ctk.CTkToplevel()
        window.title('Ошибка')
        window.geometry('800x200')
        ctk.CTkLabel(window, text=message).place(relx=0.5, rely=0.5, anchor='center')

    def run(self):
        self._fill_race_frame()
        self._main_window.mainloop()


class ArgumentSendButton(ctk.CTkButton):
    def __init__(self, master, command, text, arg):
        super().__init__(master,
                       text=text,
                       command=command)
        self._arg = arg

    def _clicked(self, event=None):
        if self._state != DISABLED:
            self._on_leave()
            self._click_animation_running = True
            self.after(100, self._click_animation)

            if self._command is not None:
                self._command(self._arg)

class LabelWithBg(ctk.CTkLabel):
    """Класс текстовой метки с серым фоном."""
    def __init__(self, master, text: str, font: ctk.CTkFont = None) -> None:
        super().__init__(master,
                         text=text,
                         fg_color=("gray70", "gray30"),
                         corner_radius=0,
                         font=font if font is not None else ctk.CTkFont(size=20))