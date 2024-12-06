import flet as ft
from subcomponents.custom_chip import CustomChip
from sorting_logic.list_based_survey import ListBasedSurvey
from sorting_logic.binary_tree_based_survey import BSTBasedSurvey

class DownPanel(ft.Container):
    def __init__(self):
        super().__init__()
        self.color_bg = "#7ab2b2"
        self.bgcolor = self.color_bg

        self.file_content = None

        self.list_dict_based_survey = ListBasedSurvey()
        self.bst_based_survey = BSTBasedSurvey()

        #self.expand = True
        self.execute_button = ft.ElevatedButton(
            content=ft.Text("Ejecutar", weight="bold", color=ft.colors.WHITE, size=20), 
            bgcolor="#4d869c",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding={
                    ft.MaterialState.DEFAULT: ft.padding.all(15)  # Añade padding al botón
                }
            ),
            on_click=self.execute_sorting,
        )
        
        self.list_dict_chip = CustomChip(label="List-Dict", initial_color="#31393c", selected_color="#4d869c")
        self.binary_tree_chip = CustomChip(label="BST", initial_color="#af4500", selected_color="#ee9a63")


        self.structures_to_use = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Estructuras a usar:", color=ft.colors.BLACK, weight="bold", size=20),
                    ft.Row(
                        controls=[
                            self.list_dict_chip,
                            self.binary_tree_chip
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

    def set_content(self, file_content):
        self.file_content = file_content
        print(file_content)

    def button_execution_mode(self):
        self.execute_button.disabled = True
        self.execute_button.bgcolor = "#435860"
        self.execute_button.content = ft.Text("Ejecutando...", weight="bold", color=ft.colors.WHITE, size=20)
        self.execute_button.update()

    def button_normal_mode(self):
        self.execute_button.disabled = False
        self.execute_button.bgcolor = "#4d869c"
        self.execute_button.content = ft.Text("Ejecutar", weight="bold", color=ft.colors.WHITE, size=20)
        self.execute_button.update()

    def execute_sorting(self, e):
        if self.file_content is not None:
            self.button_execution_mode()
            print("List-dict esta: ", self.list_dict_chip.is_selected)
            print("BST esta: ", self.binary_tree_chip.is_selected)
            if self.list_dict_chip.is_selected == True:
                print("Ejecutando por list-array")
                salida_lst = self.list_dict_based_survey.ejecutar_proceso(self.file_content)
                print(salida_lst)
                print("---------------------------------------------------------")

            if self.binary_tree_chip.is_selected == True:
                print("Ejecutando por BST")
                salida_bst = self.bst_based_survey.ejecutar_proceso(self.file_content)
                print(salida_bst)
                print("---------------------------------------------------------")
            
            self.button_normal_mode()

