import customtkinter as ctk
from tkinter import DISABLED, NORMAL, END
from app.db import DB

ctk.set_appearance_mode('dark')


class App:
    """Класс, описывающий работу приложения через графический интерфейс"""
    def __init__(self, db: DB) -> None:
        """
        Инициализация экземпляра класса.

        :param db: объект класса, реализующего работу с БД
        :type db: DB
        """
        self._db = db
        self._main_window = ctk.CTk()
        self._main_window.geometry('820x600')
        self._main_window.title('Заезды')

        self._tab_view = ctk.CTkTabview(self._main_window, 800, 500)
        races_tab = self._tab_view.add('Заезды')
        jockeys_tab = self._tab_view.add('Жокеи')
        hippodromes_tab = self._tab_view.add('Ипподромы')
        owners_tab = self._tab_view.add('Владельцы')
        horses_tab = self._tab_view.add('Лошади')

        self._races_frame = ctk.CTkScrollableFrame(races_tab, 780, 480)
        self._races_frame.grid(row=0, column=0, columnspan=5, sticky='ew')
        self._race_adding_button = ctk.CTkButton(races_tab,
                                                 text='Добавить заезд',
                                                 command=self._show_race_adding_window)
        self._race_adding_button.grid(row=1, column=0, columnspan=5, sticky='ew')

        self._races_filter_entry_from = ctk.CTkEntry(races_tab,
                                                     corner_radius=0,
                                                     width=100,
                                                     placeholder_text='От (YYYY-MM-DD)')
        self._races_filter_entry_to = ctk.CTkEntry(races_tab,
                                                   corner_radius=0,
                                                   width=100,
                                                   placeholder_text='До (YYYY-MM-DD)')
        self._races_filter_entry_from.grid(row=2, column=1, sticky='ew')
        self._races_filter_entry_to.grid(row=2, column=2, sticky='ew')
        self._races_filter_checkbox = ctk.CTkCheckBox(races_tab,
                                                      text='Фильтровать по дате',
                                                      command=self._toggle_races_filter_widgets)
        self._races_filter_checkbox.grid(row=2, column=0, sticky='ew')
        self._races_filter_reset_button = ctk.CTkButton(races_tab,
                                                        text='Сбросить',
                                                        fg_color='maroon',
                                                        command=self._reset_races_filters)
        self._races_filter_reset_button.grid(row=2, column=4, sticky='ew')
        self._races_filter_apply_button = ctk.CTkButton(races_tab,
                                                        text='Прменить',
                                                        command=self._apply_races_filters)
        self._races_filter_apply_button.grid(row=2, column=3, sticky='ew')


        self._jockeys_frame = ctk.CTkScrollableFrame(jockeys_tab, 780, 480)
        self._jockeys_frame.grid(row=0, column=0, columnspan=5, sticky='ew')
        ctk.CTkButton(
            jockeys_tab,
            text='Добавить жокея',
            command=self._show_jockey_adding_window
        ).grid(row=1, column=0, columnspan=5, sticky='ew')

        self._jockeys_filter_entry_from = ctk.CTkEntry(jockeys_tab,
                                                     corner_radius=0,
                                                     width=100,
                                                     placeholder_text='От')
        self._jockeys_filter_entry_to = ctk.CTkEntry(jockeys_tab,
                                                   corner_radius=0,
                                                   width=100,
                                                   placeholder_text='До')
        self._jockeys_filter_entry_from.grid(row=2, column=1, sticky='ew')
        self._jockeys_filter_entry_to.grid(row=2, column=2, sticky='ew')
        self._jockeys_filter_checkbox = ctk.CTkCheckBox(jockeys_tab,
                                                      text='Фильтровать по рейтингу',
                                                      command=self._toggle_jockeys_filter_widgets)
        self._jockeys_filter_checkbox.grid(row=2, column=0, sticky='ew')
        self._jockeys_filter_reset_button = ctk.CTkButton(jockeys_tab,
                                                        text='Сбросить',
                                                        fg_color='maroon',
                                                        command=self._reset_jockeys_filters)
        self._jockeys_filter_reset_button.grid(row=2, column=4, sticky='ew')
        self._jockeys_filter_apply_button = ctk.CTkButton(jockeys_tab,
                                                        text='Прменить',
                                                        command=self._apply_jockeys_filters)
        self._jockeys_filter_apply_button.grid(row=2, column=3, sticky='ew')


        self._hippodromes_frame = ctk.CTkScrollableFrame(hippodromes_tab, 780, 480)
        self._hippodromes_frame.grid(row=0, column=0, columnspan=5, sticky='ew')
        ctk.CTkButton(
            hippodromes_tab,
            text='Добавить ипподром',
            command=self._show_hippodrome_adding_window
        ).grid(row=1, column=0, columnspan=5, sticky='ew')

        self._hippodromes_filter_entry_from = ctk.CTkEntry(hippodromes_tab,
                                                           corner_radius=0,
                                                           width=100,
                                                           placeholder_text='От')
        self._hippodromes_filter_entry_to = ctk.CTkEntry(hippodromes_tab,
                                                         corner_radius=0,
                                                         width=100,
                                                         placeholder_text='До')
        self._hippodromes_filter_entry_from.grid(row=2, column=1, sticky='ew')
        self._hippodromes_filter_entry_to.grid(row=2, column=2, sticky='ew')
        self._hippodromes_filter_checkbox = ctk.CTkCheckBox(hippodromes_tab,
                                                            text='Фильтровать по количеству заездов',
                                                            command=self._toggle_hippodromes_filter_widgets)
        self._hippodromes_filter_checkbox.grid(row=2, column=0, sticky='ew')
        self._hippodromes_filter_reset_button = ctk.CTkButton(hippodromes_tab,
                                                              text='Сбросить',
                                                              fg_color='maroon',
                                                              command=self._reset_hippodromes_filters)
        self._hippodromes_filter_reset_button.grid(row=2, column=4, sticky='ew')
        self._hippodromes_filter_apply_button = ctk.CTkButton(hippodromes_tab,
                                                              text='Прменить',
                                                              command=self._apply_hippodromes_filters)
        self._hippodromes_filter_apply_button.grid(row=2, column=3, sticky='ew')


        self._owners_frame = ctk.CTkScrollableFrame(owners_tab, 780, 480)
        self._owners_frame.grid(row=0, column=0, columnspan=5, sticky='ew')
        ctk.CTkButton(
            owners_tab,
            text='Добавить владельца',
            command=self._show_owner_adding_window
        ).grid(row=1, column=0, columnspan=5, sticky='ew')

        self._owners_filter_entry_from = ctk.CTkEntry(owners_tab,
                                                      corner_radius=0,
                                                      width=100,
                                                      placeholder_text='От')
        self._owners_filter_entry_to = ctk.CTkEntry(owners_tab,
                                                    corner_radius=0,
                                                    width=100,
                                                    placeholder_text='До')
        self._owners_filter_entry_from.grid(row=2, column=1, sticky='ew')
        self._owners_filter_entry_to.grid(row=2, column=2, sticky='ew')
        self._owners_filter_checkbox = ctk.CTkCheckBox(owners_tab,
                                                       text='Фильтровать по количеству коней',
                                                       command=self._toggle_owners_filter_widgets)
        self._owners_filter_checkbox.grid(row=2, column=0, sticky='ew')
        self._owners_filter_reset_button = ctk.CTkButton(owners_tab,
                                                         text='Сбросить',
                                                         fg_color='maroon',
                                                         command=self._reset_owners_filters)
        self._owners_filter_reset_button.grid(row=2, column=4, sticky='ew')
        self._owners_filter_apply_button = ctk.CTkButton(owners_tab,
                                                         text='Прменить',
                                                         command=self._apply_owners_filters)
        self._owners_filter_apply_button.grid(row=2, column=3, sticky='ew')


        self._horses_frame = ctk.CTkScrollableFrame(horses_tab, 780, 480)
        self._horses_frame.grid(row=0, column=0, columnspan=5, sticky='ew')
        self._horse_adding_button = ctk.CTkButton(horses_tab,
                                                  text='Добавить лошадь',
                                                  command=self._show_horse_adding_window)
        self._horse_adding_button.grid(row=1, column=0, columnspan=5, sticky='ew')

        self._horses_filter_entry_from = ctk.CTkEntry(horses_tab,
                                                      corner_radius=0,
                                                      width=100,
                                                      placeholder_text='От')
        self._horses_filter_entry_to = ctk.CTkEntry(horses_tab,
                                                    corner_radius=0,
                                                    width=100,
                                                    placeholder_text='До')
        self._horses_filter_entry_from.grid(row=2, column=1, sticky='ew')
        self._horses_filter_entry_to.grid(row=2, column=2, sticky='ew')
        self._horses_filter_checkbox = ctk.CTkCheckBox(horses_tab,
                                                       text='Фильтровать по возрасту',
                                                       command=self._toggle_horses_filter_widgets)
        self._horses_filter_checkbox.grid(row=2, column=0, sticky='ew')
        self._horses_filter_reset_button = ctk.CTkButton(horses_tab,
                                                         text='Сбросить',
                                                         fg_color='maroon',
                                                         command=self._reset_horses_filters)
        self._horses_filter_reset_button.grid(row=2, column=4, sticky='ew')
        self._horses_filter_apply_button = ctk.CTkButton(horses_tab,
                                                         text='Прменить',
                                                         command=self._apply_horses_filters)
        self._horses_filter_apply_button.grid(row=2, column=3, sticky='ew')


        self._tab_view.pack()

    @staticmethod
    def _delete_children_widgets(parent_widget: ctk.CTkBaseClass) -> None:
        """
        Удаляет все дочерние виджеты у родительскоего виджета.

        :param parent_widget: родительский виджет
        :type parent_widget: CTkBaseClass 
        """
        for child in parent_widget.winfo_children():
            child.destroy()

    def _toggle_races_filter_widgets(self) -> None:
        """
        Меняет активность виджетов, отвечающих 
        за фильтрацию страницы с заездами.
        """
        if self._races_filter_checkbox.get():
            self._races_filter_entry_from.configure(state=NORMAL)
            self._races_filter_entry_to.configure(state=NORMAL)
            self._races_filter_reset_button.configure(state=NORMAL)
            self._races_filter_apply_button.configure(state=NORMAL)
        else:
            self._races_filter_entry_from.configure(state=DISABLED)
            self._races_filter_entry_to.configure(state=DISABLED)
            self._races_filter_reset_button.configure(state=DISABLED)
            self._races_filter_apply_button.configure(state=DISABLED)

    def _toggle_jockeys_filter_widgets(self) -> None:
        """
        Меняет активность виджетов, отвечающих 
        за фильтрацию страницы с жокеями.
        """
        if self._jockeys_filter_checkbox.get():
            self._jockeys_filter_entry_from.configure(state=NORMAL)
            self._jockeys_filter_entry_to.configure(state=NORMAL)
            self._jockeys_filter_reset_button.configure(state=NORMAL)
            self._jockeys_filter_apply_button.configure(state=NORMAL)
        else:
            self._jockeys_filter_entry_from.configure(state=DISABLED)
            self._jockeys_filter_entry_to.configure(state=DISABLED)
            self._jockeys_filter_reset_button.configure(state=DISABLED)
            self._jockeys_filter_apply_button.configure(state=DISABLED)

    def _toggle_hippodromes_filter_widgets(self) -> None:
        """
        Меняет активность виджетов, отвечающих 
        за фильтрацию страницы с ипподромами.
        """
        if self._hippodromes_filter_checkbox.get():
            self._hippodromes_filter_entry_from.configure(state=NORMAL)
            self._hippodromes_filter_entry_to.configure(state=NORMAL)
            self._hippodromes_filter_reset_button.configure(state=NORMAL)
            self._hippodromes_filter_apply_button.configure(state=NORMAL)
        else:
            self._hippodromes_filter_entry_from.configure(state=DISABLED)
            self._hippodromes_filter_entry_to.configure(state=DISABLED)
            self._hippodromes_filter_reset_button.configure(state=DISABLED)
            self._hippodromes_filter_apply_button.configure(state=DISABLED)

    def _toggle_owners_filter_widgets(self) -> None:
        """
        Меняет активность виджетов, отвечающих 
        за фильтрацию страницы с владельцами.
        """
        if self._owners_filter_checkbox.get():
            self._owners_filter_entry_from.configure(state=NORMAL)
            self._owners_filter_entry_to.configure(state=NORMAL)
            self._owners_filter_reset_button.configure(state=NORMAL)
            self._owners_filter_apply_button.configure(state=NORMAL)
        else:
            self._owners_filter_entry_from.configure(state=DISABLED)
            self._owners_filter_entry_to.configure(state=DISABLED)
            self._owners_filter_reset_button.configure(state=DISABLED)
            self._owners_filter_apply_button.configure(state=DISABLED)

    def _toggle_horses_filter_widgets(self) -> None:
        """
        Меняет активность виджетов, отвечающих 
        за фильтрацию страницы с лошадьми.
        """
        if self._horses_filter_checkbox.get():
            self._horses_filter_entry_from.configure(state=NORMAL)
            self._horses_filter_entry_to.configure(state=NORMAL)
            self._horses_filter_reset_button.configure(state=NORMAL)
            self._horses_filter_apply_button.configure(state=NORMAL)
        else:
            self._horses_filter_entry_from.configure(state=DISABLED)
            self._horses_filter_entry_to.configure(state=DISABLED)
            self._horses_filter_reset_button.configure(state=DISABLED)
            self._horses_filter_apply_button.configure(state=DISABLED)

    def _apply_races_filters(self) -> None:
        """Применяет фильтр для заездов и отображает новую инофрмацию."""
        try:
            races = self._db.get_races_in_date_range(
                self._races_filter_entry_from.get(),
                self._races_filter_entry_to.get()
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            App._delete_children_widgets(self._races_frame)
            self._fill_races_frame(races)

    def _apply_jockeys_filters(self) -> None:
        """Применяет жокеев для заездов и отображает новую инофрмацию."""
        try:
            jockeys = self._db.get_jockeys_with_rating_in_range(
                self._jockeys_filter_entry_from.get(),
                self._jockeys_filter_entry_to.get()
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            App._delete_children_widgets(self._jockeys_frame)
            self._fill_jockeys_frame(jockeys)

    def _apply_hippodromes_filters(self) -> None:
        """Применяет фильтр для ипподромов и отображает новую информацию."""
        try:
            hippodromes = self._db.get_hippodrome_with_races_in_range(
                self._hippodromes_filter_entry_from.get(),
                self._hippodromes_filter_entry_to.get()
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            App._delete_children_widgets(self._hippodromes_frame)
            self._fill_hippodromes_frame(hippodromes)

    def _apply_owners_filters(self) -> None:
        """Применяет фильтр для владельцев и отображает новую информацию."""
        try:
            owners = self._db.get_owners_with_horses_count_in_range(
                self._owners_filter_entry_from.get(),
                self._owners_filter_entry_to.get()
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            App._delete_children_widgets(self._owners_frame)
            self._fill_owners_frame(owners)

    def _apply_horses_filters(self) -> None:
        """Применяет фильтр для лошадей и отображает новую информацию."""
        try:
            horses = self._db.get_horses_with_age_in_range(
                self._horses_filter_entry_from.get(),
                self._horses_filter_entry_to.get()
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            App._delete_children_widgets(self._horses_frame)
            self._fill_horses_frame(horses)

    def _reset_races_filters(self) -> None:
        """Сбрасывает фильтрацию со страницы с заздами."""
        self._races_filter_checkbox.deselect()
        self._races_filter_entry_from.delete(0, END)
        self._races_filter_entry_from.configure(placeholder_text='От (YYYY-MM-DD)')
        self._races_filter_entry_to.delete(0, END)
        self._races_filter_entry_to.configure(placeholder_text='До (YYYY-MM-DD)')
        self._toggle_races_filter_widgets()

        App._delete_children_widgets(self._races_frame)
        self._fill_races_frame()

    def _reset_jockeys_filters(self) -> None:
        """Сбрасывает фильтрацию со страницы с жокеями."""
        self._jockeys_filter_checkbox.deselect()
        self._jockeys_filter_entry_from.delete(0, END)
        self._jockeys_filter_entry_from.configure(placeholder_text='От')
        self._jockeys_filter_entry_to.delete(0, END)
        self._jockeys_filter_entry_to.configure(placeholder_text='До')
        self._toggle_jockeys_filter_widgets()

        App._delete_children_widgets(self._jockeys_frame)
        self._fill_jockeys_frame()

    def _reset_hippodromes_filters(self) -> None:
        """Сбрасывает фильтрацию со страницы с ипподромами."""
        self._hippodromes_filter_checkbox.deselect()
        self._hippodromes_filter_entry_from.delete(0, END)
        self._hippodromes_filter_entry_from.configure(placeholder_text='От')
        self._hippodromes_filter_entry_to.delete(0, END)
        self._hippodromes_filter_entry_to.configure(placeholder_text='До')
        self._toggle_hippodromes_filter_widgets()

        App._delete_children_widgets(self._hippodromes_frame)
        self._fill_hippodromes_frame()

    def _reset_owners_filters(self) -> None:
        """Сбрасывает фильтрацию со страницы с владельцами."""
        self._owners_filter_checkbox.deselect()
        self._owners_filter_entry_from.delete(0, END)
        self._owners_filter_entry_from.configure(placeholder_text='От')
        self._owners_filter_entry_to.delete(0, END)
        self._owners_filter_entry_to.configure(placeholder_text='До')
        self._toggle_owners_filter_widgets()

        App._delete_children_widgets(self._owners_frame)
        self._fill_owners_frame()

    def _reset_horses_filters(self) -> None:
        """Сбрасывает фильтрацию со страницы с лошадьми."""
        self._horses_filter_checkbox.deselect()
        self._horses_filter_entry_from.delete(0, END)
        self._horses_filter_entry_from.configure(placeholder_text='От')
        self._horses_filter_entry_to.delete(0, END)
        self._horses_filter_entry_to.configure(placeholder_text='До')
        self._toggle_horses_filter_widgets()

        App._delete_children_widgets(self._horses_frame)
        self._fill_horses_frame()

    def _fill_races_frame(self, races: list[tuple] = None) -> None:
        """
        Заполняет страницу с заездами полученными данными
        или всеми записями из БД, если список не был получен.
        :param races: список с данными о заездах (default None).
        :type races: list[tuple]
        """
        if races is None:
            races = self._db.get_all_races()
        for race in races:
            ArgumentSendButton(
                self._races_frame,
                text=race[1],
                command=self._show_race_info,
                arg=race[0]
            ).pack(padx=10,pady=10)

    def _fill_jockeys_frame(self, jockeys: list[tuple] = None) -> None:
        """
        Заполняет страницу с жокеями полученными данными
        или всеми записями из БД, если список не был получен.
        :param jockeys: список с данными о жокеях (default None).
        :type jockeys: list[tuple]
        """
        if jockeys is None:
            jockeys = self._db.get_all_jockeys()
        for jockey in jockeys:
            ArgumentSendButton(
                self._jockeys_frame,
                text=jockey[1],
                command=self._show_jockey_info,
                arg=jockey[0]
            ).pack(padx=10,pady=10)

    def _fill_hippodromes_frame(self, hippodromes: list[tuple] = None) -> None:
        """
        Заполняет страницу с ипподромами полученными данными
        или всеми записями из БД, если список не был получен.
        :param hippodromes: список с данными о ипподромах (default None).
        :type hippodromes: list[tuple]
        """
        if hippodromes is None:
            hippodromes = self._db.get_all_hippodromes()
        for hippodrome in hippodromes:
            ArgumentSendButton(
                self._hippodromes_frame,
                text=hippodrome[1],
                command=self._show_hippodrome_info,
                arg=hippodrome[0]
            ).pack(padx=10,pady=10)

    def _fill_owners_frame(self, owners: list[tuple] = None) -> None:
        """
        Заполняет страницу с владельцами полученными данными
        или всеми записями из БД, если список не был получен.
        :param owners: список с данными о владельцах (default None).
        :type owners: list[tuple]
        """
        if owners is None:
            owners = self._db.get_all_owners()
        for owner in owners:
            ArgumentSendButton(
                self._owners_frame,
                text=owner[1],
                command=self._show_owner_info,
                arg=owner[0]
            ).pack(padx=10,pady=10)

    def _fill_horses_frame(self, horses: list[tuple] = None) -> None:
        """
        Заполняет страницу с лошадях полученными данными
        или всеми записями из БД, если список не был получен.
        :param horses: список с данными о конях (default None).
        :type horses: list[tuple]
        """
        if horses is None:
            horses = self._db.get_all_horses()
        for horse in horses:
            ArgumentSendButton(
                self._horses_frame,
                text=horse[1],
                command=self._show_horse_info,
                arg=horse[0]
            ).pack(padx=10,pady=10)

    def _show_race_adding_window(self) -> None:
        """Отрисовывает окно добавления нового заезда"""
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
        ctk.CTkButton(
            window,
            text='Добавить',
            command=lambda: self._add_race({
                    'name': name_entry.get(),
                    'date': date_entry.get(),
                    'hippodrome_id': hippodromes[hippodrome_choose.get()]
                    }, window)
        ).pack(padx=10, pady=10)

    def _show_race_editing_window(self,
                                  race_id: int,
                                  race_info_window: ctk.CTkToplevel) -> None:
        """
        Отрисовывает окно редактирования заезда.
        
        :param race_id: id заезда
        :type race_id: int
        :param race_info_window: окно, в котором нужно
                                 обновить информацию
        :type race_info_window: CTkToplevel
        """
        window = ctk.CTkToplevel()
        window.title('Редактирование заезда')
        window.geometry('500x300')

        race_info = self._db.get_race(race_id)
        race_name = ctk.StringVar(value=race_info[0][0])
        race_date = ctk.StringVar(value=race_info[0][1])
        race_hippodrome = ctk.StringVar(value=race_info[0][2])
        hippodromes = {x[1]:x[0] for x in self._db.get_all_hippodromes()}

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Название',
                                  width=400,
                                  corner_radius=0,
                                  textvariable=race_name)
        date_entry = ctk.CTkEntry(window,
                                  placeholder_text='Дата (YYYY-MM-DD)',
                                  width=400,
                                  corner_radius=0,
                                  textvariable=race_date)
        hippodrome_choose = ctk.CTkOptionMenu(window,
                                              width=400,
                                              values=list(hippodromes.keys()),
                                              variable=race_hippodrome)

        name_entry.pack(padx=10, pady=10)
        date_entry.pack(padx=10, pady=10)
        hippodrome_choose.pack(padx=10, pady=10)
        ctk.CTkButton(
            window,
            text='Обновить',
            command=lambda: self._edit_race({
                    'name': name_entry.get(),
                    'date': date_entry.get(),
                    'hippodrome_id': hippodromes[hippodrome_choose.get()],
                    'id': race_id
                    },race_info_window, window)
        ).pack(padx=10, pady=10)

    def _show_race_result_adding_window(self,
                                        race_id: int,
                                        race_info_window: ctk.CTkToplevel) -> None:
        """
        Отрисовывает окно добавления нового результата заезда.

        :param race_id: id заезда для короторого добавляется результат.
        :type race_id: int
        :param race_info_window: окно с информацией о заезде, данные в котором
                                 нужно будет обновить после добавления результата.
        :type race_info_window: CTkToplevel
        """
        window = ctk.CTkToplevel()
        window.title('Добавление результата')
        window.geometry('500x300')

        jockeys = [f'{x[0]} - {x[1]}' for x in self._db.get_jockeys_that_not_in_race(race_id)]
        horses = [f'{x[0]} - {x[1]}' for x in self._db.get_horses_that_not_in_race(race_id)]

        if not jockeys:
            window.destroy()
            App.show_message('В БД нет записей о жокеях, которые не учавствуют в данном заезде.')
            return
        elif not horses:
            window.destroy()
            App.show_message('В БД нет записей о лошадях, которые не учавствуют в данном заезде.')
            return

        jockey_choose = ctk.CTkOptionMenu(window,
                                          width=400,
                                          values=jockeys)
        horse_choose = ctk.CTkOptionMenu(window,
                                         width=400,
                                         values=horses)
        place_entry = ctk.CTkEntry(window,
                                   placeholder_text='Место ([1,20])',
                                   width=400,
                                   corner_radius=0)
        time_entry = ctk.CTkEntry(window,
                                  placeholder_text='Время (в секундах)',
                                  width=400,
                                  corner_radius=0)

        jockey_choose.pack(padx=10, pady=10)
        horse_choose.pack(padx=10, pady=10)
        place_entry.pack(padx=10, pady=10)
        time_entry.pack(padx=10, pady=10)
        ctk.CTkButton(
            window,
            text='Добавить',
            command=lambda: self._add_race_result(race_result_data={
                    'jockey_id': int(jockey_choose.get().split('-')[0]),
                    'horse_id': int(horse_choose.get().split('-')[0]),
                    'result_place': place_entry.get(),
                    'result_time': time_entry.get()
                    },
            creation_window=window,
            race_info_window=race_info_window,
            race_id=race_id)
        ).pack(padx=10, pady=10)

    def _show_owner_adding_window(self) -> None:
        """Отрисовывает окно добавления нового владельца"""
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
        ctk.CTkButton(
            window,
            text='Добавить',
            command=lambda: self._add_owner({
                    'name': name_entry.get(),
                    'telephone': phone_number_entry.get(),
                    'address': address_entry.get()
                    }, window)
        ).pack(padx=10, pady=10)

    def _show_owner_editing_window(self,
                                  owner_id: int,
                                  owner_info_window: ctk.CTkToplevel) -> None:
        """
        Отрисовывает окно редактирования владельца.
        
        :param owner_id: id владельца
        :type owner_id: int
        :param owner_info_window: окно, в котором нужно
                                  обновить информацию
        :type owner_info_window: CTkToplevel
        """
        window = ctk.CTkToplevel()
        window.title('Редактирование владельца')
        window.geometry('500x300')

        owner_info = self._db.get_owner(owner_id)
        owner_name = ctk.StringVar(value=owner_info[0][0])
        owner_address = ctk.StringVar(value=owner_info[0][1])
        owner_phone_number = ctk.StringVar(value=owner_info[0][2])

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Имя',
                                  width=400,
                                  corner_radius=0,
                                  textvariable=owner_name)
        address_entry = ctk.CTkEntry(window,
                                     placeholder_text='Адрес',
                                     width=400,
                                     corner_radius=0,
                                     textvariable=owner_address)
        phone_number_entry = ctk.CTkEntry(window,
                                          placeholder_text='Телефон',
                                          width=400,
                                          corner_radius=0,
                                          textvariable=owner_phone_number)

        name_entry.pack(padx=10, pady=10)
        address_entry.pack(padx=10, pady=10)
        phone_number_entry.pack(padx=10, pady=10)
        ctk.CTkButton(
            window,
            text='Обновить',
            command=lambda: self._edit_owner({'name': owner_name.get(),
                                              'address': owner_address.get(),
                                              'telephone': owner_phone_number.get(),
                                              'id': owner_id},
                                              owner_info_window,
                                              window)
        ).pack(padx=10, pady=10)

    def _show_horse_adding_window(self,
                                  owner_id: int = None,
                                  owner_info_window: ctk.CTkToplevel = None) -> None:
        """
        Отрисовывает окно добавления новой лошади.

        :param owner_id: id владельца, к которому добавлется лошадь
                         (если не указан, то будет отрисован виджет
                          с выбором владельца) (default None)
        :type onwer_id: int
        :param owner_info_window: окно, данные в котором нужно будет обновить
                                  после добавления новой лошади, если
                                  создание вызвано из окна с информацией
                                  о владельце (default None)
        :type owner_info_window: CTkToplevel
        """
        window = ctk.CTkToplevel()
        window.title('Добавление лошади')
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
        ctk.CTkButton(
            window,
            text='Добавить',
            command=lambda: self._add_horse({
                    'name': name_entry.get(),
                    'age': age_entry.get(),
                    'gender': gender_entry.get(),
                    'owner_id': owner_id if owner_id is not None else int(owner_choose.get().split('-')[0])
                    }, window, owner_info_window)
        ).pack(padx=10, pady=10)

    def _show_horse_editing_window(self,
                                   horse_id: int,
                                   horse_info_window: ctk.CTkToplevel) -> None:
        """
        Отрисовывает окно редактирования лошади.

        :param horse_id: id коня
        :type horse_id: int
        :param horse_info_window: окно, в котором нужно
                                  обновить информацию
        :type horse_info_window: CTkToplevel
        :param owner_info_window: окно, данные в котором нужно будет обновить
                                  после добавления новой лошади, если
                                  создание вызвано из окна с информацией
                                  о владельце (default None)
        :type owner_info_window: CTkToplevel
        """
        window = ctk.CTkToplevel()
        window.title('Редактирование лошади')
        window.geometry('500x300')

        horse_info = self._db.get_horse(horse_id)
        horse_name = ctk.StringVar(value=horse_info[0][0])
        horse_age = ctk.StringVar(value=horse_info[0][1])
        horse_gender = ctk.StringVar(value=horse_info[0][2])

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Имя',
                                  width=400,
                                  corner_radius=0,
                                  textvariable=horse_name)
        age_entry = ctk.CTkEntry(window,
                                 placeholder_text='Возраст',
                                 width=400,
                                 corner_radius=0,
                                 textvariable=horse_age)
        gender_entry = ctk.CTkEntry(window,
                                    placeholder_text='Пол (мужской/женский)',
                                    width=400,
                                    corner_radius=0,
                                    textvariable=horse_gender)

        horse_owner = ctk.StringVar(value=f'{horse_info[0][4]} - {horse_info[0][3]}')
        owner_choose = ctk.CTkOptionMenu(window,
                                         width=400,
                                         values=[f'{x[0]} - {x[1]}' for x in self._db.get_all_owners()],
                                         variable=horse_owner)

        name_entry.pack(padx=10, pady=10)
        age_entry.pack(padx=10, pady=10)
        gender_entry.pack(padx=10, pady=10)
        owner_choose.pack(padx=10, pady=10)
            
        ctk.CTkButton(
            window,
            text='Обновить',
            command=lambda: self._edit_horse({
                    'name': horse_name.get(),
                    'age': horse_age.get(),
                    'gender': horse_gender.get(),
                    'owner_id': int(horse_owner.get().split('-')[0]),
                    'id': horse_id
                    },horse_info_window, window)
        ).pack(padx=10, pady=10)

    def _show_jockey_adding_window(self) -> None:
        """Отрисовывает окно добавления нового жокея."""
        window = ctk.CTkToplevel()
        window.title('Добавление жокея')
        window.geometry('500x200')

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

        name_entry.pack(padx=10, pady=10)
        age_entry.pack(padx=10, pady=10)
        address_entry.pack(padx=10, pady=10)
        ctk.CTkButton(
            window,
            text='Добавить',
            command=lambda: self._add_jockey({
                    'name': name_entry.get(),
                    'age': age_entry.get(),
                    'address': address_entry.get()
                    }, window)
        ).pack(padx=10, pady=10)

    def _show_jockey_editing_window(self,
                                    jockey_id: int,
                                    jockey_info_window: ctk.CTkToplevel) -> None:
        """
        Отрисовывает окно редактирования жокея.
        
        :param jockey_id: id жокея
        :type jockey_id: int
        :param jockey_info_window: окно, в котором нужно
                                   обновить информацию
        :type jockey_info_window: CTkToplevel
        """
        window = ctk.CTkToplevel()
        window.title('Редактирование жокея')
        window.geometry('500x200')

        jockey_info = self._db.get_jockey(jockey_id)
        jockey_name = ctk.StringVar(value=jockey_info[0][0])
        jockey_age = ctk.StringVar(value=jockey_info[0][1])
        jockey_address = ctk.StringVar(value=jockey_info[0][2])

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Имя',
                                  width=400,
                                  corner_radius=0,
                                  textvariable=jockey_name)
        age_entry = ctk.CTkEntry(window,
                                 placeholder_text='Возраст',
                                 width=400,
                                 corner_radius=0,
                                 textvariable=jockey_age)
        address_entry = ctk.CTkEntry(window,
                                     placeholder_text='Адрес',
                                     width=400,
                                     corner_radius=0,
                                     textvariable=jockey_address)

        name_entry.pack(padx=10, pady=10)
        age_entry.pack(padx=10, pady=10)
        address_entry.pack(padx=10, pady=10)
        ctk.CTkButton(
            window,
            text='Обновить',
            command=lambda: self._edit_jockey({'name': jockey_name.get(),
                                               'age': jockey_age.get(),
                                               'address': jockey_address.get(),
                                               'id': jockey_id},
                                               jockey_info_window,
                                               window)
        ).pack(padx=10, pady=10)

    def _show_hippodrome_adding_window(self) -> None:
        """Отрисовывает окно добавления нового ипподрома."""
        window = ctk.CTkToplevel()
        window.title('Добавление ипподрома')
        window.geometry('500x150')

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Название',
                                  width=400,
                                  corner_radius=0)
        name_entry.pack(padx=10, pady=10)
        ctk.CTkButton(
            window,
            text='Добавить',
            command=lambda: self._add_hippodrome(name_entry.get(), window)
        ).pack(padx=10, pady=10)

    def _show_hippodrome_editing_window(self,
                                        hippodrome_id: int,
                                        hippodrome_info_window: ctk.CTkToplevel) -> None:
        """
        Отрисовывает окно редактирования ипподрома.
        
        :param hippodrome_id: id ипподрома
        :type hippodrome_id: int
        :param hippodrome_info_window: окно, в котором нужно
                                       обновить информацию
        :type hippodrome_info_window: CTkToplevel
        """
        window = ctk.CTkToplevel()
        window.title('Редактирование ипподрома')
        window.geometry('500x150')

        hippodrome_info = self._db.get_hippodrome(hippodrome_id)
        hippodrome_name = ctk.StringVar(value=hippodrome_info[0][0])

        name_entry = ctk.CTkEntry(window,
                                  placeholder_text='Название',
                                  width=400,
                                  corner_radius=0,
                                  textvariable=hippodrome_name)
        name_entry.pack(padx=10, pady=10)
        ctk.CTkButton(
            window,
            text='Обновить',
            command=lambda: self._edit_hippodrome(hippodrome_name.get(),
                                                  hippodrome_id,
                                                  hippodrome_info_window,
                                                  window)
        ).pack(padx=10, pady=10)

    def _show_race_info(self, race_id: int) -> None:
        """
        Отрисовывает окно с информацией о выбранном заезде.

        :param race_id: id выбранного заезда.
        :type race_id: int
        """
        window = ctk.CTkToplevel()
        window.title('Информация о заезде')
        window.geometry('400x530')
        window.grid_anchor('n')

        race = {
            'info': self._db.get_race(race_id)[0],
            'results': self._db.get_race_results(race_id)
        }

        LabelWithBg(window, text='Название:',font=ctk.CTkFont(size=18)).grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Дата:',font=ctk.CTkFont(size=18)).grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Ипподром:',font=ctk.CTkFont(size=18)).grid(row=2, column=0, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text='Результаты:',font=ctk.CTkFont(size=18)).grid(row=3, column=0, pady=10, padx=10, sticky='ew')

        LabelWithBg(window, text=race['info'][0],font=ctk.CTkFont(size=18)).grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        LabelWithBg(window, text=race['info'][1],font=ctk.CTkFont(size=18)).grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        ctk.CTkButton(
            window,
            text=race['info'][2],
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_hippodrome_info(race['info'][3])
        ).grid(row=2, column=1, pady=10, sticky='ew')

        scrollable_frame = ctk.CTkScrollableFrame(window, height=300, width=300)
        scrollable_frame.grid(row=3, column=0, rowspan=4, columnspan=2, sticky='ew')
        for result in race['results']:
            RaceResultFrame(scrollable_frame,
                            result,
                            self._show_jockey_info,
                            self._show_horse_info,
                            self._delete_race_result).pack(padx=10, pady=10)

        ctk.CTkButton(
            window,
            text='Редактировать',
            fg_color='#bf6c08',
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_race_editing_window(race_id, window)
        ).grid(row=7, column=0, sticky='ew')
        ctk.CTkButton(
            window,
            text='Удалить',
            fg_color='maroon',
            font=ctk.CTkFont(size=18),
            command=lambda: self._delete_race(race_id, window)
        ).grid(row=7, column=1, sticky='ew')

        result_adding_button = ctk.CTkButton(window,
                      text='Добавить результат',
                      font=ctk.CTkFont(size=18),
                      command=lambda: self._show_race_result_adding_window(race_id, window))
        result_adding_button.grid(row=8, column=0, columnspan=2, sticky='ew')

        if not self._db.get_all_horses() or not self._db.get_all_jockeys():
            result_adding_button.configure(state=DISABLED)

    def _show_jockey_info(self, jockey_id: int) -> None:
        """
        Отрисовывает окно с информацией о выбранном жокее.

        :param jockey_id: id выбранного жокея.
        :param jockey_id: int
        """
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
            ArgumentSendButton(
                scrollable_frame,
                self._show_race_info,
                text=race[1],
                arg=race[0]
            ).pack(padx=10, pady=10, fill='x')

        ctk.CTkButton(
            window,
            text='Редактировать',
            fg_color='#bf6c08',
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_jockey_editing_window(jockey_id, window)
        ).grid(row=8, column=0, sticky='ew')
        ctk.CTkButton(
            window,
            text='Удалить',
            fg_color='maroon',
            font=ctk.CTkFont(size=18),
            command=lambda: self._delete_jockey(jockey_id, window)
        ).grid(row=8, column=1, sticky='ew')

    def _show_hippodrome_info(self, hippodrome_id: int) -> None:
        """
        Отрисовывает окно с информацией о выбранном ипподроме.

        :param hippodrome_id: id выбранного ипподрома.
        :param hippodrome_id: int
        """
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
            ArgumentSendButton(
                scrollable_frame,
                self._show_race_info,
                text=race[1],
                arg=race[0]
            ).pack(padx=10, pady=10, fill='x')

        ctk.CTkButton(
            window,
            text='Редактировать',
            fg_color='#bf6c08',
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_hippodrome_editing_window(hippodrome_id, window)
        ).grid(row=5, column=0,sticky='ew')
        ctk.CTkButton(
            window,
            text='Удалить',
            fg_color='maroon',
            font=ctk.CTkFont(size=18),
            command=lambda: self._delete_hippodrome(hippodrome_id, window)
        ).grid(row=5, column=1, sticky='ew')

    def _show_owner_info(self, owner_id: int) -> None:
        """
        Отрисовывает окно с информацией о выбранном владельце.

        :param owner_id: id выбранного владельца.
        :param owner_id: int
        """
        window = ctk.CTkToplevel()
        window.title('Информация о владельце')
        window.geometry('350x500')
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

        ctk.CTkButton(
            window,
            text='Редактировать',
            fg_color='#bf6c08',
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_owner_editing_window(owner_id, window)
        ).grid(row=7, column=0, sticky='ew')
        ctk.CTkButton(
            window,
            text='Удалить',
            fg_color='maroon',
            font=ctk.CTkFont(size=18),
            command=lambda: self._delete_owner(owner_id, window)
        ).grid(row=7, column=1, sticky='ew')
        ctk.CTkButton(
            window,
            text='Добавить лошадь',
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_horse_adding_window(owner_id, window)
        ).grid(row=8, column=0, columnspan=2, sticky='ew')
        
        for horse in owner['horses']:
            ArgumentSendButton(
                scrollable_frame,
                self._show_horse_info,
                text=horse[1],
                arg=horse[0]
            ).pack(padx=10, pady=10, fill='x')

    def _show_horse_info(self, horse_id: int) -> None:
        """
        Отрисовывает окно с информацией о выбранной лошади.

        :param horse_id: id выбранного коня.
        :param horse_id: int
        """
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
        ctk.CTkButton(
            window,
            text=horse['info'][3],
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_owner_info(horse['info'][4])
        ).grid(row=3, column=1, pady=10, padx=10, sticky='ew')

        scrollable_frame = ctk.CTkScrollableFrame(window)
        scrollable_frame.grid(row=5, column=0, rowspan=3, columnspan=2, sticky='ew')
        for race in horse['races']:
            ArgumentSendButton(
                scrollable_frame,
                self._show_race_info,
                text=race[1],
                arg=race[0]
            ).pack(padx=10, pady=10, fill='x')

        ctk.CTkButton(
            window,
            text='Редактировать',
            fg_color='#bf6c08',
            font=ctk.CTkFont(size=18),
            command=lambda: self._show_horse_editing_window(horse_id, window)
        ).grid(row=8, column=0, sticky='ew')
        ctk.CTkButton(
            window,
            text='Удалить',
            fg_color='maroon',
            font=ctk.CTkFont(size=18),
            command=lambda: self._delete_horse(horse_id, window)
        ).grid(row=8, column=1, sticky='ew')

    def _add_race(self,
                  race_data: dict,
                  creation_window: ctk.CTkToplevel) -> None:
        """
        Добавление нового заезда в БД и обновление страницы с заездами.

        :param race_data: данные о новоном заезде.
        :type race_data: dict
        :param creation_window: окно создания, которое нужно закрыть.
        :type creation_window: CTkToplevel
        """
        try:
            race_id = self._db.create_race(
                race_data['name'],
                race_data['date'],
                race_data['hippodrome_id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            ArgumentSendButton(self._races_frame,
                               text=race_data['name'].strip().capitalize(),
                               command=self._show_race_info,
                               arg=race_id).pack(padx=10,pady=10)

    def _edit_race(self,
                  race_data: dict,
                  race_info_window: ctk.CTkToplevel,
                  editing_window: ctk.CTkToplevel) -> None:
        """
        Редактирование заезда,обновление страницы с заездами
        и окна с информацией.

        :param race_data: данные о заезде.
        :type race_data: dict
        :param race_info_window: окно, информацию в котором нужно обновить
        :type race_info_window: CTkToplevel
        :param editing_window: окно редактирования, которое нужно закрыть
        :type editing_window: CTkToplevel
        """
        try:
            self._db.update_race(
                race_data['name'],
                race_data['date'],
                race_data['hippodrome_id'],
                race_data['id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            race_info_window.destroy()
            editing_window.destroy()
            self._show_race_info(race_data['id'])

            for button in self._races_frame.winfo_children():
                if button._arg == race_data['id']:
                    button.configure(text=race_data['name'].capitalize())
                    break

    def _add_race_result(self,
                         race_id: int,
                         race_result_data: dict,
                         creation_window: ctk.CTkToplevel,
                         race_info_window: ctk.CTkToplevel) -> None:
        """
        Добавление нового результата заезда в БД и обновление окна
        с информацией о заезде.

        :param race_id: id заезда, для которого добавляется результат.
        :type race_id: int
        :param race_result_data: данные о новоном результате заезда.
        :type race_result_data: dict
        :param creation_window: окно создания, которое нужно закрыть.
        :type creation_window: CTkToplevel
        :param race_info_window: окно с информацией о заезде, данные
                                 в котором нужно обновить.
        :type race_info_window: CTkToplevel
        """
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
                   owner_data: dict,
                   creation_window: ctk.CTkToplevel) -> None:
        """
        Добавление нового владельца в БД и обновление страницы с владельцами.

        :param owner_data: данные о новоном владельце.
        :type owner_data: dict
        :param creation_window: окно создания, которое нужно закрыть.
        :type creation_window: CTkToplevel
        """
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
            ArgumentSendButton(
                self._owners_frame,
                text=owner_data['name'].strip().lower().capitalize(),
                command=self._show_owner_info,
                arg=owner_id
            ).pack(padx=10, pady=10)
            self._toggle_horse_adding_button_activity()

    def _edit_owner(self,
                   owner_data: dict,
                   owner_info_window: ctk.CTkToplevel,
                   editing_window: ctk.CTkToplevel) -> None:
        """
        Редактирование владельца,обновление страницы с владельцами
        и окна с информацией.

        :param owner_data: данные о владельце.
        :type owner_data: dict
        :param owner_info_window: окно, информацию в котором нужно обновить
        :type owner_info_window: CTkToplevel
        :param editing_window: окно редактирования, которое нужно закрыть
        :type editing_window: CTkToplevel
        """
        try:
            self._db.update_owner(
                owner_data['name'],
                owner_data['telephone'],
                owner_data['address'],
                owner_data['id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            owner_info_window.destroy()
            editing_window.destroy()
            self._show_owner_info(owner_data['id'])

            for button in self._jockeys_frame.winfo_children():
                if button._arg == owner_data['id']:
                    button.configure(text=owner_data['name'].capitalize())
                    break

    def _add_horse(self,
                   horse_data: dict,
                   creation_window: ctk.CTkToplevel,
                   owner_info_window: ctk.CTkToplevel = None) -> None:
        """
        Добавление нового коня в БД, обновление страницы с лошадьми
        и обновление окна владельца, если добавление лошади
        вызвано через него.

        :param horse_data: данные о новоной лошади.
        :type horse_data: dict
        :param creation_window: окно создания, которое нужно закрыть.
        :type creation_window: CTkToplevel
        :param owner_info_window: окно с информацией о владельце,
                                  данные в котором нужно обновить.
        """
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
            ArgumentSendButton(
                self._horses_frame,
                text=horse_data['name'].strip().lower().capitalize(),
                command=self._show_horse_info,
                arg=horse_id
            ).pack(padx=10, pady=10)
            if owner_info_window is not None:
                owner_info_window.destroy()
                self._show_owner_info(horse_data['owner_id'])

    def _edit_horse(self,
                   horse_data: dict,
                   horse_info_window: ctk.CTkToplevel,
                   editing_window: ctk.CTkToplevel) -> None:
        """
        Добавление нового коня в БД, обновление страницы с лошадьми
        и обновление окна владельца, если добавление лошади
        вызвано через него.

        :param horse_data: данные о новоной лошади.
        :type horse_data: dict
        :param creation_window: окно создания, которое нужно закрыть.
        :type creation_window: CTkToplevel
        """
        try:
            self._db.update_horse(
                horse_data['name'],
                horse_data['age'],
                horse_data['gender'],
                horse_data['owner_id'],
                horse_data['id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            horse_info_window.destroy()
            editing_window.destroy()
            self._show_horse_info(horse_data['id'])

            for button in self._horses_frame.winfo_children():
                if button._arg == horse_data['id']:
                    button.configure(text=horse_data['name'].capitalize())
                    break

    def _add_hippodrome(self,
                        name: str,
                        creation_window: ctk.CTkToplevel) -> None:
        """
        Добавление нового ипподрома в БД и обновление страницы с ипподромами.

        :param name: название нового ипподрома.
        :type race_data: str
        :param creation_window: окно создания, которое нужно закрыть.
        :type creation_window: CTkToplevel
        """
        try:
            hippodrome_id = self._db.create_hippodrome(name)
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            ArgumentSendButton(
                self._hippodromes_frame,
                text=name.strip().lower().capitalize(),
                command=self._show_hippodrome_info,
                arg=hippodrome_id
            ).pack(padx=10, pady=10)
            self._toggle_race_adding_button_activity()

    def _edit_hippodrome(self,
                        name: str,
                        hippodrome_id: int,
                        hippodrome_info_window: ctk.CTkToplevel,
                        editing_window: ctk.CTkToplevel) -> None:
        """
        Редактирование ипподрома,обновление страницы с ипподромами
        и окна с информацией.

        :param name: новое название.
        :type race_data: str
        :param creation_window: окно, информацию в котором нужно обновить
        :type creation_window: CTkToplevel
        :param hippodrome_editing_window: окно редактировния, которое нужно закрыть
        :type hippodrome_editing_window: CTkToplevel
        """
        try:
            self._db.update_hippodrome(name, hippodrome_id)
        except Exception as err:
            App.show_message(str(err))
        else:
            editing_window.destroy()
            hippodrome_info_window.destroy()
            self._show_hippodrome_info(hippodrome_id)
            for button in self._hippodromes_frame.winfo_children():
                if button._arg == hippodrome_id:
                    button.configure(text=name.capitalize())
                    break

    def _add_jockey(self,
                    jockey_data: dict,
                    creation_window: ctk.CTkToplevel) -> None:
        """
        Добавление нового жокея в БД и обновление страницы с жокеями.

        :param jockey_data: данные о новоном жокее.
        :type jockey_data: dict
        :param creation_window: окно создания, которое нужно закрыть.
        :type creation_window: CTkToplevel
        """
        try:
            jockey_id = self._db.create_jockey(
                jockey_data['name'],
                jockey_data['age'],
                jockey_data['address'],
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            creation_window.destroy()
            ArgumentSendButton(
                self._jockeys_frame,
                text=jockey_data['name'].strip().lower().capitalize(),
                command=self._show_jockey_info,
                arg=jockey_id
            ).pack(padx=10, pady=10)

    def _edit_jockey(self,
                    jockey_data: dict,
                    jockey_info_window: ctk.CTkToplevel,
                    editing_window: ctk.CTkToplevel) -> None:
        """
        Редактирование жокея,обновление страницы с жокеями
        и окна с информацией.

        :param jockey_data: данные о жокее.
        :type jockey_data: dict
        :param jockey_info_window: окно, информацию в котором нужно обновить
        :type jockey_info_window: CTkToplevel
        :param editing_window: окно редактирования, которое нужно закрыть
        :type editing_window: CTkToplevel
        """
        try:
            self._db.update_jockey(
                jockey_data['name'],
                jockey_data['age'],
                jockey_data['address'],
                jockey_data['id']
            )
        except Exception as err:
            App.show_message(str(err))
        else:
            jockey_info_window.destroy()
            editing_window.destroy()
            self._show_jockey_info(jockey_data['id'])

            for button in self._jockeys_frame.winfo_children():
                if button._arg == jockey_data['id']:
                    button.configure(text=jockey_data['name'].capitalize())
                    break

    def _delete_race_result(self,
                            race_result_id: int,
                            race_result_frame: ctk.CTkFrame) -> None:
        """
        Удаление результата заезда из БД и фрейма с его данными
        из окна с информацией о заезде.

        :param race_result_id: id результата заезда
        :type race_result_id: int
        :param race_result_frame: фрейм результата заезда
        :type race_result_frame: RaceResultFrame
        """
        self._db.delete_race_result(race_result_id)
        race_result_frame.destroy()

    def _delete_race(self,
                     race_id: int,
                     race_info_window: ctk.CTkToplevel) -> None:
        """
        Удаление заезда из БД и обновление страницы
        с заездами.

        :param race_id: id заезда
        :type race_id: int
        :param race_info_window: окно с информацией о заезде, которое нужно закрыть
        :type race_info_window: CTkToplevel
        """
        self._db.delete_race(race_id)
        for button in self._races_frame.winfo_children():
            if button._arg == race_id:
                button.destroy()
                break

        race_info_window.destroy()

    def _delete_hippodrome(self,
                           hippodrome_id: int,
                           hippodrome_info_window: ctk.CTkToplevel) -> None:
        """
        Удаление ипподрома из БД и обновление страницы
        с ипподромами и страницы с заездами.

        :param hippodrome_id: id ипподрома
        :type hippodrome_id: int
        :param hippodrome_info_window: окно с информацией об ипподроме, которое нужно закрыть
        :type hippodrome_info_window: CTkToplevel
        """
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

    def _delete_jockey(self,
                       joceky_id: int,
                       jockey_info_window: ctk.CTkToplevel) -> None:
        """
        Удаление жокея из БД и обновление страницы с жокеями.

        :param joceky_id: id жокея
        :type joceky_id: int
        :param jockey_info_window: окно с информацией о жокее, которое нужно закрыть
        :type jockey_info_window: CTkToplevel
        """
        self._db.delete_jockey(joceky_id)
        for button in self._jockeys_frame.winfo_children():
            if button._arg == joceky_id:
                button.destroy()
                break

        jockey_info_window.destroy()

    def _delete_horse(self,
                      horse_id: int,
                      horse_info_window: ctk.CTkToplevel) -> None:
        """
        Удаление лошади из БД и обновление страницы с лошадьми.

        :param horse_id: id коня
        :type horse_id: int
        :param horse_info_window: окно с информацией о лошади, которое нужно закрыть
        :type horse_info_window: CTkToplevel
        """
        self._db.delete_horse(horse_id)
        for button in self._horses_frame.winfo_children():
            if button._arg == horse_id:
                button.destroy()
                break

        horse_info_window.destroy()

    def _delete_owner(self,
                      owner_id: int,
                      owner_info_window: ctk.CTkToplevel) -> None:
        """
        Удаление владельца из БД и обновление страницы
        с владельцами и страницы с лошадьми.

        :param owner_id: id владельца
        :type owner_id: int
        :param owner_info_window: окно с информацией об ипподроме, которое нужно закрыть
        :type owner_info_window: CTkToplevel
        """
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

    def _toggle_horse_adding_button_activity(self) -> None:
        """Меняет активность кнопки добавления лошади"""
        if not self._db.get_all_owners():
            self._horse_adding_button.configure(state=DISABLED)
        else:
            self._horse_adding_button.configure(state=NORMAL)

    def _toggle_race_adding_button_activity(self) -> None:
        """Меняет активность кнопки добавления заезда"""
        if not self._db.get_all_hippodromes():
            self._race_adding_button.configure(state=DISABLED)
        else:
            self._race_adding_button.configure(state=NORMAL)

    @staticmethod
    def show_message(message: str) -> None:
        """
        Отрисовывает окно с указаным сообщением.

        :param message: сообщение для отображения
        :type message: str
        """
        window = ctk.CTkToplevel()
        window.title('Ошибка')
        window.geometry('650x200')
        ctk.CTkLabel(window, text=message).place(relx=0.5, rely=0.5, anchor='center')

    def run(self) -> None:
        """Гланвый метод, запускающий программу"""
        self._fill_races_frame()
        self._fill_jockeys_frame()
        self._fill_hippodromes_frame()
        self._fill_owners_frame()
        self._fill_horses_frame()

        self._toggle_horse_adding_button_activity()
        self._toggle_race_adding_button_activity()

        self._toggle_races_filter_widgets()
        self._toggle_jockeys_filter_widgets()
        self._toggle_hippodromes_filter_widgets()
        self._toggle_owners_filter_widgets()
        self._toggle_horses_filter_widgets()

        self._main_window.mainloop()


class ArgumentSendButton(ctk.CTkButton):
    """
    Класс кнопки, которая при вызове назначенной на
    нее функции, передает в эту функцию указанный при 
    инициализации аргумент.
    """
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
    """Класс фрейма с информацией о результате заезда"""
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
        LabelWithBg(self, text='Время:',font=ctk.CTkFont(size=18)).grid(row=3, column=0, pady=10, padx=10, sticky='ew')

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
