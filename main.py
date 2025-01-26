import flet as ft
from input_checker import InputData


def main(page: ft.Page):
    page.window.width = 350
    page.window.height = 570
    page.window.center()

    data = InputData(page)

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "ثبت بیمار"

    # add all option to the front
    page.add(ft.Column(
        controls=[
            data],
        
    ))


if __name__ == "__main__":
    ft.app(main)
