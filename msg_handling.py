import flet as ft


class MsgHandling(ft.UserControl):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.popup_msg = None

    def error_dialog(self, error_text, width=400, height=80, size=20, rtl=False, position=ft.TextAlign.CENTER):

        # define error msg
        self.popup_msg = ft.AlertDialog(
            content=ft.Container(
                height=height,
                content=ft.Text(value=error_text, size=size, rtl=rtl, text_align=position),
                width=width

            ),
            actions=[ft.Container(
                width=width,
                content=ft.TextButton(
                    text="خروج", on_click=lambda _: self.closing_msg()
                )
            )],
            open=True
        )

        self.page.dialog = self.popup_msg
        self.page.update()

    def closing_msg(self):
        self.popup_msg.open = False

        self.page.update()
