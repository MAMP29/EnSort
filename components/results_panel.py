import flet as ft 
from textwrap import dedent


class ResultsPanel(ft.Container):
    def __init__(self):
        super().__init__()
        self.name_execution = ft.Text("Panel de los resultados", size=20, weight="bold")

        # Es necesario mantenerlo así para que no falle
        self.test_message = dedent("""
        # Este es un ejemplo de un panel de resultados 

        Aquí podrás ver los resultados de tus ejecuciones. Cada ejecución tiene su información respectiva, esta se cargará sobre el panel junto a sus gráficos y demás información para que puedas verlas.

        ---

        - **Gráficos:** Información visual sobre los datos.
        - **Detalles:** Información detallada de cada ejecución.
        """)

        self.results_text = ft.Container(
            content=ft.Markdown(
                value=self.test_message,
                selectable=True,
            ),
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.BLACK26),
            border_radius=10,
            padding=10,
            expand=True,
        )

        self.extra_info = ft.Container(
            content=ft.Text("Aquí verás información adicional", size=20, weight="bold"),
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