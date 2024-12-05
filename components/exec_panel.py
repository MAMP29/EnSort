import flet as ft
from components.down_panel import DownPanel

class ExecPanel(ft.Container):
    def __init__(self, file_picker):
        super().__init__()
        self.color_bg = "#eef7ff"

        self.selected_file = ft.Text()
        self.file_picker = file_picker #ft.FilePicker(on_result=self.pick_file_result)
        self.selected_file = None  # Variable para guardar la ruta del archivo

        self.button_files = ft.ElevatedButton(
            text="Seleccione el archivo",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(allow_multiple=False),
        )

        self.content = ft.Column(
            controls=[
                ft.Text("Panel de Ejecuciones"),
                self.button_files,
                DownPanel(),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.MainAxisAlignment.CENTER
        )
        self.bgcolor = self.color_bg
        self.expand = True  # Permite que el panel derecho ocupe el resto del espacio

        # Añadir bordes y estilo al contenedor principal
        self.border = ft.border.all(1, ft.colors.BLACK26)
        self.border_radius = 10
        self.padding = 10
        self.expand = True

    def set_selected_file(self, file_content):
        # Pasar el contenido del archivo a BSTBasedSurvey
        self.selected_file = file_content
        self.cargar_datos(file_content)

        # Llamar a cargar_datos de BSTBasedSurvey
        #self.bst_survey.cargar_datos(self.selected_file_path)
    
    def cargar_datos(self, file_content):
        print(file_content)