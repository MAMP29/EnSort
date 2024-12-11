import flet as ft
from subcomponents.custom_chip import CustomChip
from subcomponents.custom_button import ResultExcutionButton
from sorting_logic.list_based_survey import ListBasedSurvey
from sorting_logic.binary_tree_based_survey import BSTBasedSurvey
from sorting_logic.execution import Execution
import datetime
import time
import os

class DownPanel(ft.Container):
    def __init__(self, results_manager):
        super().__init__()
        self.color_bg = "#7ab2b2"
        self.bgcolor = self.color_bg
        self.result_manager = results_manager
#        self.sidebar = sidebar

        self.file_name = None
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

    def set_content(self, file_content, nombre_archivo):
        self.file_name = nombre_archivo
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

        # Tiempo general
        tiempo_inicio_general = time.time()

        timestamp_id = str(int(time.time()))
        hour_and_date = self.format_timestamp_id(timestamp_id)

        ejecucion = Execution(os.path.splitext(self.file_name)[0])
        ejecucion.content = self.file_content

        # Calcular tamaño entrada y medir tiempos
        tiempo_inicio_tamano = time.time()
        participantes_raw, temas_preguntas_raw = ejecucion.calcular_tamano_entrada()
        tiempo_fin_tamano = time.time()

        algoritmos_usados = [] 
        print(ejecucion.tamano_entrada)

        if self.file_content is not None:
            self.button_execution_mode()
            print("List-dict esta: ", self.list_dict_chip.is_selected)
            print("BST esta: ", self.binary_tree_chip.is_selected)

            # Resultados de los algoritmos
            resultados = {}

            if self.list_dict_chip.is_selected == True:
                print("Ejecutando por list-array")
                algoritmos_usados.append("Listas-Diccionarios")

                tiempo_inicio_lst = time.time()
                salida_lst = self.list_dict_based_survey.ejecutar_proceso(self.file_content, participantes_raw=participantes_raw, temas_preguntas_raw=temas_preguntas_raw)
                tiempo_fin_lst = time.time()

                resultados["Listas-diccionarios"] = {
                    "salida": salida_lst,
                    "tiempo_ejecucion": round(tiempo_fin_lst - tiempo_inicio_lst, 4)
                }

                print(salida_lst)
                print("---------------------------------------------------------")

            if self.binary_tree_chip.is_selected == True:
                print("Ejecutando por BST")
                algoritmos_usados.append("Arbol Binario de Busqueda")

                tiempo_inicio_bst = time.time()
                salida_bst = self.bst_based_survey.ejecutar_proceso(self.file_content, participantes_raw=participantes_raw, temas_preguntas_raw=temas_preguntas_raw)
                tiempo_fin_bst = time.time()

                resultados["Arbol Binario de Busqueda"] = {
                    "salida": salida_bst,
                    "tiempo_ejecucion": round(tiempo_fin_bst - tiempo_inicio_bst, 4)
                }

                print(salida_bst)
                print("---------------------------------------------------------")

            ejecucion.content = resultados
            

            self.button_normal_mode()
            tiempo_fin_general = time.time()
            ejecucion.cargar_datos_ejecucion(timestamp_id, hour_and_date, algoritmos_usados)

             # Agregar tiempos al objeto de ejecución
            ejecucion.tiempos_de_ejecucion = {
                "general": round(tiempo_fin_general - tiempo_inicio_general, 4),
                "tamano_entrada": round(tiempo_fin_tamano - tiempo_inicio_tamano, 4),
                **{alg: resultados[alg]["tiempo_ejecucion"] for alg in resultados}
            }
            
            print("Tiempos de ejecución:", ejecucion.tiempos_de_ejecucion)

            print("NOMbre ejecucion:", ejecucion.nombre)
            #result_button = ResultExcutionButton(execution=ejecucion, color=ft.colors.BLACK)

            #self.page.controls[0].controls[0].add_results_button(result_button)
            self.result_manager.add_result_button(ejecucion)
            

    def format_timestamp_id(self, timestamp_id):
        timestamp_seconds = int(timestamp_id)
        hour_and_date = datetime.datetime.fromtimestamp(timestamp_seconds)
        format_hour_and_date = hour_and_date.strftime("%Y-%m-%d %H:%M:%S")
        return format_hour_and_date