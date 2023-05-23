import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import DISABLED, NORMAL
from app.db import DB

ctk.set_appearance_mode('dark')


class App:
    def __init__(self, db: DB)  -> None:
        self._db = db
        self._main_window = ctk.CTk()
        self._main_window.geometry('800x570')
        self._main_window.title('Заезды')

        self._tab_view = ctk.CTkTabview(self._main_window, 800, 500)
        races_tab = self._tab_view.add('Заезды')
        jockeys_tab = self._tab_view.add('Жокеи')
        hippodromes_tab = self._tab_view.add('Ипподромы')
        owners_tab = self._tab_view.add('Владельцы')
        horses_tab = self._tab_view.add('Лошади')

        self._races_frame = ctk.CTkScrollableFrame(races_tab, 780, 480)
        self._races_frame.pack()
        self._race_adding_button = ctk.CTkButton(races_tab,
                      text='Добавить заезд',
                      command=self._show_race_adding_window)
        self._race_adding_button.pack(fill='x')

        self._jockeys_frame = ctk.CTkScrollableFrame(jockeys_tab, 780, 480)
        self._jockeys_frame.pack()
        ctk.CTkButton(jockeys_tab,
                      text='Добавить жокея',
                      command=self._show_jockey_adding_window).pack(fill='x')

        self._hippodromes_frame = ctk.CTkScrollableFrame(hippodromes_tab, 780, 480)
        self._hippodromes_frame.pack()
        ctk.CTkButton(hippodromes_tab,
                      text='Добавить ипподром',
                      command=self._show_hippodrome_adding_window).pack(fill='x')

        self._owners_frame = ctk.CTkScrollableFrame(owners_tab, 780, 480)
        self._owners_frame.pack()
        ctk.CTkButton(owners_tab,
                      text='Добавить владельца',
                      command=self._show_owner_adding_window).pack(fill='x')

        self._horses_frame = ctk.CTkScrollableFrame(horses_tab, 780, 480)
        self._horses_frame.pack()
        self._horse_adding_button = ctk.CTkButton(horses_tab,
                      text='Добавить лошадь',
                      command=self._show_horse_adding_window)
        self._horse_adding_button.pack(fill='x')

        self._tab_view.pack()

    def _fill_race_frame(self):
        for race in self._db.get_all_races():
            ArgumentSendButton(self._races_frame,
                          text=race[1],
                          command=self._show_race_info,
                          arg=race[0]).pack(padx=10,pady=10)

    def _fill_jockeys_frame(self):
        for jockey in self._db.get_all_jockeys():
            ArgumentSendButton(self._jockeys_frame,
                               text=jockey[1],
                               command=self._show_jockey_info,
                               arg=jockey[0]).pack(padx=10,pady=10)

    def _fill_hippodromes_frame(self):
        for hippodrome in self._db.get_all_hippodromes():
            ArgumentSendButton(self._hippodromes_frame,
                               text=hippodrome[1],
                               command=self._show_hippodrome_info,
                               arg=hippodrome[0]).pack(padx=10,pady=10)

    def _fill_owners_frame(self):
        for owner in self._db.get_all_owners():
            ArgumentSendButton(self._owners_frame,
                               text=owner[1],
                               command=self._show_owner_info,
                               arg=owner[0]).pack(padx=10,pady=10)

    def _fill_horses_frame(self):
        for horse in self._db.get_all_horses():
            ArgumentSendButton(self._horses_frame,
                               text=horse[1],
                               command=self._show_horse_info,
                               arg=horse[0]).pack(padx=10,pady=10)

    def _show_race_adding_window(self):
        window = ctk.CTkToplevel()
        window.title('Добавление заезда')
        window.geometry('500x300')

        hippodromes = {x[1]:x[0] for x in self._db.get_all_hippodromes()}

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Название',
                                  width=400,
                                  corner_radius=0)
        date_entry = ctk.CTkEntry(window,
                                  placeholder_text='Дата (YYYY-MM-DD)',
                                  width=400,
                                  corner_radius=0)
        hippodrome_choose = ctk.CTkOptionMenu(window,
                                              width=400,
                                              values=list(hippodromes.keys()))

        name_entry.pack(padx=10, pady=10)
        date_entry.pack(padx=10, pady=10)
        hippodrome_choose.pack(padx=10, pady=10)
        ctk.CTkButton(window,
                      text='Добавить',
                      command=lambda: self._add_race({
                                'name': name_entry.get(),
                                'date': date_entry.get(),
                                'hippodrome_id': hippodromes[hippodrome_choose.get()]
                                }, window))\
                      .pack(padx=10, pady=10)

    def _show_owner_adding_window(self):
        window = ctk.CTkToplevel()
        window.title('Добавление владельца')
        window.geometry('500x300')

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Имя',
                                  width=400,
                                  corner_radius=0)
        address_entry = ctk.CTkEntry(window,
                                  placeholder_text='Адрес',
                                  width=400,
                                  corner_radius=0)
        phone_number_entry = ctk.CTkEntry(window,
                                  placeholder_text='Телефон',
                                  width=400,
                                  corner_radius=0)

        name_entry.pack(padx=10, pady=10)
        address_entry.pack(padx=10, pady=10)
        phone_number_entry.pack(padx=10, pady=10)
        ctk.CTkButton(window,
                      text='Добавить',
                      command=lambda: self._add_owner({
                                'name': name_entry.get(),
                                'telephone': phone_number_entry.get(),
                                'address': address_entry.get()
                                }, window))\
                      .pack(padx=10, pady=10)

    def _show_horse_adding_window(self, owner_id = None, owner_info_window = None):
        window = ctk.CTkToplevel()
        window.title('Добавление владельца')
        window.geometry('500x300')

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Имя',
                                  width=400,
                                  corner_radius=0)
        age_entry = ctk.CTkEntry(window,
                                  placeholder_text='Возраст',
                                  width=400,
                                  corner_radius=0)
        gender_entry = ctk.CTkEntry(window,
                                  placeholder_text='Пол (мужской/женский)',
                                  width=400,
                                  corner_radius=0)

        name_entry.pack(padx=10, pady=10)
        age_entry.pack(padx=10, pady=10)
        gender_entry.pack(padx=10, pady=10)
        if owner_id is None:
            owners = [f'{x[0]} - {x[1]}' for x in self._db.get_all_owners()]
            owner_choose = ctk.CTkOptionMenu(window,
                                         width=400,
                                         values=owners)
            owner_choose.pack(padx=10, pady=10)
        ctk.CTkButton(window,
                      text='Добавить',
                      command=lambda: self._add_horse({
                                'name': name_entry.get(),
                                'age': age_entry.get(),
                                'gender': gender_entry.get(),
                                'owner_id': owner_id if owner_id is not None else owner_choose.get().split('-')[0]
                                }, window, owner_info_window))\
                      .pack(padx=10, pady=10)

    def _show_jockey_adding_window(self):
        window = ctk.CTkToplevel()
        window.title('Добавление жокея')
        window.geometry('500x300')

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Имя',
                                  width=400,
                                  corner_radius=0)
        age_entry = ctk.CTkEntry(window,
                                  placeholder_text='Возраст',
                                  width=400,
                                  corner_radius=0)
        address_entry = ctk.CTkEntry(window,
                                  placeholder_text='Адрес',
                                  width=400,
                                  corner_radius=0)
        rating_entry = ctk.CTkEntry(window,
                                  placeholder_text='Рейтинг',
                                  width=400,
                                  corner_radius=0)

        name_entry.pack(padx=10, pady=10)
        age_entry.pack(padx=10, pady=10)
        address_entry.pack(padx=10, pady=10)
        rating_entry.pack(padx=10, pady=10)

        ctk.CTkButton(window,
                      text='Добавить',
                      command=lambda: self._add_jockey({
                                'name': name_entry.get(),
                                'age': age_entry.get(),
                                'address': address_entry.get(),
                                'rating': rating_entry.get()
                                }, window))\
                      .pack(padx=10, pady=10)

    def _show_hippodrome_adding_window(self):
        window = ctk.CTkToplevel()
        window.title('Добавление ипподрома')
        window.geometry('500x200')

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Название',
                                  width=400,
                                  corner_radius=0)
        name_entry.pack(padx=10, pady=10)
        ctk.CTkButton(window,
                      text='Добавить',
                      command=lambda: self._add_hippodrome(name_entry.get(), window))\
                      .pack(padx=10, pady=10)

    def _show_race_info(self, race_id):
        window = ctk.CTkToplevel()
        window.title('Информация о заезде')
        window.geometry('400x500')
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
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._show_hippodrome_info(race['info'][3])).grid(row=2, column=1, pady=10, sticky='ew')
        scrollable_frame = ctk.CTkScrollableFrame(window, height=300)
        scrollable_frame.grid(row=3, column=0, rowspan=4, columnspan=2, sticky='ew')
        for result in race['results']:
            RaceResultFrame(scrollable_frame,
                            result,
                            self._show_jockey_info,
                            self._show_horse_info,
                            self._delete_race_result).pack(padx=10, pady=10)
        ctk.CTkButton(window,
                      text='Удалить заезд',
                      fg_color='maroon',
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._delete_race(race_id, window)).grid(row=7, column=1, sticky='ew')
        result_adding_button = ctk.CTkButton(window,
                      text='Добавить результат',
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._show_race_result_adding_window(race_id, window))
        result_adding_button.grid(row=7, column=0, sticky='ew')
        if not self._db.get_all_horses() or not self._db.get_all_jockeys():
            result_adding_button.configure(state=DISABLED)

    def _show_jockey_info(self, jockey_id):
        window = ctk.CTkToplevel()
        window.title('Информация о жокее')
        window.geometry('400x500')
        window.grid_anchor('n')

        jockey = {
            'info': self._db.get_jockey(jockey_id)[0],    
            'races': self._db.get_jockeys_races(jockey_id)
        }    

        LabelWithBg(window, text='Имя:',font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Возраст:',font=ctk.CTkFont(size=18)).grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Адрес:',font=ctk.CTkFont(size=18)).grid(row=2, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Рейтинг:',font=ctk.CTkFont(size=18)).grid(row=3, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Заезды, в которых учавствовал:',font=ctk.CTkFont(size=18)).grid(row=4, column=0, pady=10, padx=10, sticky='ew', columnspan=2)

        LabelWithBg(window, text=jockey['info'][0],font=ctk.CTkFont(size=18)).grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=jockey['info'][1],font=ctk.CTkFont(size=18)).grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=jockey['info'][2],font=ctk.CTkFont(size=18)).grid(row=2, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=jockey['info'][3],font=ctk.CTkFont(size=18)).grid(row=3, column=1, pady=10, padx=10, sticky='ew')

        scrollable_frame = ctk.CTkScrollableFrame(window)
        scrollable_frame.grid(row=5, column=0, rowspan=3, columnspan=2, sticky='ew')
        for race in jockey['races']:
            ArgumentSendButton(scrollable_frame,
                               self._show_race_info,
                               text=race[1],
                               arg=race[0]).pack(padx=10, pady=10, fill='x')

        ctk.CTkButton(window,
                      text='Удалить жокея',
                      fg_color='maroon',
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._delete_jockey(jockey_id, window)).grid(row=8, column=0, columnspan=2, sticky='ew')

    def _show_hippodrome_info(self, hippodrome_id):
        window = ctk.CTkToplevel()
        window.title('Информация об ипподроме')
        window.geometry('400x350')
        window.grid_anchor('n')

        hippodrome = {
            'info': self._db.get_hippodrome(hippodrome_id)[0],    
            'races': self._db.get_hippodrome_races(hippodrome_id)
        }    


        LabelWithBg(window, text='Название:',font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Заезды на данном ипподроме:',font=ctk.CTkFont(size=18)).grid(row=1, column=0, pady=10, padx=10, sticky='ew', columnspan=2)

        LabelWithBg(window, text=hippodrome['info'][0],font=ctk.CTkFont(size=18)).grid(row=0, column=1, pady=10, padx=10, sticky='ew')

        scrollable_frame = ctk.CTkScrollableFrame(window)
        scrollable_frame.grid(row=2, column=0, rowspan=3, columnspan=2, sticky='ew')
        for race in hippodrome['races']:
            ArgumentSendButton(scrollable_frame,
                               self._show_race_info,
                               text=race[1],
                               arg=race[0]).pack(padx=10, pady=10, fill='x')
        ctk.CTkButton(window,
                      text='Удалить ипподром',
                      fg_color='maroon',
                      command=lambda: self._delete_hippodrome(hippodrome_id, window)).grid(row=5, column=0, columnspan=2, sticky='ew')

    def _show_owner_info(self, owner_id):
        window = ctk.CTkToplevel()
        window.title('Информация о владельце')
        window.geometry('400x500')
        window.grid_anchor('n')

        owner = {
            'info': self._db.get_owner(owner_id)[0],    
            'horses': self._db.get_owner_horses(owner_id)
        }    


        LabelWithBg(window, text='Имя:',font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Адрес:',font=ctk.CTkFont(size=18)).grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Телефон:',font=ctk.CTkFont(size=18)).grid(row=2, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Лошади:',font=ctk.CTkFont(size=18)).grid(row=3, column=0, pady=10, padx=10, sticky='ew', columnspan=2)

        LabelWithBg(window, text=owner['info'][0],font=ctk.CTkFont(size=18)).grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=owner['info'][1],font=ctk.CTkFont(size=18)).grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=owner['info'][2],font=ctk.CTkFont(size=18)).grid(row=2, column=1, pady=10, padx=10, sticky='ew')

        scrollable_frame = ctk.CTkScrollableFrame(window)
        scrollable_frame.grid(row=4, column=0, rowspan=3, columnspan=2, sticky='ew')
        ctk.CTkButton(window,
                      text='Удалить владельца',
                      fg_color='maroon',
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._delete_owner(owner_id, window)).grid(row=7, column=1)
        ctk.CTkButton(window,
                      text='Добавить лошадь',
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._show_horse_adding_window(owner_id, window)).grid(row=7, column=0)
        
        for horse in owner['horses']:
            ArgumentSendButton(scrollable_frame,
                               self._show_horse_info,
                               text=horse[1],
                               arg=horse[0]).pack(padx=10, pady=10, fill='x')

    def _show_horse_info(self, horse_id):
        window = ctk.CTkToplevel()
        window.title('Информация о лошади')
        window.geometry('400x500')
        window.grid_anchor('n')

        horse = {
            'info': self._db.get_horse(horse_id)[0],    
            'races': self._db.get_races_with_horse(horse_id)
        }    


        LabelWithBg(window, text='Имя:',font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Возраст:',font=ctk.CTkFont(size=18)).grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Пол:',font=ctk.CTkFont(size=18)).grid(row=2, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Владелец:',font=ctk.CTkFont(size=18)).grid(row=3, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Заезды, в которых участвовала:',font=ctk.CTkFont(size=18)).grid(row=4, column=0, pady=10, padx=10, sticky='ew', columnspan=2)

        LabelWithBg(window, text=horse['info'][0],font=ctk.CTkFont(size=18)).grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=horse['info'][1],font=ctk.CTkFont(size=18)).grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=horse['info'][2],font=ctk.CTkFont(size=18)).grid(row=2, column=1, pady=10, padx=10, sticky='ew')
        ctk.CTkButton(window,
                      text=horse['info'][3],
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._show_owner_info(horse['info'][4])).grid(row=3, column=1, pady=10, padx=10, sticky='ew')

        scrollable_frame = ctk.CTkScrollableFrame(window)
        scrollable_frame.grid(row=5, column=0, rowspan=3, columnspan=2, sticky='ew')
        for race in horse['races']:
            ArgumentSendButton(scrollable_frame,
                               self._show_race_info,
                               text=race[1],
                               arg=race[0]).pack(padx=10, pady=10, fill='x')
        ctk.CTkButton(window,
                      text='Удалить лошадь',
                      fg_color='maroon',
                      command=lambda: self._delete_horse(horse_id, window)).grid(row=8, column=0, columnspan=2, sticky='ew')

    def _show_race_result_adding_window(self, race_id, race_info_window):
        window = ctk.CTkToplevel()
        window.title('Добавление резульата')
        window.geometry('500x300')

        jockeys = [f'{x[0]} - {x[1]}' for x in self._db.get_jockeys_that_not_in_race(race_id)]
        horses = [f'{x[0]} - {x[1]}' for x in self._db.get_horses_that_not_in_race(race_id)]

        if not jockeys or not horses:
            window.destroy()
            App.show_message('Для добавления результата заезда в БД должны присутствовать лошади и жокеи.')
            return

        jockey_choose = ctk.CTkOptionMenu(window,
                                  width=400,
                                  values=jockeys)
        horse_choose = ctk.CTkOptionMenu(window,
                                  width=400,
                                  values=horses)
        place_entry = ctk.CTkEntry(window,
                                  placeholder_text='Место',
                                  width=400,
                                  corner_radius=0)
        time_entry = ctk.CTkEntry(window,
                                  placeholder_text='Время',
                                  width=400,
                                  corner_radius=0)

        jockey_choose.pack(padx=10, pady=10)
        horse_choose.pack(padx=10, pady=10)
        place_entry.pack(padx=10, pady=10)
        time_entry.pack(padx=10, pady=10)
        ctk.CTkButton(window,
                      text='Добавить',
                      command=lambda: self._add_race_result(race_result_data={
                                'jockey_id': jockey_choose.get().split('-')[0],
                                'horse_id': horse_choose.get().split('-')[0],
                                'result_place': place_entry.get(),
                                'result_time': time_entry.get()
                                },
                      creation_window=window,
                      race_info_window=race_info_window,
                      race_id=race_id))\
                        .pack(padx=10, pady=10)

    def _add_race(self, race_data, window):
        try:
            race_id = self._db.create_race(
                race_data['name'],
                race_data['date'],
                race_data['hippodrome_id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            window.destroy()
            ArgumentSendButton(self._races_frame,
                          text=race_data['name'].strip(),
                          command=self._show_race_info,
                          arg=race_id).pack(padx=10,pady=10)

    def _add_race_result(self,
                         race_id,
                         race_result_data,
                         creation_window,
                         race_info_window):
        try:
            self._db.create_race_result(
                race_result_data['result_place'],
                race_result_data['result_time'],
                race_id,
                race_result_data['horse_id'],
                race_result_data['jockey_id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            race_info_window.destroy()
            self._show_race_info(race_id)

    def _add_owner(self,
                   owner_data,
                   creation_window):
        try:
            owner_id = self._db.create_owner(
                owner_data['name'],
                owner_data['telephone'],
                owner_data['address']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            ArgumentSendButton(self._owners_frame,
                          text=owner_data['name'].strip().lower().capitalize(),
                          command=self._show_owner_info,
                          arg=owner_id).pack(padx=10, pady=10)
            self._toggle_horse_adding_button_activity()

    def _add_horse(self,
                   horse_data,
                   creation_window,
                   owner_info_window = None):
        try:
            horse_id = self._db.create_horse(
                horse_data['name'],
                horse_data['age'],
                horse_data['gender'],
                horse_data['owner_id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            ctk.CTkButton(self._horses_frame,
                          text=horse_data['name'].strip().lower().capitalize(),
                          command=lambda: self._show_horse_info(horse_id)).pack(padx=10, pady=10)
            if owner_info_window is not None:
                owner_info_window.destroy()
                self._show_owner_info(horse_data['owner_id'])

    def _add_hippodrome(self, name, creation_window):
        try:
            hippodrome_id = self._db.create_hippodrome(name)
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            ArgumentSendButton(self._hippodromes_frame,
                               text=name.strip().lower().capitalize(),
                               command=self._show_hippodrome_info,
                               arg=hippodrome_id).pack(padx=10, pady=10)
            self._toggle_race_adding_button_activity()

    def _add_jockey(self, jockey_data, creation_window):
        try:
            jockey_id = self._db.create_jockey(
                jockey_data['name'],
                jockey_data['age'],
                jockey_data['address'],
                jockey_data['rating']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            ArgumentSendButton(self._jockeys_frame,
                               text=jockey_data['name'].strip().lower().capitalize(),
                               command=self._show_jockey_info,
                               arg=jockey_id).pack(padx=10, pady=10)

    def _delete_race_result(self, race_result_id, race_result_frame):
        self._db.delete_race_result(race_result_id)
        race_result_frame.destroy()

    def _delete_race(self, race_id, race_info_window):
        self._db.delete_race(race_id)
        for button in self._races_frame.winfo_children():
            if button._arg == race_id:
                button.destroy()
                break
        race_info_window.destroy()

    def _delete_hippodrome(self, hippodrome_id, hippodrome_info_window):
        hippodrome_races = self._db.get_hippodrome_races(hippodrome_id)
        for button in self._races_frame.winfo_children():
            if any(button._arg in x for x in hippodrome_races):
                button.destroy()
        self._db.delete_hippodrome(hippodrome_id)
        for button in self._hippodromes_frame.winfo_children():
            if button._arg == hippodrome_id:
                button.destroy()
                break
        hippodrome_info_window.destroy()
        self._toggle_race_adding_button_activity()

    def _delete_jockey(self, joceky_id, jockey_info_window):
        self._db.delete_jockey(joceky_id)
        for button in self._jockeys_frame.winfo_children():
            if button._arg == joceky_id:
                button.destroy()
                break
        jockey_info_window.destroy()

    def _delete_horse(self, horse_id, horse_info_window):
        self._db.delete_horse(horse_id)
        for button in self._horses_frame.winfo_children():
            if button._arg == horse_id:
                button.destroy()
                break
        horse_info_window.destroy()

    def _delete_owner(self, owner_id, owner_info_window):
        owner_horses = self._db.get_owner_horses(owner_id)
        for button in self._horses_frame.winfo_children():
            if any(button._arg in x for x in owner_horses):
                button.destroy()
        self._db.delete_owner(owner_id)
        for button in self._owners_frame.winfo_children():
            if button._arg == owner_id:
                button.destroy()
                break
        owner_info_window.destroy()
        self._toggle_horse_adding_button_activity()

    def _toggle_horse_adding_button_activity(self):
        if not self._db.get_all_owners():
            self._horse_adding_button.configure(state=DISABLED)
        else:
            self._horse_adding_button.configure(state=NORMAL)

    def _toggle_race_adding_button_activity(self):
        if not self._db.get_all_hippodromes():
            self._race_adding_button.configure(state=DISABLED)
        else:
            self._race_adding_button.configure(state=NORMAL)

    @staticmethod
    def show_message(message: str) -> None:
        """
        Отрисовка окна с указанными сообщением и заголовком.

        Args:
            message: str - сообщение для отображение.
        """
        window = ctk.CTkToplevel()
        window.title('Ошибка')
        window.geometry('650x200')
        ctk.CTkLabel(window, text=message).place(relx=0.5, rely=0.5, anchor='center')

    def run(self):
        self._fill_race_frame()
        self._fill_jockeys_frame()
        self._fill_hippodromes_frame()
        self._fill_owners_frame()
        self._fill_horses_frame()

        self._toggle_horse_adding_button_activity()
        self._toggle_race_adding_button_activity()

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
                         corner_radius=7,
                         font=font if font is not None else ctk.CTkFont(size=20))


class RaceResultFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 race_result,
                 show_jockey_method,
                 show_horse_method,
                 delete_race_result_method):
        super().__init__(master, fg_color=("gray80", "gray40"))
        LabelWithBg(self, text='Жокей:',font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(self, text='Лошадь:',font=ctk.CTkFont(size=18)).grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(self, text='Место:',font=ctk.CTkFont(size=18)).grid(row=2, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(self, text='Времся:',font=ctk.CTkFont(size=18)).grid(row=3, column=0, pady=10, padx=10, sticky='ew')

        ctk.CTkButton(self,
                      text=race_result[1],
                      font=ctk.CTkFont(size=18),
                      command=lambda: show_jockey_method(race_result[5])).grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        ctk.CTkButton(self,
                    text=race_result[2],
                    font=ctk.CTkFont(size=18),
                    command=lambda: show_horse_method(race_result[6])).grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(self, text=race_result[3],font=ctk.CTkFont(size=18)).grid(row=2, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(self, text=race_result[4],font=ctk.CTkFont(size=18)).grid(row=3, column=1, pady=10, padx=10, sticky='ew')
        ctk.CTkButton(self,
                      text='Удалить',
                      font=ctk.CTkFont(size=18),
                      fg_color='maroon',
                      command=lambda: delete_race_result_method(race_result[0], self)).grid(row=4, column=0, pady=10, padx=10, sticky='ew', columnspan=2)
