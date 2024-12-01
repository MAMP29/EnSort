import flet as ft

class MainPage(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.color_bg = '#eef7ff'
        self.page.bgcolor = self.color_bg


        self.page.add(
            ft.Button(text="Avocados")
        )