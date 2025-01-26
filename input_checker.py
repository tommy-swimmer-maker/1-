import flet as ft
from erfandb import save_data
from persiantools.jdatetime import JalaliDate
import re
from db_requests import SendRequests
from msg_handling import MsgHandling
import os
import sys


class InputData(ft.UserControl):
    dropdowns = [
        {'value': 'CBC-BG', 'amount': 1_500_000},
        {'value': 'PC', 'amount': 1_500_000},
        {'value': 'LPC', 'amount': 2_000_000},
        {'value': 'FFP', 'amount': 1_000_000},
        {'value': 'Cryo', 'amount': 1_000_000},
        {'value': 'Plt-RD', 'amount': 1_000_000},
        {'value': 'Plt-SD', 'amount': 1_500_000},
        {'value': 'WPC', 'amount': 2_000_000},
        {'value': 'Cross Match', 'amount': 2_000_000}]

    tests = {}

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        req = SendRequests(page)
        self.msg = MsgHandling(self.page)

        # name input
        self.name = ft.TextField(hint_text="نام و نام خانوادگی", rtl=True,
                                 text_align=ft.TextAlign.CENTER, width=300,
                                 autofocus=True, on_change=self.name_checker, border_radius=10)

        # date input
        self.date = ft.TextField(label="تاریخ", hint_text="YYYY/MM/DD", text_align=ft.TextAlign.CENTER,
                                 width=300, on_change=self.date_checker, border_radius=10,
                                 max_length=10, counter_text=" ")

        # dropdown setting and khadamat option to choose
        self.dropdown = ft.Dropdown(label="انتخاب خدمات",
                                    options=[ft.dropdown.Option(db['value']) for db in self.dropdowns],
                                    width=120, on_change=self.test_check, border_radius=10)

        # number of tests
        self.tedad = ft.TextField(value=1, text_align=ft.TextAlign.CENTER, width=70, border_radius=10)

        # add or edit button
        self.sabt_button = ft.IconButton(icon=ft.icons.ADD, width=40, on_click=self.add_khedmat, tooltip="افزودن")
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, width=40, tooltip="ویرایش", on_click=self.edit_tests)

        # edit selected tests
        self.edit_db = ft.Dropdown(label="انتخاب خدمات",
                                   width=120, visible=False, on_change=self.edit_tests, options=[])
        self.virayesh_tedad = ft.TextField(width=60,
                                           text_align=ft.TextAlign.CENTER, visible=False,
                                           on_change=self.save_changes)

        self.delete_bt = ft.IconButton(icon=ft.icons.DELETE, tooltip="حذف تست",
                                       visible=False, on_click=self.delete_test)

        self.save_bt = ft.IconButton(icon=ft.icons.SAVE, tooltip="ثبت تغییرات",
                                     visible=False, on_click=self.save_edited_tests)

        # done test
        self.done_test = ft.TextField(label="تست های انجام شده", value="", disabled=True,
                                      width=300, border_radius=10, multiline=True)

        # gheymat
        self.price = ft.TextField(value=0, label="قیمت نهایی", text_align=ft.TextAlign.CENTER,
                                  width=300, disabled=True, prefix_text="ریال", border_radius=10)

        # define save and search button
        self.save_button = ft.IconButton(icon=ft.icons.SAVE, width=150,
                                         on_click=self.save_button_click, tooltip="ذخیره")
        # define search button
        self.search_button = ft.IconButton(icon=ft.icons.SEARCH_SHARP, width=150,
                                           tooltip="جست و جو",
                                           on_click=lambda _: self.msg.error_dialog(
                                               "این قابلیت به زودی فعال می گردد",
                                               height=70))

        # define search and save button in a row
        self.data_button = ft.Row(controls=[self.search_button, self.save_button],
                                  alignment=ft.MainAxisAlignment.CENTER)

        # define saving file button
        self.word = ft.IconButton(content=ft.Image(src=self.resource_path("icon/microsoft-word-icon.png")
                                                   , width=30, height=30),
                                  on_click=lambda _: req.choose_date(), width=50, tooltip="Word ایجاد فایل", )

        self.excel = ft.IconButton(content=ft.Image(src=self.resource_path("icon/microsoft-excel-icon.png")
                                                    , width=30, height=30),
                                   width=50, tooltip="Excel ایجاد فایل",
                                   on_click=lambda _: self.msg.error_dialog("این قابلیت به زودی فعال می گردد",
                                                                            height=70))

        self.printer = ft.IconButton(icon=ft.icons.PRINT, width=50, icon_size=30, tooltip="چاپ",
                                     on_click=lambda _: self.msg.error_dialog("این قابلیت به زودی فعال می گردد",
                                                                              height=70))

        self.preview = ft.IconButton(icon=ft.icons.PREVIEW, icon_size=30, width=50, tooltip="پیش نمایش",
                                     on_click=lambda _: self.msg.error_dialog("این قابلیت به زودی فعال می گردد",
                                                                              height=70))

        self.create_file = ft.Row(controls=[self.word, self.excel, self.preview, self.printer],
                                  alignment=ft.MainAxisAlignment.CENTER)

        # all element of add or edit test store in row
        self.khedmat_button = ft.Row(controls=[self.dropdown,
                                               self.edit_db,
                                               self.virayesh_tedad,
                                               self.delete_bt, self.save_bt,
                                               self.tedad, self.sabt_button,
                                               self.edit_button],
                                     alignment=ft.MainAxisAlignment.CENTER)

        self.page.add(ft.Column(controls=[self.name,
                                          self.date,
                                          self.khedmat_button,
                                          self.done_test,
                                          self.price,
                                          self.data_button,
                                          self.create_file,
                                          ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    def name_checker(self, e):
        persian_name = "([\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u200C\u200F]+.*)"
        if self.name.value and not re.fullmatch(persian_name, self.name.value):
            self.name.error_text = "لطفا نام بیمار را به فارسی وارد کنید"
            self.page.update()
        elif re.fullmatch(persian_name, self.name.value):
            self.name.error_text = ""
            self.page.update()
            return True

    def resource_path(self, relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # check entry date
    def date_checker(self, e):
        # add or remove / after 4 and 6 character
        if len(self.date.value) in [5, 8]:
            if not self.date.value[-1] == "/":
                self.date.value = self.date.value[:-1] + "/" + self.date.value[-1]

        elif len(self.date.value) in [5, 8] and self.date.value[-1] == "/":
            self.date.value = self.date.value[:-1]

        # check date after 10 character
        elif len(self.date.value) == 10:
            temp_date = self.date.value.split("/")
            date_pattern = "(\\d{4}[/]+\\d{2}[/]+\\d{2})"

            try:
                JalaliDate(int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))
                self.date.error_text = ""

                if not re.fullmatch(date_pattern, self.date.value):

                    self.date.error_text = "correct format : YYYY/MM/DD"

                elif re.fullmatch(date_pattern, self.date.value):
                    self.date.error_text = ""
                    self.page.update()
                    return True
                try:
                    if self.date.value and isinstance(int("".join(temp_date)), int):
                        pass
                except ValueError:
                    if self.date.value and isinstance("".join(temp_date), str):
                        self.date.error_text = "Date input is invalid"

            except ValueError:
                self.date.error_text = "Date input is invalid"

        self.page.update()

    # add done tests
    def add_khedmat(self, e):

        if int(self.tedad.value) > 0:

            if not self.dropdown.value:
                self.dropdown.width = 200
                self.dropdown.error_text = "لطفا ابتدا یک تست را انتخاب کنید"
                self.tedad.visible = False
                self.edit_button.visible = False
                self.sabt_button.visible = False
                self.page.update()

            if self.test_check(e):
                selected_khedmat = self.dropdown.value
                tedad_khedmat = int(self.tedad.value)

                if selected_khedmat not in self.tests.keys():
                    self.tests[selected_khedmat] = tedad_khedmat
                    item = len(self.tests)
                    self.done_test.value += (f"{list(self.tests.items())[item - 1][0]}"
                                             f"({list(self.tests.items())[item - 1][1]}), ")
                    self.page.update()
                elif selected_khedmat in self.tests.keys():
                    self.tests[selected_khedmat] += tedad_khedmat
                    sub_search = r"\b%s\b\(\d+\)" % selected_khedmat
                    sub_changer = "%s(%i)" % (selected_khedmat, self.tests[selected_khedmat])
                    self.done_test.value = re.sub(sub_search, sub_changer, self.done_test.value)
                    self.page.update()

                self.tedad.value = 1

                if isinstance(self.price.value, str):
                    self.price.value = int(self.price.value.replace(",", ""))

                for test in self.dropdowns:
                    if test['value'] == selected_khedmat:
                        self.price.value += (test['amount'] * tedad_khedmat)

                self.price.value = format(f"{self.price.value:,}")

                self.page.update()

        elif int(self.tedad.value) <= 0:
            self.msg.error_dialog("مقدار صحیح نمی باشد.",
                                  400, 30, 20, True, ft.TextAlign.CENTER)

    # check for test entry
    def test_check(self, e):
        if self.dropdown.value:
            self.dropdown.width = 120
            self.dropdown.error_text = ""
            self.tedad.visible = True
            self.edit_button.visible = True
            self.sabt_button.visible = True
            self.page.update()
            return True

    # edit done tests
    def edit_tests(self, e):

        self.sabt_button.visible = False
        self.edit_button.visible = False
        self.dropdown.visible = False
        self.tedad.visible = False
        self.edit_db.visible = True
        self.virayesh_tedad.visible = True
        self.save_bt.visible = True
        self.delete_bt.visible = True
        self.edit_db.options = [ft.dropdown.Option(key) for key in self.tests.keys()]
        self.virayesh_tedad.value = self.tests[self.edit_db.value] if self.edit_db.value else 0

        self.page.update()

    # save edited tests
    def save_edited_tests(self, e):

        self.edit_db.value = ""
        self.dropdown.value = ""
        self.edit_db.options = []
        self.virayesh_tedad.value = 0
        self.edit_db.visible = False
        self.virayesh_tedad.visible = False
        self.save_bt.visible = False
        self.delete_bt.visible = False
        self.sabt_button.visible = True
        self.edit_button.visible = True
        self.dropdown.visible = True
        self.tedad.visible = True
        for esm, meghdar in list(self.tests.items()):
            if not meghdar:
                sub_search = r"\b%s\b\(\d+\), " % esm
                sub_changer = ""
                self.done_test.value = re.sub(sub_search, sub_changer, self.done_test.value)
                del self.tests[esm]
        self.page.update()
        return True

    # delete done test
    def delete_test(self, e):

        if not self.edit_db.value:
            self.msg.error_dialog("No test selected for deletion")
            return

        try:

            # delete test from list
            sub_search = r"\b%s\b\(\d+\), " % self.edit_db.value
            self.done_test.value = re.sub(sub_search, "", self.done_test.value)
            deleted_test = self.edit_db.value
            tedad_test = self.tests.pop(self.edit_db.value)
            self.edit_db.options = [ft.dropdown.Option(key) for key in self.tests.keys()]
            self.edit_db.value = ""
            self.virayesh_tedad.value = 0

            if isinstance(self.price.value, str):
                self.price.value = int(self.price.value.replace(",", ""))

            for test in self.dropdowns:
                if test['value'] == deleted_test:
                    self.price.value -= (test['amount'] * tedad_test)

            if "," in str(self.price.value):
                self.price.value = int(self.price.value.replace(",", ""))

            self.price.value = format(f"{self.price.value:,}")

        except ValueError as ex:
            self.msg.error_dialog(str(ex))

        self.page.update()

    # save changes
    def save_changes(self, e):

        if not self.edit_db.value and not self.save_edited_tests:
            self.msg.error_dialog("Please select a valid test")
            return

        if not self.virayesh_tedad.value and not self.save_edited_tests:
            self.msg.error_dialog("Please enter a valid number")
            return

        try:
            # remove , from price and change it to int
            if isinstance(self.price.value, str):
                self.price.value = int(self.price.value.replace(",", ""))

            # only act when the test and number of them is different
            if self.edit_db.value and self.tests[self.edit_db.value] != self.virayesh_tedad.value:
                # change the price after change tedad
                for test in self.dropdowns:
                    if test['value'] == self.edit_db.value:
                        tedad_test = self.tests[test['value']]
                        if int(self.virayesh_tedad.value) > tedad_test:
                            self.price.value += (test['amount'] * (int(self.virayesh_tedad.value) - tedad_test))
                        elif int(self.virayesh_tedad.value) < tedad_test:
                            self.price.value -= (test['amount'] * (tedad_test - int(self.virayesh_tedad.value)))

                self.tests[self.edit_db.value] = int(self.virayesh_tedad.value)
                sub_search = r"\b%s\b\(\d+\)" % self.edit_db.value
                sub_changer = "%s(%i)" % (self.edit_db.value, int(self.tests[self.edit_db.value]))
                self.done_test.value = re.sub(sub_search, sub_changer, self.done_test.value)
                self.page.update()
        except ValueError as ex:
            # check if box is empty no error return
            if isinstance(self.price.value, int):
                return
            self.msg.error_dialog(str(ex))

        self.price.value = format(f"{self.price.value:,}")

        self.page.update()

    # check done tests that input or not
    def done_test_checker(self, e):

        if not self.done_test.value:
            self.done_test.error_text = "لطفا حداقل یک تست را انتخاب کنید"
            self.page.update()

        else:
            self.done_test.error_text = ""
            self.page.update()
            return True

    # save all test inside db
    def save_button_click(self, e):

        if not self.name.value:
            self.name.error_text = "لطفا نام را وارد کنید!"
            self.page.update()
        if not self.date.value:
            self.date.error_text = "Please enter the date."
            self.page.update()

        if self.name_checker(e) and self.date_checker(e) and self.done_test_checker(e):
            save_data(self.page, self.name.value, self.date.value, self.done_test.value, self.price.value)
            self.selected_khedmat = ""
            self.tests.clear()
            self.date.error_text = ""
            self.name.value = ""
            self.name.focus()
            self.date.value = ""
            self.dropdown.value = ""
            self.done_test.value = ""
            self.price.value = 0
            self.page.update()
