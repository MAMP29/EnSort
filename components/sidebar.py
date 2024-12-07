import flet as ft

class SideBar(ft.Container):
    def __init__(self):
        super().__init__()
        self.color_bg = "#cde8e5"
        self.bgcolor = self.color_bg
        self.width = 200  # Define el ancho fijo del sidebar
        self.alignment=ft.alignment.center
        #self.expand = expand  # Expande el contenedor verticalmente
        self.rows = [self.create_row()]
        self.rows_column = ft.Column(self.rows, scroll=ft.ScrollMode.AUTO, expand=True)

        self.add_button = ft.ElevatedButton(content=ft.Text("+", color=ft.colors.BLACK), on_click=lambda e: print("Nueva ejecución"), color="#eef7ff")
        
        self.executions_column = ft.Column(
            controls=[],  # Inicialmente vacía
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.executions = ft.Container(
            content=ft.Column(
                controls=[
                    ft.TextButton(content=ft.Text("Prueba 1", color=ft.colors.BLACK)),#, color="#eef7ff") # Puede ser un outlined button o un filedtonedbutton
                    self.executions_column,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centra los botones
            ),
            alignment=ft.alignment.center
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Mis ejecuciones", text_align=ft.TextAlign.CENTER, width='bold', size=20),
                self.executions,
                self.add_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centra horizontalmente
            alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Centra verticalmente
        )

    def create_row(self):
        return ft.Row(
            [
                ft.TextButton(content=ft.Text("aguacates 1", color=ft.colors.BLACK)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def add_results_button(self, execution_button):

        # Añade el botón a la columna de ejecuciones
        self.executions_column.controls.append(execution_button)
        # Actualiza la vista
        self.executions_column.update()