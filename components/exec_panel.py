import flet as ft
from components.down_panel import DownPanel

class ExecPanel(ft.Container):
    def __init__(self):
        super().__init__()
        self.color_bg = "#eef7ff"
        self.content = ft.Column(
            controls=[
                ft.Text("Panel de Ejecuciones"),
                ft.Button(text="Avocados"),
                DownPanel(),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self.bgcolor = self.color_bg
        self.expand = True  # Permite que el panel derecho ocupe el resto del espacio