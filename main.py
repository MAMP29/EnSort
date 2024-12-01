import flet as ft
from components.exec_panel import ExecPanel
from components.sidebar import SideBar

def main(page: ft.Page):
    page.title = "EnSort"
    page.theme_mode = "light"
    page.bgcolor = "#eef7ff"

    # Layout general
    page.add(
        ft.Row(
            controls=[
                SideBar(),
                ExecPanel(),
            ],
            alignment=ft.MainAxisAlignment.START,  # Sidebar al inicio
            spacing=5, # Sin espacio entre sidebar y panel
            expand=True
        )
    )

ft.app(target=main)