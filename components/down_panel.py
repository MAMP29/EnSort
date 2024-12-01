import flet as ft

class DownPanel(ft.Container):
    def __init__(self):
        super().__init__()
        self.color_bg = "#7ab2b2"
        self.bgcolor = self.color_bg
        #self.expand = True
        self.execute_button = ft.ElevatedButton(
            content=ft.Text("Ejecutar", weight="bold", color=ft.colors.WHITE, size=20), 
            bgcolor="#4d869c",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding={
                    ft.MaterialState.DEFAULT: ft.padding.all(15)  # Añade padding al botón
                }
            )
        )

        self.chip_for_array_structure = ft.Chip(
            label=ft.Text("Array"),
        )

        self.structures_to_use = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Estructura a usar:", color=ft.colors.BLACK, weight="bold", size=20),
                    ft.Row(
                        controls=[
                            self.chip_for_array_structure,
                        ]
                            
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            bgcolor="#f5f5dc",
            border_radius=10,  # Añade bordes redondeados
            border=ft.border.all(1, ft.colors.BLACK45),  # Añade un borde delgado
            padding=ft.padding.all(5),  # Añade padding interno
            margin=ft.margin.all(5)  # Añade margen externo
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls = [
                        ft.Container(expand=True),
                        ft.Container(content=self.structures_to_use, alignment=ft.alignment.center_right),
                    ],
                ),

                ft.Container(
                    content=self.execute_button,
                    alignment=ft.alignment.center_left  # Alinea el botón a la derecha
                )
            ],
            alignment=ft.MainAxisAlignment.END,  # Alinea el contenido en la parte inferior
            horizontal_alignment=ft.CrossAxisAlignment.END  # Alinea horizontalmente a la derecha
        )

        self.padding = ft.padding.all(10)  # Añade padding al contenedor principal