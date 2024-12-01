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
        
        self.is_chip_selected = False

        self.chip_for_array_structure = ft.Chip(
            label=ft.Text("Array", color=ft.colors.WHITE),
            bgcolor="#31393c",
            disabled_color="#080a0a",
        )



        # Función para manejar el clic en el chip
        def on_chip_click(e):
            # Cambiar el estado de seleccionado
            self.is_chip_selected = not self.is_chip_selected

            # Actualizar los colores del chip dependiendo de su estado
            if self.is_chip_selected:
                self.chip_for_array_structure.bgcolor = "#4d869c"  # Color cuando está seleccionado
                self.chip_for_array_structure.leading = ft.Icon(ft.Icons.CHECK, color=ft.colors.WHITE)
            else:
                self.chip_for_array_structure.bgcolor = "#080a0a"  # Color cuando no está seleccionado
                self.chip_for_array_structure.label = ft.Text("Array", color=ft.colors.WHITE)
                self.chip_for_array_structure.leading = None

            # Actualizar la página para reflejar el cambio
            self.update()

        # Asignar el evento on_click al chip
        self.chip_for_array_structure.on_click = on_chip_click




        self.structures_to_use = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Estructuras a usar:", color=ft.colors.BLACK, weight="bold", size=20),
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


        def create_decoration_line(bgcolor):
            return ft.Container(
                expand=True,
                bgcolor=bgcolor,
                border_radius=10,
                border=ft.border.all(1, ft.colors.BLACK45),
                padding=ft.padding.all(2),
                margin=ft.margin.all(2)
            )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls = [
                        create_decoration_line("#f5f5dc"),
                        #ft.Container(expand=True),
                        ft.Container(content=self.structures_to_use, alignment=ft.alignment.center_right),
                    ],
                ),

                ft.Container(
                    content=ft.Row(controls = [self.execute_button,create_decoration_line("#4d869c"),]),
                    alignment=ft.alignment.center_left  # Alinea el botón a la derecha
                )
            ],
            alignment=ft.MainAxisAlignment.END,  # Alinea el contenido en la parte inferior
            horizontal_alignment=ft.CrossAxisAlignment.END  # Alinea horizontalmente a la derecha
        )

        self.padding = ft.padding.all(10)  # Añade padding al contenedor principal


