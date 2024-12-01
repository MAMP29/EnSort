import flet as ft
from components.mainpage import MainPage

def main(page: ft.Page):
    page.title = "EnSort"

    page.add(
        MainPage(page)
    )

ft.app(target=main)