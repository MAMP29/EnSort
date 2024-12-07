import flet as ft 
from textwrap import dedent


class ResultsPanel(ft.Container):
    def __init__(self, execution):
        super().__init__()
        self.name_execution = ft.Text("Panel de los resultados", size=20, weight="bold")
        self.execution = execution

        self.view_for_content()
        self.button_text_examiner()

        # Es necesario mantenerlo así para que no falle
        self.test_message = dedent("""
        # Este es un ejemplo de un panel de resultados 

        Aquí podrás ver los resultados de tus ejecuciones. Cada ejecución tiene su información respectiva, esta se cargará sobre el panel junto a sus gráficos y demás información para que puedas verlas.

        ---

        - **Gráficos:** Información visual sobre los datos.
        - **Detalles:** Información detallada de cada ejecución.
                                
        Selecciona uno de los botones para visualizar los resultados de la ejecución correspondiente.
        """)

        self.buttons_row = ft.Row(
            controls=[
                ft.ElevatedButton(content=ft.Text("lst-dic result", color=ft.Colors.WHITE, width="bold"), bgcolor="#4c5559", disabled=True, on_click=self.change_content_to_lst),
                ft.ElevatedButton(content=ft.Text("BST result", color=ft.Colors.WHITE, width="bold"), bgcolor="#61554e", disabled=True, on_click=self.change_content_to_bst)
            ],
            expand=False
        )

        self.markdown = ft.Markdown(value=self.test_message, selectable=True)

        self.results_text = ft.Container(
            content=ft.Column(
                controls=[
                    self.buttons_row,
                    self.markdown,
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            ),
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            border=ft.border.all(1, ft.colors.BLACK26),
            border_radius=10,
            padding=10,
            expand=True,
        )

        self.extra_info_text = ft.Text("Aquí verás información adicional", 
                                       size=20, 
                                       weight="bold") if self.execution is None else ft.Text(f"Tiempo general: {self.execution.tiempos_de_ejecucion['general']}", 
                                                                                             size=20, 
                                                                                             weight="bold")


        self.extra_info = ft.Container(
            content=self.extra_info_text,
            bgcolor="#e9ecef",
            border=ft.border.all(1, ft.colors.BLACK26),
            border_radius=10,
            padding=5,
            expand=True,
        )

        self.chart_info = ft.Container(
            content=ft.Text("Podrás visualizar gráficas aquí", size=20, weight="bold"),
            bgcolor="#e9ecef",
            border=ft.border.all(1, ft.colors.BLACK26),
            border_radius=10,
            padding=5,
            expand=True,
        )
        
        self.info_panel = ft.Column(
            controls=[
                self.extra_info,
                self.chart_info,
            ],
            spacing=5,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH ,
        )

        self.principal_result_panel = ft.Row(
            controls=[
                self.results_text,
                self.info_panel,
            ],
            spacing=10,
            expand=True,
        )

        self.content = ft.Column(
            controls=[
                self.name_execution,
                self.principal_result_panel,
            ],
            spacing=10,
        )

        # Añadir bordes y estilo al contenedor principal
        self.border = ft.border.all(1, ft.colors.BLACK26)
        self.border_radius = 10
        self.padding = 10
        self.expand = True

    def view_for_content(self):
        if self.execution is not None:
            listas_diccionarios = self.execution.content.get('Listas-diccionarios', None)
            arbol_binario_busqueda = self.execution.content.get('Arbol Binario de Busqueda', None)

            if listas_diccionarios is not None:
                self.buttons_row.controls[0].disabled = False

            if arbol_binario_busqueda is not None:
                self.buttons_row.controls[1].disabled = False

    def change_content_to_lst(self, e):
        self.text_mensaje = self.execution.content['Listas-diccionarios']
        self.buttons_row.controls[0].bgcolor = "#4d869c"
        self.buttons_row.controls[1].bgcolor = "#af4500"
        self.markdown.update()
    
    def change_content_to_bst(self, e):
        self.text_mensaje = self.execution.content['Arbol Binario de Busqueda']
        self.buttons_row.controls[0].bgcolor = "#31393c"
        self.buttons_row.controls[1].bgcolor = "#ee9a63"
        self.markdown.update()

    def button_text_examiner(self):
        if self.execution is None:
            return ft.Text("Aquí verás información adicional", size=20, weight="bold")
        else:
            tiempo_general = self.execution.tiempos_de_ejecucion['general']
            tiempo_listas_diccionarios = self.execution.algoritmos_usados.get("Listas-diccionarios", {}).get("tiempo_ejecucion", "No consideraste esta implementación")
            tiempo_bst = self.execution.algoritmos_usados.get("Arbol Binario de Busqueda", {}).get("tiempo_ejecucion", "No consideraste esta implementación")

            # Concatenar todo en un solo string
            texto = f"Tiempo general: {tiempo_general} \n Tiempo listas-diccionarios: {tiempo_listas_diccionarios} \n Tiempo BST: {tiempo_bst}"

            return ft.Text(texto, size=20, weight="bold")