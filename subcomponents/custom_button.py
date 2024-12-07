import flet as ft

# Botón que representa una ejecución realizada, esta asociada a la misma

class ResultExcutionButton(ft.TextButton):
    def __init__(self, execution, color):
        super().__init__()
        self.execution = execution
        nombre = self.execution.nombre
        self.text = ft.Text(value=nombre, color=color)
        