import flet as ft
from doc_file import save_doc
from persiantools.jdatetime import JalaliDate
import re
from msg_handling import MsgHandling


class SendRequests(ft.UserControl):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.dialog = None
        self.start_date_box = self.create_date_boxes("شروع")
        self.end_date_box = self.create_date_boxes("پایان")
        self.msg = MsgHandling(page)

    def alert_txt(self):
        return ft.Text("لطفا تاریخ مورد نظر را انتخاب کنید", rtl=True)

    def choose_date(self):
        self.dialog = ft.AlertDialog(
            modal=True,
            content=self.alert_txt(),
            actions=[
                ft.Column(
                    controls=[
                        self.start_date_box,
                        self.end_date_box,
                        ft.Row(
                            controls=[
                                ft.TextButton("OK", on_click=lambda _: self.ok_dialog(self.start_date_box.value,
                                                                                      self.end_date_box.value)),
                                ft.TextButton("Cancel", on_click=lambda _: self.cancel_dialog()),
                            ]
                        )],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            open=True
        )

        self.page.dialog = self.dialog
        self.page.update()

    # ok button in date chooser
    def ok_dialog(self, start, end):
        save_doc(self.page, start, end)
        self.start_date_box.value = ""
        self.end_date_box.value = ""
        self.page.close(self.dialog)
        self.page.update()

    # cancel button in date chooser
    def cancel_dialog(self):
        self.start_date_box.value = ""
        self.end_date_box.value = ""
        self.page.close(self.dialog)
        self.page.update()

    # check date that is correct or not
    def date_checking(self, date_box):
        # add or remove automatically / from date box
        if len(date_box.value) in [5, 8]:
            if not date_box.value[-1] == "/":
                date_box.value = date_box.value[:-1] + "/" + date_box.value[-1]

        elif len(date_box.value) in [5, 8] and self.date_box.value[-1] == "/":
            date_box.value = date_box.value[:-1]

        elif len(date_box.value) == 10:
            temp_date = date_box.value.split("/")
            date_pattern = "(\\d{4}[/]+\\d{2}[/]+\\d{2})"

            try:
                JalaliDate(int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))
                date_box.error_text = ""

                if not re.fullmatch(date_pattern, date_box.value):

                    self.date.error_text = "correct format : YYYY/MM/DD"

                elif re.fullmatch(date_pattern, date_box.value):
                    date_box.error_text = ""
                    self.page.update()
                    return True
                try:
                    if date_box.value and isinstance(int("".join(temp_date)), int):
                        pass
                except ValueError:
                    if date_box.value and isinstance("".join(temp_date), str):
                        date_box.error_text = "Date input is invalid"

            except ValueError:
                date_box.error_text = "Date input is invalid"

        self.page.update()

    def create_date_boxes(self, label):
        date_box = ft.TextField(label=label, hint_text="____/__/__", text_align=ft.TextAlign.CENTER,
                                max_length=10, counter_text=" ", width=200,
                                on_change=lambda _: self.date_checking(date_box))
        return date_box
