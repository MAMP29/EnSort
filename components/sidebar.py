import flet as ft

class SideBar(ft.Container):
    def __init__(self):
        super().__init__()
        self.color_bg = "#cde8e5"
        self.bgcolor = self.color_bg
        self.width = 200  # Define el ancho fijo del sidebar
        self.alignment=ft.alignment.center
        #self.expand = expand  # Expande el contenedor verticalmente


        self.add_button = ft.ElevatedButton(content=ft.Text("+", color=ft.colors.BLACK), on_click=lambda e: print("Nueva ejecución"), color="#eef7ff")

        self.executions = ft.Container(
            content=ft.Column(
                controls=[
                    ft.FilledTonalButton(content=ft.Text("Prueba 1", color=ft.colors.BLACK), color="#eef7ff")
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centra los botones
            ),
            alignment=ft.alignment.center
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Mis ejecuciones", text_align=ft.TextAlign.CENTER),
                self.executions,
                self.add_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra horizontalmente
            alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Centra verticalmente
        )