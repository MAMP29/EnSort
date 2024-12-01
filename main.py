import flet as ft
from components.excec_panel import ExecPanel

def main(page: ft.Page):
    page.title = "EnSort"

    page.add(
        ExecPanel(page)
    )

ft.app(target=main)